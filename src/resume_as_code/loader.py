from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Tuple


class ResumeSpecError(ValueError):
    pass


@dataclass
class ParsedLine:
    line_number: int
    indent: int
    content: str


def load_resume_spec(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    text = source.read_text(encoding="utf-8")
    suffix = source.suffix.lower()
    if suffix == ".json":
        data = json.loads(text)
    elif suffix in {".yaml", ".yml"}:
        data = parse_yaml_subset(text)
    else:
        raise ResumeSpecError(
            f"Unsupported file type '{source.suffix}'. Use .json, .yaml, or .yml."
        )

    if not isinstance(data, dict):
        raise ResumeSpecError("The top-level resume document must be a mapping/object.")
    return data


def parse_yaml_subset(text: str) -> Any:
    lines = _prepare_lines(text)
    if not lines:
        return {}
    value, index = _parse_block(lines, 0, lines[0].indent)
    if index != len(lines):
        trailing = lines[index]
        raise ResumeSpecError(
            f"Unexpected trailing content on line {trailing.line_number}: {trailing.content}"
        )
    return value


def dump_yaml_subset(value: Any, indent: int = 0) -> str:
    prefix = " " * indent
    if isinstance(value, dict):
        lines: List[str] = []
        for key, item in value.items():
            if _is_scalar(item):
                lines.append(f"{prefix}{key}: {_format_scalar(item)}")
            else:
                lines.append(f"{prefix}{key}:")
                lines.append(dump_yaml_subset(item, indent + 2))
        return "\n".join(lines)

    if isinstance(value, list):
        lines = []
        for item in value:
            if _is_scalar(item):
                lines.append(f"{prefix}- {_format_scalar(item)}")
            else:
                lines.append(f"{prefix}-")
                lines.append(dump_yaml_subset(item, indent + 2))
        return "\n".join(lines)

    return f"{prefix}{_format_scalar(value)}"


def _prepare_lines(text: str) -> list[ParsedLine]:
    prepared: list[ParsedLine] = []
    for number, raw in enumerate(text.splitlines(), start=1):
        content = _strip_comment(raw.rstrip())
        if not content.strip():
            continue
        indent = len(content) - len(content.lstrip(" "))
        if indent % 2 != 0:
            raise ResumeSpecError(
                f"Line {number} has odd indentation. Use multiples of two spaces."
            )
        prepared.append(
            ParsedLine(
                line_number=number,
                indent=indent,
                content=content.strip(),
            )
        )
    return prepared


def _strip_comment(line: str) -> str:
    in_single = False
    in_double = False
    for index, character in enumerate(line):
        if character == "'" and not in_double:
            in_single = not in_single
        elif character == '"' and not in_single:
            in_double = not in_double
        elif (
            character == "#"
            and not in_single
            and not in_double
            and (index == 0 or line[index - 1].isspace())
        ):
            return line[:index]
    return line


def _parse_block(
    lines: list[ParsedLine], index: int, indent: int
) -> Tuple[Any, int]:
    current = lines[index]
    if current.indent != indent:
        raise ResumeSpecError(
            f"Unexpected indentation on line {current.line_number}: expected {indent} spaces."
        )

    if current.content.startswith("-"):
        return _parse_sequence(lines, index, indent)
    return _parse_mapping(lines, index, indent)


def _parse_mapping(
    lines: list[ParsedLine], index: int, indent: int
) -> Tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    while index < len(lines):
        line = lines[index]
        if line.indent < indent:
            break
        if line.indent != indent:
            raise ResumeSpecError(
                f"Unexpected indentation on line {line.line_number}: {line.content}"
            )
        if line.content.startswith("-"):
            raise ResumeSpecError(
                f"Mixed sequence and mapping content on line {line.line_number}."
            )

        key, has_value, raw_value = _split_mapping_entry(line.content, line.line_number)
        index += 1
        if has_value:
            result[key] = _parse_scalar(raw_value)
            continue

        if index < len(lines) and lines[index].indent > indent:
            child_indent = lines[index].indent
            result[key], index = _parse_block(lines, index, child_indent)
        else:
            result[key] = None
    return result, index


def _parse_sequence(
    lines: list[ParsedLine], index: int, indent: int
) -> Tuple[list[Any], int]:
    result: list[Any] = []
    while index < len(lines):
        line = lines[index]
        if line.indent < indent:
            break
        if line.indent != indent:
            raise ResumeSpecError(
                f"Unexpected indentation on line {line.line_number}: {line.content}"
            )
        if not line.content.startswith("-"):
            break

        item_text = line.content[1:].lstrip()
        index += 1

        if not item_text:
            if index < len(lines) and lines[index].indent > indent:
                item, index = _parse_block(lines, index, lines[index].indent)
            else:
                item = None
            result.append(item)
            continue

        if _looks_like_mapping(item_text):
            key, has_value, raw_value = _split_mapping_entry(item_text, line.line_number)
            item = {key: _parse_scalar(raw_value) if has_value else None}
            if index < len(lines) and lines[index].indent > indent:
                if not isinstance(item, dict):
                    raise ResumeSpecError(
                        f"Unexpected nested content on line {line.line_number}."
                    )
                extra, index = _parse_mapping(lines, index, lines[index].indent)
                item.update(extra)
            result.append(item)
            continue

        if index < len(lines) and lines[index].indent > indent:
            raise ResumeSpecError(
                f"Scalar list item on line {line.line_number} cannot own nested content."
            )

        result.append(_parse_scalar(item_text))
    return result, index


def _split_mapping_entry(content: str, line_number: int) -> Tuple[str, bool, str]:
    if ":" not in content:
        raise ResumeSpecError(f"Expected ':' on line {line_number}: {content}")
    key, raw_value = content.split(":", 1)
    key = key.strip()
    if not key:
        raise ResumeSpecError(f"Missing key on line {line_number}.")
    raw_value = raw_value.lstrip()
    return key, bool(raw_value), raw_value


def _looks_like_mapping(text: str) -> bool:
    return bool(re.match(r"^[A-Za-z0-9_-]+\s*:", text))


def _parse_scalar(value: str) -> Any:
    lowered = value.lower()
    if lowered in {"null", "~", "none"}:
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if re.fullmatch(r"[+-]?\d+", value):
        return int(value)
    if re.fullmatch(r"[+-]?\d+\.\d+", value):
        return float(value)
    if value.startswith('"') and value.endswith('"'):
        return json.loads(value)
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value


def _is_scalar(value: Any) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def _format_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


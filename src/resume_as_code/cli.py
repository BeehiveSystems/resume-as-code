from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .loader import ResumeSpecError, dump_yaml_subset, load_resume_spec
from .render import render_resume_html
from .sample_data import build_sample_resume
from .schema import ALLOWED_THEMES, normalize_resume, resolve_theme


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="resume-as-code",
        description="Resume-as-code CLI that renders JSON or YAML specs into HTML.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    init_parser = subcommands.add_parser("init", help="Create a starter resume spec.")
    init_parser.add_argument(
        "--format",
        choices=["yaml", "json"],
        default="yaml",
        help="Starter file format.",
    )
    init_parser.add_argument(
        "-o",
        "--output",
        help="Output file path. Defaults to resume.yaml or resume.json.",
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the output file if it already exists.",
    )

    validate_parser = subcommands.add_parser(
        "validate", help="Validate and normalize a resume spec."
    )
    validate_parser.add_argument("spec", help="Path to the resume JSON/YAML file.")

    render_parser = subcommands.add_parser("render", help="Render a resume to HTML.")
    render_parser.add_argument("spec", help="Path to the resume JSON/YAML file.")
    render_parser.add_argument(
        "-o",
        "--output",
        help="Output HTML path. Defaults to the input name with an .html suffix.",
    )
    render_parser.add_argument(
        "--theme",
        choices=sorted(ALLOWED_THEMES),
        help="Override the theme from the resume spec.",
    )
    render_parser.add_argument(
        "--title",
        help="Override the HTML document title.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "init":
            return _run_init(args)
        if args.command == "validate":
            return _run_validate(args)
        if args.command == "render":
            return _run_render(args)
    except ResumeSpecError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    parser.print_help()
    return 1


def _run_init(args: argparse.Namespace) -> int:
    destination = Path(args.output or f"resume.{args.format}")
    if destination.exists() and not args.force:
        raise ResumeSpecError(
            f"{destination} already exists. Use --force to overwrite it."
        )

    sample = build_sample_resume()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if args.format == "json":
        destination.write_text(json.dumps(sample, indent=2) + "\n", encoding="utf-8")
    else:
        destination.write_text(dump_yaml_subset(sample) + "\n", encoding="utf-8")

    print(f"Wrote starter resume spec to {destination}")
    return 0


def _run_validate(args: argparse.Namespace) -> int:
    resume = normalize_resume(load_resume_spec(args.spec))
    basics = resume["basics"]
    print(
        f"Valid resume spec for {basics['name']} with theme {resume['theme']['name']}."
    )
    return 0


def _run_render(args: argparse.Namespace) -> int:
    resume = normalize_resume(load_resume_spec(args.spec))
    if args.theme:
        resume["theme"] = resolve_theme(args.theme)

    output = Path(args.output) if args.output else Path(args.spec).with_suffix(".html")
    output.parent.mkdir(parents=True, exist_ok=True)
    html = render_resume_html(resume, title=args.title)
    output.write_text(html, encoding="utf-8")
    print(f"Rendered resume to {output}")
    return 0

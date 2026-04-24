from __future__ import annotations

from typing import Any

from .loader import ResumeSpecError
from .themes import THEME_PRESETS


ALLOWED_THEMES = frozenset(THEME_PRESETS)


def normalize_resume(document: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        "version": document.get("version", 1),
        "theme": _normalize_theme(document.get("theme")),
        "basics": _normalize_basics(document.get("basics", {})),
        "skills": _normalize_list_of_mappings(document.get("skills", []), "skills"),
        "experience": _normalize_experience(document.get("experience", [])),
        "projects": _normalize_list_of_mappings(document.get("projects", []), "projects"),
        "education": _normalize_list_of_mappings(
            document.get("education", []), "education"
        ),
        "certifications": _normalize_list_of_mappings(
            document.get("certifications", []), "certifications"
        ),
        "awards": _normalize_list_of_mappings(document.get("awards", []), "awards"),
        "sections": _normalize_list_of_mappings(document.get("sections", []), "sections"),
    }

    if normalized["version"] != 1:
        raise ResumeSpecError(
            f"Unsupported schema version '{normalized['version']}'. Only version 1 is supported."
        )

    return normalized


def resolve_theme(theme: Any) -> dict[str, str]:
    return _normalize_theme(theme)


def _normalize_theme(theme: Any) -> dict[str, str]:
    if theme is None:
        name = "classic"
        extra: dict[str, Any] = {}
    elif isinstance(theme, str):
        name = theme
        extra = {}
    elif isinstance(theme, dict):
        name = str(theme.get("name", "classic"))
        extra = theme
    else:
        raise ResumeSpecError("Theme must be a string or mapping.")

    if name not in THEME_PRESETS:
        raise ResumeSpecError(
            f"Unknown theme '{name}'. Allowed themes: {', '.join(sorted(THEME_PRESETS))}."
        )

    preset = THEME_PRESETS[name]
    return {
        "name": name,
        "accent_color": str(extra.get("accent_color", preset["default_accent"])),
        "font_family": str(extra.get("font_family", preset["default_font"])),
    }


def _normalize_basics(basics: Any) -> dict[str, Any]:
    if not isinstance(basics, dict):
        raise ResumeSpecError("`basics` must be a mapping.")

    name = str(basics.get("name", "")).strip()
    if not name:
        raise ResumeSpecError("`basics.name` is required.")

    profiles = basics.get("profiles", [])
    if profiles is None:
        profiles = []
    if not isinstance(profiles, list):
        raise ResumeSpecError("`basics.profiles` must be a list.")

    normalized_profiles = []
    for index, profile in enumerate(profiles, start=1):
        if not isinstance(profile, dict):
            raise ResumeSpecError(f"`basics.profiles[{index}]` must be a mapping.")
        normalized_profiles.append(
            {
                "network": str(profile.get("network", "")).strip(),
                "username": str(profile.get("username", "")).strip(),
                "url": str(profile.get("url", "")).strip(),
            }
        )

    return {
        "name": name,
        "role": str(basics.get("role", "")).strip(),
        "email": str(basics.get("email", "")).strip(),
        "phone": str(basics.get("phone", "")).strip(),
        "location": str(basics.get("location", "")).strip(),
        "website": str(basics.get("website", "")).strip(),
        "summary": str(basics.get("summary", "")).strip(),
        "profiles": normalized_profiles,
    }


def _normalize_list_of_mappings(value: Any, field_name: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ResumeSpecError(f"`{field_name}` must be a list.")

    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            raise ResumeSpecError(f"`{field_name}[{index}]` must be a mapping.")
        normalized.append({str(key): item[key] for key in item})
    return normalized


def _normalize_experience(value: Any) -> list[dict[str, Any]]:
    entries = _normalize_list_of_mappings(value, "experience")
    normalized: list[dict[str, Any]] = []

    for index, item in enumerate(entries, start=1):
        positions = item.get("positions")
        if positions is None:
            normalized.append(item)
            continue

        company = str(item.get("company", "")).strip()
        if not company:
            raise ResumeSpecError(
                f"`experience[{index}].company` is required when `positions` is used."
            )
        if not isinstance(positions, list):
            raise ResumeSpecError(f"`experience[{index}].positions` must be a list.")

        normalized_positions: list[dict[str, Any]] = []
        for position_index, position in enumerate(positions, start=1):
            if not isinstance(position, dict):
                raise ResumeSpecError(
                    f"`experience[{index}].positions[{position_index}]` must be a mapping."
                )
            title = str(position.get("title", "")).strip()
            if not title:
                raise ResumeSpecError(
                    f"`experience[{index}].positions[{position_index}].title` is required."
                )
            normalized_positions.append({str(key): position[key] for key in position})

        item["positions"] = normalized_positions
        normalized.append(item)

    return normalized

from __future__ import annotations

from typing import Any


_STANDARD = {
    "body_font_size": "14px",
    "line_height": "1.45",
    "page_padding": "0.65in 0.7in 0.75in",
    "section_gap": "18px",
    "item_padding": "10px 0",
    "header_gap": "10px",
    "header_pad_b": "18px",
    "name_size": "32px",
    "role_size": "16px",
    "contact_gap": "8px 14px",
    "contact_size": "13px",
    "summary_margin": "18px 0 6px",
    "h2_margin": "0 0 10px",
    "h2_size": "12px",
    "heading_letter_spacing": "0.18em",
    "skill_label_width": "140px",
    "item_subtitle_size": "13px",
    "highlight_margin": "8px 0 0 18px",
    "highlight_li_margin": "4px",
    "pill_padding": "4px 8px",
    "pill_font_size": "12px",
    "skills_grid_gap": "8px",
    "pill_list_gap": "6px",
}

_DENSE = {
    "body_font_size": "13px",
    "line_height": "1.4",
    "page_padding": "0.5in 0.6in 0.6in",
    "section_gap": "14px",
    "item_padding": "8px 0",
    "header_gap": "8px",
    "header_pad_b": "14px",
    "name_size": "28px",
    "role_size": "14px",
    "contact_gap": "6px 12px",
    "contact_size": "12px",
    "summary_margin": "14px 0 4px",
    "h2_margin": "0 0 8px",
    "h2_size": "11px",
    "heading_letter_spacing": "0.12em",
    "skill_label_width": "120px",
    "item_subtitle_size": "12px",
    "highlight_margin": "6px 0 0 18px",
    "highlight_li_margin": "3px",
    "pill_padding": "3px 7px",
    "pill_font_size": "11.5px",
    "skills_grid_gap": "6px",
    "pill_list_gap": "5px",
}

_COMPACT = {
    "body_font_size": "12.5px",
    "line_height": "1.35",
    "page_padding": "0.45in 0.55in 0.55in",
    "section_gap": "11px",
    "item_padding": "6px 0",
    "header_gap": "6px",
    "header_pad_b": "12px",
    "name_size": "26px",
    "role_size": "13px",
    "contact_gap": "5px 10px",
    "contact_size": "11.5px",
    "summary_margin": "12px 0 3px",
    "h2_margin": "0 0 6px",
    "h2_size": "10.5px",
    "heading_letter_spacing": "0.14em",
    "skill_label_width": "110px",
    "item_subtitle_size": "11.5px",
    "highlight_margin": "5px 0 0 17px",
    "highlight_li_margin": "2px",
    "pill_padding": "2px 6px",
    "pill_font_size": "11px",
    "skills_grid_gap": "5px",
    "pill_list_gap": "4px",
}


THEME_PRESETS: dict[str, dict[str, Any]] = {
    "classic": {
        **_STANDARD,
        "default_accent": "#1f4f78",
        "default_font": 'Georgia, "Times New Roman", serif',
        "body_background": "#f3f1ec",
        "card_background": "#fffdf8",
        "muted": "#6b6a67",
        "heading_font": None,
        "use_background_gradient": True,
    },
    "slate": {
        **_STANDARD,
        "default_accent": "#2f5d62",
        "default_font": 'Arial, "Helvetica Neue", sans-serif',
        "body_background": "#e9eff0",
        "card_background": "#ffffff",
        "muted": "#56656a",
        "heading_font": None,
        "use_background_gradient": True,
    },
    "compact": {
        **_COMPACT,
        "default_accent": "#2a3f54",
        "default_font": 'Inter, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
        "body_background": "#f5f6f8",
        "card_background": "#ffffff",
        "muted": "#5a6270",
        "heading_font": None,
        "use_background_gradient": False,
    },
    "technical": {
        **_DENSE,
        "default_accent": "#0b6e4f",
        "default_font": 'Inter, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
        "body_background": "#f2f4f5",
        "card_background": "#ffffff",
        "muted": "#556268",
        "heading_font": 'ui-monospace, "JetBrains Mono", Menlo, Consolas, monospace',
        "use_background_gradient": False,
    },
    "mono": {
        **_COMPACT,
        "default_accent": "#1f2328",
        "default_font": 'ui-monospace, "JetBrains Mono", Menlo, Consolas, monospace',
        "body_background": "#ffffff",
        "card_background": "#ffffff",
        "muted": "#555c62",
        "heading_font": None,
        "use_background_gradient": False,
        "heading_letter_spacing": "0.08em",
    },
}


EXTRA_CSS: dict[str, str] = {
    "technical": """
      h2 {
        border-left: 3px solid var(--accent);
        padding-left: 10px;
      }
      .item-meta {
        font-family: ui-monospace, "JetBrains Mono", Menlo, Consolas, monospace;
      }
      .pill {
        border-radius: 4px;
      }
      .skill-row {
        grid-template-columns: 150px 1fr;
        align-items: baseline;
      }
      .skill-category {
        white-space: nowrap;
        font-size: 10.5px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-family: ui-monospace, "JetBrains Mono", Menlo, Consolas, monospace;
      }
      .skills-grid {
        gap: 4px;
      }
""",
    "mono": """
      .header {
        border-bottom-style: dashed;
        border-bottom-width: 1px;
      }
      .pill {
        border-radius: 2px;
      }
      .contact {
        gap: 4px 10px;
      }
""",
}

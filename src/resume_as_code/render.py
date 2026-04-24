from __future__ import annotations

import re
from html import escape
from typing import Any

from .themes import EXTRA_CSS, THEME_PRESETS


_FONT_STACK_ALLOWED = re.compile(r"[^A-Za-z0-9 ,\-_'\".()]")


def _safe_font_stack(value: str) -> str:
    return _FONT_STACK_ALLOWED.sub("", value)


def render_resume_html(resume: dict[str, Any], title: str | None = None) -> str:
    basics = resume["basics"]
    theme = resume["theme"]
    document_title = title or f"{basics['name']} Resume"

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{escape(document_title)}</title>
    <style>
{build_css(theme)}
    </style>
  </head>
  <body class="theme-{escape(theme['name'])}">
    <main class="page">
      {render_header(basics)}
      {render_summary(basics.get("summary", ""))}
      {render_skills(resume.get("skills", []))}
      {render_experience(resume.get("experience", []))}
      {render_projects(resume.get("projects", []))}
      {render_education(resume.get("education", []))}
      {render_certifications(resume.get("certifications", []))}
      {render_awards(resume.get("awards", []))}
      {render_custom_sections(resume.get("sections", []))}
    </main>
  </body>
</html>
"""


def build_css(theme: dict[str, str]) -> str:
    preset = THEME_PRESETS[theme["name"]]
    accent = theme["accent_color"]
    font_family = _safe_font_stack(theme["font_family"])
    heading_font = _safe_font_stack(preset["heading_font"]) if preset["heading_font"] else font_family

    if preset["use_background_gradient"]:
        body_background_rule = (
            "background:\n"
            "          radial-gradient(circle at top right, rgba(255,255,255,0.75), transparent 35%),\n"
            "          linear-gradient(180deg, var(--background), #dde4e6);"
        )
    else:
        body_background_rule = "background: var(--background);"

    extra = EXTRA_CSS.get(theme["name"], "")

    return f"""      :root {{
        --accent: {accent};
        --text: #1f2328;
        --muted: {preset['muted']};
        --paper: {preset['card_background']};
        --background: {preset['body_background']};
        --rule: rgba(31, 35, 40, 0.15);
      }}

      * {{
        box-sizing: border-box;
      }}

      body {{
        margin: 0;
        {body_background_rule}
        color: var(--text);
        font-family: {font_family};
        font-size: {preset['body_font_size']};
        line-height: {preset['line_height']};
      }}

      .page {{
        width: min(100%, 8.5in);
        min-height: 11in;
        margin: 24px auto;
        padding: {preset['page_padding']};
        background: var(--paper);
        box-shadow: 0 18px 50px rgba(0, 0, 0, 0.08);
      }}

      .header {{
        display: grid;
        gap: {preset['header_gap']};
        padding-bottom: {preset['header_pad_b']};
        border-bottom: 3px solid var(--accent);
      }}

      .name {{
        margin: 0;
        font-size: {preset['name_size']};
        letter-spacing: 0.01em;
        font-family: {heading_font};
      }}

      .role {{
        font-size: {preset['role_size']};
        color: var(--accent);
        font-weight: 700;
      }}

      .contact {{
        display: flex;
        flex-wrap: wrap;
        gap: {preset['contact_gap']};
        color: var(--muted);
        font-size: {preset['contact_size']};
      }}

      .contact a {{
        color: inherit;
        text-decoration: none;
      }}

      .summary {{
        margin: {preset['summary_margin']};
      }}

      section {{
        margin-top: {preset['section_gap']};
      }}

      h2 {{
        margin: {preset['h2_margin']};
        font-size: {preset['h2_size']};
        letter-spacing: {preset['heading_letter_spacing']};
        text-transform: uppercase;
        color: var(--accent);
        font-family: {heading_font};
      }}

      .item {{
        padding: {preset['item_padding']};
        border-top: 1px solid var(--rule);
      }}

      .item:first-of-type {{
        border-top: 0;
        padding-top: 0;
      }}

      .item-head {{
        display: flex;
        justify-content: space-between;
        gap: 16px;
      }}

      .item-title {{
        font-weight: 700;
      }}

      .item-subtitle {{
        color: var(--muted);
        font-size: {preset['item_subtitle_size']};
      }}

      .item-meta {{
        text-align: right;
        color: var(--muted);
        white-space: nowrap;
        font-size: {preset['item_subtitle_size']};
      }}

      .highlights {{
        margin: {preset['highlight_margin']};
        padding: 0;
      }}

      .highlights li {{
        margin-top: {preset['highlight_li_margin']};
      }}

      .skills-grid {{
        display: grid;
        gap: {preset['skills_grid_gap']};
      }}

      .skill-row {{
        display: grid;
        grid-template-columns: {preset['skill_label_width']} 1fr;
        gap: 12px;
      }}

      .skill-category {{
        color: var(--accent);
        font-weight: 700;
      }}

      .pill-list {{
        display: flex;
        flex-wrap: wrap;
        gap: {preset['pill_list_gap']};
      }}

      .pill {{
        padding: {preset['pill_padding']};
        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.65);
        font-size: {preset['pill_font_size']};
      }}

      p {{
        margin: 0;
      }}
{extra}
      @media print {{
        body {{
          background: white;
        }}

        .page {{
          margin: 0;
          width: auto;
          min-height: auto;
          box-shadow: none;
        }}
      }}
"""


def render_header(basics: dict[str, Any]) -> str:
    contact_items = []
    for value in [basics.get("email"), basics.get("phone"), basics.get("location")]:
        if value:
            contact_items.append(f"<span>{escape(str(value))}</span>")

    website = basics.get("website")
    if website:
        contact_items.append(_link(website, website))

    for profile in basics.get("profiles", []):
        label = profile.get("network") or profile.get("username") or profile.get("url")
        url = profile.get("url")
        if label and url:
            contact_items.append(_link(label, url))

    role_html = (
        f'<div class="role">{escape(str(basics["role"]))}</div>' if basics.get("role") else ""
    )
    return f"""
      <header class="header">
        <div>
          <h1 class="name">{escape(str(basics["name"]))}</h1>
          {role_html}
        </div>
        <div class="contact">{' '.join(contact_items)}</div>
      </header>
"""


def render_summary(summary: str) -> str:
    if not summary:
        return ""
    return f"""
      <section>
        <h2>Summary</h2>
        <p class="summary">{escape(summary)}</p>
      </section>
"""


def render_skills(skills: list[dict[str, Any]]) -> str:
    if not skills:
        return ""

    rows = []
    for skill in skills:
        category = escape(str(skill.get("category", "")))
        items = skill.get("items", [])
        if not isinstance(items, list):
            items = [items]
        rendered_items = "".join(
            f'<span class="pill">{escape(str(item))}</span>' for item in items if str(item).strip()
        )
        rows.append(
            f"""
        <div class="skill-row">
          <div class="skill-category">{category}</div>
          <div class="pill-list">{rendered_items}</div>
        </div>
"""
        )

    return f"""
      <section>
        <h2>Skills</h2>
        <div class="skills-grid">
          {''.join(rows)}
        </div>
      </section>
"""


def render_experience(items: list[dict[str, Any]]) -> str:
    if not items:
        return ""
    return render_timeline_section("Experience", items, "company", "title")


def render_projects(items: list[dict[str, Any]]) -> str:
    if not items:
        return ""
    rendered_items = []
    for item in items:
        name = item.get("name", "")
        link = item.get("link")
        description = item.get("description", "")
        title = _link(name, link) if link else escape(str(name))
        body = f"<p>{escape(str(description))}</p>" if description else ""
        rendered_items.append(
            f"""
        <article class="item">
          <div class="item-title">{title}</div>
          {body}
          {render_highlights(item.get("highlights", []))}
        </article>
"""
        )

    return f"""
      <section>
        <h2>Projects</h2>
        {''.join(rendered_items)}
      </section>
"""


def render_education(items: list[dict[str, Any]]) -> str:
    if not items:
        return ""
    return render_timeline_section("Education", items, "institution", "degree")


def render_certifications(items: list[dict[str, Any]]) -> str:
    if not items:
        return ""
    return render_simple_section("Certifications", items, "name", ["issuer", "date"])


def render_awards(items: list[dict[str, Any]]) -> str:
    if not items:
        return ""
    return render_simple_section("Awards", items, "name", ["issuer", "date"])


def render_custom_sections(items: list[dict[str, Any]]) -> str:
    sections = []
    for item in items:
        title = str(item.get("title", "")).strip()
        if not title:
            continue

        paragraphs = item.get("paragraphs", [])
        bullets = item.get("highlights", item.get("items", []))
        if not isinstance(paragraphs, list):
            paragraphs = [paragraphs]

        paragraph_html = "".join(
            f"<p>{escape(str(paragraph))}</p>"
            for paragraph in paragraphs
            if str(paragraph).strip()
        )
        sections.append(
            f"""
      <section>
        <h2>{escape(title)}</h2>
        {paragraph_html}
        {render_highlights(bullets)}
      </section>
"""
        )
    return "".join(sections)


def render_timeline_section(
    heading: str, items: list[dict[str, Any]], org_key: str, role_key: str
) -> str:
    rendered_items = []
    for item in items:
        left_title = escape(str(item.get(role_key, "")))
        left_subtitle = escape(str(item.get(org_key, "")))
        location = escape(str(item.get("location", ""))) if item.get("location") else ""
        date_bits = [str(item.get("start", "")).strip(), str(item.get("end", "")).strip()]
        date_bits = [bit for bit in date_bits if bit]
        summary = item.get("summary")
        summary_html = f"<p>{escape(str(summary))}</p>" if summary else ""
        rendered_items.append(
            f"""
        <article class="item">
          <div class="item-head">
            <div>
              <div class="item-title">{left_title}</div>
              <div class="item-subtitle">{left_subtitle}</div>
              {'<div class="item-subtitle">' + location + '</div>' if location else ''}
            </div>
            <div class="item-meta">{escape(' - '.join(date_bits))}</div>
          </div>
          {summary_html}
          {render_highlights(item.get("highlights", []))}
        </article>
"""
        )

    return f"""
      <section>
        <h2>{escape(heading)}</h2>
        {''.join(rendered_items)}
      </section>
"""


def render_simple_section(
    heading: str, items: list[dict[str, Any]], title_key: str, detail_keys: list[str]
) -> str:
    rendered_items = []
    for item in items:
        details = [str(item.get(key, "")).strip() for key in detail_keys]
        details = [detail for detail in details if detail]
        rendered_items.append(
            f"""
        <article class="item">
          <div class="item-head">
            <div class="item-title">{escape(str(item.get(title_key, '')))}</div>
            <div class="item-meta">{escape(' | '.join(details))}</div>
          </div>
        </article>
"""
        )

    return f"""
      <section>
        <h2>{escape(heading)}</h2>
        {''.join(rendered_items)}
      </section>
"""


def render_highlights(highlights: Any) -> str:
    if not highlights:
        return ""
    if not isinstance(highlights, list):
        highlights = [highlights]
    items = "".join(
        f"<li>{escape(str(highlight))}</li>" for highlight in highlights if str(highlight).strip()
    )
    if not items:
        return ""
    return f'<ul class="highlights">{items}</ul>'


def _link(label: Any, url: Any) -> str:
    return f'<a href="{escape(str(url), quote=True)}">{escape(str(label))}</a>'


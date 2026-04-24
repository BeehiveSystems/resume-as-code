from __future__ import annotations

import re
from html import escape
from typing import Any

from .themes import EXTRA_CSS, THEME_PRESETS


_FONT_STACK_ALLOWED = re.compile(r"[^A-Za-z0-9 ,\-_'\".()]")


def _safe_font_stack(value: str) -> str:
    return _FONT_STACK_ALLOWED.sub("", value)


def _display_url(url: Any) -> str:
    return re.sub(r"^https?://(www\.)?", "", str(url).strip())


def render_resume_html(resume: dict[str, Any], title: str | None = None) -> str:
    basics = resume["basics"]
    theme = resume["theme"]
    document_title = title or f"{basics['name']} Resume"
    sections_html = render_resume_sections(resume)

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
    <div class="resume-pages" id="resume-pages"></div>
    <div class="resume-source" id="resume-source">
      <main class="page page--source">
        {render_header(basics)}
        {sections_html}
      </main>
    </div>
    <script>
{build_pagination_script()}
    </script>
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
        position: relative;
      }}

      .resume-pages {{
        position: absolute;
        top: 0;
        left: -200vw;
        width: 100%;
        visibility: hidden;
        pointer-events: none;
        padding: 24px 0;
      }}

      .resume-source {{
        padding: 24px 0;
      }}

      body.is-paginated .resume-pages {{
        position: static;
        left: auto;
        visibility: visible;
        pointer-events: auto;
      }}

      body.is-paginated .resume-source {{
        display: none;
      }}

      .page {{
        width: min(100%, 8.5in);
        min-height: 11in;
        height: 11in;
        margin: 24px auto;
        padding: {preset['page_padding']};
        background: var(--paper);
        box-shadow: 0 18px 50px rgba(0, 0, 0, 0.08);
        overflow: hidden;
      }}

      .page--source {{
        height: auto;
        overflow: visible;
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

      .resume-header,
      .resume-section,
      .section-item,
      .role-group,
      .position {{
        break-inside: avoid;
        page-break-inside: avoid;
      }}

      .resume-section {{
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

      .item.is-continuation > .item-head .item-title::after {{
        content: " (cont.)";
        color: var(--muted);
        font-weight: 400;
      }}

      .role-group {{
        margin-top: 10px;
      }}

      .position {{
        padding-top: 10px;
        border-top: 1px solid var(--rule);
      }}

      .position:first-child {{
        padding-top: 0;
        border-top: 0;
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

      .highlights .highlights {{
        margin-top: 3px;
        margin-bottom: 2px;
      }}

      .highlights .highlights li {{
        margin-top: 2px;
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

      .resume-section.is-continuation h2::after {{
        content: " (cont.)";
        letter-spacing: normal;
        text-transform: none;
        color: var(--muted);
      }}

      .page--oversize {{
        height: auto;
        overflow: visible;
      }}
{extra}
      @page {{
        size: Letter;
        margin: 0;
      }}

      @media print {{
        body {{
          background: white;
        }}

        .resume-pages,
        .resume-source {{
          padding: 0;
        }}

        .page {{
          margin: 0;
          width: 8.5in;
          box-shadow: none;
          break-after: page;
          page-break-after: always;
        }}

        .page:last-child {{
          break-after: auto;
          page-break-after: auto;
        }}

        .page--source {{
          width: auto;
          min-height: auto;
          height: auto;
          overflow: visible;
        }}
      }}
"""


def render_resume_sections(resume: dict[str, Any]) -> str:
    custom_sections = resume.get("sections", [])
    return "".join(
        [
            render_summary(resume["basics"].get("summary", "")),
            render_custom_sections(custom_sections, placement="after_summary"),
            render_skills(resume.get("skills", [])),
            render_experience(resume.get("experience", [])),
            render_projects(resume.get("projects", [])),
            render_education(resume.get("education", [])),
            render_certifications(resume.get("certifications", [])),
            render_awards(resume.get("awards", [])),
            render_custom_sections(custom_sections, placement="end"),
        ]
    )


def render_header(basics: dict[str, Any]) -> str:
    contact_items = []
    for value in [basics.get("email"), basics.get("phone"), basics.get("location")]:
        if value:
            contact_items.append(f"<span>{escape(str(value))}</span>")

    website = basics.get("website")
    if website:
        contact_items.append(f"<span>{escape(_display_url(website))}</span>")

    for profile in basics.get("profiles", []):
        url = profile.get("url")
        if url:
            contact_items.append(f"<span>{escape(_display_url(url))}</span>")

    role_html = (
        f'<div class="role">{escape(str(basics["role"]))}</div>' if basics.get("role") else ""
    )
    return f"""
      <header class="resume-header header">
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
    return render_section(
        "Summary",
        [f'<div class="section-item"><p class="summary">{escape(summary)}</p></div>'],
    )


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
        <div class="skill-row section-item">
          <div class="skill-category">{category}</div>
          <div class="pill-list">{rendered_items}</div>
        </div>
"""
        )

    return render_section("Skills", rows)


def render_experience(items: list[dict[str, Any]]) -> str:
    if not items:
        return ""

    rendered_items = []
    for item in items:
        if item.get("positions"):
            rendered_items.append(render_grouped_experience_item(item))
        else:
            rendered_items.append(render_timeline_item(item, "company", "title"))

    return render_section("Experience", rendered_items)


def render_projects(items: list[dict[str, Any]]) -> str:
    if not items:
        return ""
    rendered_items = []
    for item in items:
        name = item.get("name", "")
        link = item.get("link")
        description = item.get("description", "")
        url_line = (
            f'<div class="item-subtitle">{escape(_display_url(link))}</div>'
            if link
            else ""
        )
        body = f"<p>{escape(str(description))}</p>" if description else ""
        rendered_items.append(
            f"""
        <article class="item section-item">
          <div class="item-title">{escape(str(name))}</div>
          {url_line}
          {body}
          {render_highlights(item.get("highlights", []))}
        </article>
"""
        )

    return render_section("Projects", rendered_items)


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


def render_custom_sections(
    items: list[dict[str, Any]], placement: str = "end"
) -> str:
    sections = []
    for item in items:
        item_placement = str(item.get("placement", "end")).strip() or "end"
        if item_placement != placement:
            continue
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
      <section class="resume-section">
        <h2>{escape(title)}</h2>
        <div class="section-item">
          {paragraph_html}
          {render_highlights(bullets)}
        </div>
      </section>
"""
        )
    return "".join(sections)


def render_timeline_section(
    heading: str, items: list[dict[str, Any]], org_key: str, role_key: str
) -> str:
    rendered_items = [
        render_timeline_item(item, org_key, role_key)
        for item in items
    ]

    return render_section(heading, rendered_items)


def render_grouped_experience_item(item: dict[str, Any]) -> str:
    company = str(item.get("company", "")).strip()
    location = str(item.get("location", "")).strip()
    summary = item.get("summary")
    summary_html = f"<p>{escape(str(summary))}</p>" if summary else ""
    location_html = (
        f'<div class="item-subtitle">{escape(location)}</div>' if location else ""
    )
    positions = "".join(render_position(position) for position in item.get("positions", []))

    return f"""
        <article class="item section-item">
          <div class="item-head">
            <div>
              <div class="item-title">{escape(company)}</div>
              {location_html}
            </div>
            <div class="item-meta">{escape(format_date_range(item))}</div>
          </div>
          {summary_html}
          {render_highlights(item.get("highlights", []))}
          <div class="role-group">
            {positions}
          </div>
        </article>
"""


def render_position(position: dict[str, Any]) -> str:
    location = str(position.get("location", "")).strip()
    summary = position.get("summary")
    summary_html = f"<p>{escape(str(summary))}</p>" if summary else ""
    location_html = (
        f'<div class="item-subtitle">{escape(location)}</div>' if location else ""
    )

    return f"""
            <div class="position">
              <div class="item-head">
                <div>
                  <div class="item-title">{escape(str(position.get("title", "")))}</div>
                  {location_html}
                </div>
                <div class="item-meta">{escape(format_date_range(position))}</div>
              </div>
              {summary_html}
              {render_highlights(position.get("highlights", []))}
            </div>
"""


def render_timeline_item(item: dict[str, Any], org_key: str, role_key: str) -> str:
    primary = str(item.get(role_key, "")).strip()
    secondary = str(item.get(org_key, "")).strip()
    if not primary:
        primary, secondary = secondary, ""

    location = str(item.get("location", "")).strip()
    subtitle_html = (
        f'<div class="item-subtitle">{escape(secondary)}</div>' if secondary else ""
    )
    location_html = (
        f'<div class="item-subtitle">{escape(location)}</div>' if location else ""
    )
    summary = item.get("summary")
    summary_html = f"<p>{escape(str(summary))}</p>" if summary else ""

    return f"""
        <article class="item section-item">
          <div class="item-head">
            <div>
              <div class="item-title">{escape(primary)}</div>
              {subtitle_html}
              {location_html}
            </div>
            <div class="item-meta">{escape(format_date_range(item))}</div>
          </div>
          {summary_html}
          {render_highlights(item.get("highlights", []))}
        </article>
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
        <article class="item section-item">
          <div class="item-head">
            <div class="item-title">{escape(str(item.get(title_key, '')))}</div>
            <div class="item-meta">{escape(' | '.join(details))}</div>
          </div>
        </article>
"""
        )

    return render_section(heading, rendered_items)


def render_highlights(highlights: Any) -> str:
    if not highlights:
        return ""
    if not isinstance(highlights, list):
        highlights = [highlights]
    rendered: list[str] = []
    for highlight in highlights:
        if isinstance(highlight, dict):
            text = str(highlight.get("text", "")).strip()
            child_html = render_highlights(highlight.get("children", []))
            if text or child_html:
                rendered.append(f"<li>{escape(text)}{child_html}</li>")
        else:
            text = str(highlight).strip()
            if text:
                rendered.append(f"<li>{escape(text)}</li>")
    if not rendered:
        return ""
    return f'<ul class="highlights">{"".join(rendered)}</ul>'


def format_date_range(item: dict[str, Any]) -> str:
    date_bits = [str(item.get("start", "")).strip(), str(item.get("end", "")).strip()]
    return " - ".join(bit for bit in date_bits if bit)


def render_section(heading: str, items: list[str]) -> str:
    content = "".join(item for item in items if item)
    if not content:
        return ""
    return f"""
      <section class="resume-section" data-section-title="{escape(heading, quote=True)}">
        <h2>{escape(heading)}</h2>
        {content}
      </section>
"""


def build_pagination_script() -> str:
    return """
      (() => {
        const PAGES_ID = "resume-pages";
        const SOURCE_ID = "resume-source";

        function createPage(pagesRoot, header, includeHeader) {
          const page = document.createElement("main");
          page.className = "page page--generated";
          if (includeHeader && header) {
            page.appendChild(header.cloneNode(true));
          }
          pagesRoot.appendChild(page);
          return page;
        }

        function cloneSectionShell(section, isContinuation) {
          const shell = section.cloneNode(false);
          shell.innerHTML = "";
          shell.classList.toggle("is-continuation", Boolean(isContinuation));
          const heading = section.querySelector(":scope > h2");
          if (heading) {
            shell.appendChild(heading.cloneNode(true));
          }
          return shell;
        }

        function pageOverflows(page) {
          return page.scrollHeight > page.clientHeight + 1;
        }

        function splitSectionItem(item) {
          const positions = Array.from(
            item.querySelectorAll(":scope > .role-group > .position")
          );

          if (positions.length < 2) {
            return [item.cloneNode(true)];
          }

          const itemHead = item.querySelector(":scope > .item-head");
          const introNodes = Array.from(item.children).filter((child) => {
            return (
              !child.classList.contains("item-head") &&
              !child.classList.contains("role-group")
            );
          });

          return positions.map((position, index) => {
            const clone = item.cloneNode(false);
            if (index > 0) {
              clone.classList.add("is-continuation");
            }

            if (itemHead) {
              clone.appendChild(itemHead.cloneNode(true));
            }

            if (index === 0) {
              for (const introNode of introNodes) {
                clone.appendChild(introNode.cloneNode(true));
              }
            }

            const roleGroup = document.createElement("div");
            roleGroup.className = "role-group";
            roleGroup.appendChild(position.cloneNode(true));
            clone.appendChild(roleGroup);
            return clone;
          });
        }

        function paginateResume() {
          const sourceRoot = document.getElementById(SOURCE_ID);
          const pagesRoot = document.getElementById(PAGES_ID);
          if (!sourceRoot || !pagesRoot) {
            return;
          }

          const sourcePage = sourceRoot.querySelector(".page--source");
          if (!sourcePage) {
            return;
          }

          const header = sourcePage.querySelector(":scope > .resume-header");
          const sections = Array.from(
            sourcePage.querySelectorAll(":scope > .resume-section")
          );

          pagesRoot.innerHTML = "";
          let currentPage = createPage(pagesRoot, header, true);

          for (const section of sections) {
            const items = Array.from(section.querySelectorAll(":scope > .section-item"));
            if (!items.length) {
              continue;
            }

            let sectionShell = null;
            let isContinuation = false;

            for (const item of items) {
              const chunks = splitSectionItem(item);

              for (const itemClone of chunks) {
                if (!sectionShell) {
                  sectionShell = cloneSectionShell(section, isContinuation);
                  currentPage.appendChild(sectionShell);
                }

                sectionShell.appendChild(itemClone);

                if (!pageOverflows(currentPage)) {
                  continue;
                }

                sectionShell.removeChild(itemClone);

                if (!sectionShell.querySelector(".section-item")) {
                  currentPage.removeChild(sectionShell);
                }

                currentPage = createPage(pagesRoot, header, false);
                isContinuation = true;
                sectionShell = cloneSectionShell(section, isContinuation);
                currentPage.appendChild(sectionShell);
                sectionShell.appendChild(itemClone);

                if (pageOverflows(currentPage)) {
                  currentPage.classList.add("page--oversize");
                }
              }
            }
          }

          if (pagesRoot.children.length) {
            document.body.classList.add("is-paginated");
          }
        }

        async function initializePagination() {
          if (document.fonts && document.fonts.ready) {
            try {
              await document.fonts.ready;
            } catch (error) {
              // Ignore font readiness failures and paginate with available metrics.
            }
          }

          paginateResume();

          let resizeTimer = null;
          window.addEventListener("resize", () => {
            window.clearTimeout(resizeTimer);
            resizeTimer = window.setTimeout(paginateResume, 120);
          });
        }

        window.addEventListener("load", initializePagination);
      })();
""".strip()


def _link(label: Any, url: Any) -> str:
    return f'<a href="{escape(str(url), quote=True)}">{escape(str(label))}</a>'

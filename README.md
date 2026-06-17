# resume-as-code

`resume-as-code` is a zero-dependency resume-as-code CLI. You describe a resume in JSON or a practical YAML subset, and the tool renders a print-ready HTML resume that can be exported to PDF from any browser.

The design goal is the same as IaC or LaTeX:

- Keep resume content declarative.
- Separate structure from presentation.
- Make formatting repeatable.
- Let templates and themes handle the visual polish.

## Current MVP

- `init` generates a starter spec in `json` or `yaml`
- `validate` checks and normalizes a resume spec
- `render` converts a resume spec into a themed HTML document (`--open` to preview in a browser)
- `themes` lists the available built-in themes
- Automatic pagination splits rendered output across letter-sized pages
- Five built-in themes covering general-purpose and dense engineering layouts
- No third-party dependencies

## Themes

| Theme | Density | Typography | Best for |
| --- | --- | --- | --- |
| `classic` | standard | Georgia serif | General-purpose, warm paper feel |
| `slate` | standard | Arial sans | General-purpose, neutral |
| `compact` | tight | Inter / system sans | Long engineering resumes that need to fit more on one page |
| `technical` | dense | Inter body, monospace section headers, left accent rule | Engineering resumes that want a technical look without sacrificing readability |
| `mono` | tight | Fully monospaced, dashed rules | Terminal-aesthetic, minimalist |

Any theme's `accent_color` and `font_family` can be overridden in the spec:

```yaml
theme:
  name: technical
  accent_color: "#1f4f78"
```

## Quick Start

From the repository root, run the module directly without installing:

```bash
PYTHONPATH=src python3 -m resume_as_code init --format yaml
PYTHONPATH=src python3 -m resume_as_code render resume.yaml -o dist/resume.html --open
```

The `--open` flag opens the rendered HTML in your default browser, ready to print to PDF.

If you want the installed command on your shell path:

```bash
python3 -m pip install -e .
resume-as-code render resume.yaml --open
```

## CLI

```bash
resume-as-code init --format yaml --output resume.yaml
resume-as-code validate resume.yaml
resume-as-code themes
resume-as-code render resume.yaml --theme slate --output dist/resume.html --open
```

`validate` also prints non-fatal warnings (for example, a missing contact email or an
overly long summary) so you can catch issues before printing.

## Example Spec

The repository includes:

- `examples/jane-doe.yaml`
- `examples/jane-doe.json`

Schema shape:

```yaml
version: 1
theme:
  name: classic
  accent_color: "#1f4f78"
basics:
  name: Jane Doe
  role: Staff Product Engineer
  email: jane@example.com
  phone: "(555) 555-0100"
  location: Brooklyn, NY
  website: https://janedoe.dev
  summary: Builder focused on developer tools and product systems.
  profiles:
    -
      network: LinkedIn
      username: janedoe
      url: https://linkedin.com/in/janedoe
skills:
  -
    category: Languages
    items:
      - Python
      - TypeScript
experience:
  -
    company: Acme Inc.
    location: Remote
    start: 2022-01
    end: Present
    positions:
      -
        title: Staff Engineer
        start: 2023-07
        end: Present
        highlights:
          - Led platform modernization.
      -
        title: Senior Platform Engineer
        start: 2022-01
        end: 2023-06
education:
  -
    institution: University Name
    degree: B.S. Computer Science
    start: 2014
    end: 2018
```

## YAML Support

To stay dependency-free, the YAML parser intentionally supports a practical subset:

- nested mappings
- lists
- strings, numbers, booleans, and `null`
- quoted strings

This is enough for resume specs. If you need full YAML compatibility later, the parser can be swapped for `PyYAML` without changing the CLI contract.

## Output Strategy

The renderer produces semantic HTML with inline CSS tuned for both screen and print. The simplest PDF flow is:

1. Render to HTML.
2. Open the file in a browser.
3. Print to PDF.

That keeps the tool portable and avoids native PDF dependencies in the first version.

## Repo Layout

```text
resume-as-code/
├── examples/
├── src/resume_as_code/
└── tests/
```

## Next Logical Steps

- add multiple template families
- add Markdown support for long-form summaries
- add direct PDF export behind an optional dependency
- add schema versioning and migrations

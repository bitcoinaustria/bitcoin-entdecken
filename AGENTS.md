# AGENTS.md — Bitcoin entdecken

Open-source brand for "Bitcoin entdecken" events, MIT-licensed — anyone may use it. Bitcoin Austria funds and supports the project; the brand itself belongs to the community. The repo holds brand assets, print/social templates, and LaTeX Beamer presentations that CI builds into release PDFs.

**Direction:** Baselayer workshop materials (Bitcoin Austria's workshop format) will be added to this repo as a new top-level area.

## Language

Everything is **German** (DACH audience): content, `.tex` comments, commit messages, docs. `.tex` files are UTF-8. English appears only in research notes explicitly marked as such.

## Map

| Path | What |
|---|---|
| [README.md](README.md) | Human-facing index — canonical for brand colors (`#FF7700` family), fonts (Poppins), asset locations, release PDF links |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How the community contributes (PR-based, keep it simple) |
| `brand-assets/` | Logos (orange/black/white × SVG/EPS/PNG), design elements, alternative logo concepts |
| `templates/` | Print and event templates (PDF/PSD) — binary artifacts, contributed as-is |
| `slides/` | LaTeX Beamer presentations — has its own scoped [slides/CLAUDE.md](slides/CLAUDE.md) with build/release workflow. Work in there follows that file. |
| `.github/workflows/` | Ground truth for CI: `build-pdf.yml` builds on `.tex` changes, `release.yml` releases on tags `ersteschritte-*`, `missverstaendnisse-*`, `mythen-*` |

## Quality gates

- Brand assets and templates: none — they're design artifacts, reviewed by humans in PRs.
- Slides: `make format` then `make build` from `slides/` must succeed (needs a local LaTeX toolchain; CI is authoritative). Details in [slides/CLAUDE.md](slides/CLAUDE.md).

## Rules

- Commit prefix names the area you touched, matching existing history (e.g. `Missverständnisse:`, `README:`, `CI:`).
- Don't commit built PDFs of the presentations — CI builds and attaches them to releases.
- Facts in slides need working primary-source citations; when updating data (e.g. energy numbers), update the footnote source too.
- Don't invent brand rules: colors and fonts come from README; if a design question isn't answered there, ask rather than extrapolate.

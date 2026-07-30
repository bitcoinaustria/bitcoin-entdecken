# CLAUDE.md — slides/

LaTeX Beamer presentations for "Bitcoin entdecken" events. Three presentations live here, each in a directory whose main `.tex` file carries the directory's name (`erste-schritte/erste-schritte.tex` etc.):

- `erste-schritte/` — Einstieg: Wallet, erste Sats, Sicherheit
- `missverstaendnisse/` — die häufigsten Missverständnisse, faktenbasiert entkräftet
- `mythen/` — Ursprungs-Mythen und was wirklich dahinter steckt

Shared infrastructure: `styles/bitcoin-entdecken.sty` (Beamer style, documented in [styles/BITCOIN-ENTDECKEN-STYLE.md](styles/BITCOIN-ENTDECKEN-STYLE.md)), `makefile` (universal, fuzzy-matches presentations), `screenshot-page.sh`, `generate-images/` (AI image generation — see [generate-images/README.md](generate-images/README.md)).

**Sprache:** Deutsch — Inhalte, `.tex`-Kommentare, neue Texte. UTF-8. Zielgruppe DACH.

## Build (from this directory)

```bash
make format PRESENTATION=<keyword>   # latexindent — run after every .tex edit
make build PRESENTATION=<keyword>    # compile PDF (quiet); MUST pass before you're done
make build-verbose PRESENTATION=<keyword>  # full LaTeX log when build fails
make view / watch / clean / clean-all / help
make screenshot-samples PRESENTATION=<keyword>          # key pages as 150-DPI PNGs
make screenshot-page PAGE=<n> NAME=<desc> PRESENTATION=<keyword>
```

- `PRESENTATION` fuzzy-matches directory names via `.claude/find-presentation.sh` (`miss`, `erste`, `myth` all work). **Default is `erste`** when omitted.
- Workflow after editing `.tex`: `make format`, then `make build`. Screenshots are how you visually verify a slide.
- Requires latexmk/XeLaTeX, inkscape (logo SVG→PDF), latexindent. If unavailable locally, rely on CI.
- Don't commit built PDFs — CI builds them.

## Content conventions

- Use each presentation's slide macro for its list items — e.g. `\misconceptionslide[image.jpg]{Title}{Misconception}{facts items}{Conclusion}`. The image shows on overlay 1 and disappears when facts reveal on overlay 2.
- Item counts (titles like "Die 11 häufigsten …") are generated: a `count-*.sh` script per presentation writes `generated-count.tex`. Never hardcode the number.
- Footnotes on overlay slides: `\footnotemark` in text + `\only<2->{\footnotetext[n]{...}}` — otherwise the footnote shows before its content.
- Every factual claim carries a working primary-source citation; verify URLs when touching them.
- Orange Bitcoin color scheme comes from the style package — don't restyle inline.

## Git & releases

- **Commit prefix** = presentation name, e.g. `Missverständnisse:`, `Erste Schritte:`, `Mythen:`. Only commit when the user asks.
- CI (`../.github/workflows/`): `build-pdf.yml` compiles on pushes touching `.tex`/`makefile`/`.svg`/`pix/**`; `release.yml` creates a GitHub Release with the PDF on tag push. Tag patterns per presentation: `ersteschritte-*`, `missverstaendnisse-*`, `mythen-*`.
- Release: `git tag missverstaendnisse-v1.1 && git push origin missverstaendnisse-v1.1`, then verify at the repo's Actions and Releases pages. `/release` command automates this.

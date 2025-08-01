# CLAUDE.md

This file provides guidance to Claude Code when working with this LaTeX Beamer presentation project about Bitcoin misconceptions in German.

## Project Overview

Bitcoin misconceptions presentation ("Die 11 häufigsten Missverständnisse") - a factual, evidence-based presentation addressing common Bitcoin misunderstandings.

## Git Guidelines

- **Commit Prefix**: "Missverständnisse:"
- **IMPORTANT**: Only commit when explicitly asked by user

## Build Commands

### Essential Workflow
1. **Format**: `make format` - Format LaTeX source with latexindent
2. **Build**: `make build` - Compile PDF with microtype enhancement
3. **View**: `make view` - Open PDF viewer

**WORKFLOW**: After editing tex files, always run `make format` then `make build`

### Additional Commands
- `make clean` - Clean auxiliary files, keep PDF
- `make clean-all` - Clean everything including PDF
- `make watch` - Continuous compilation with file watching
- `make screenshot-samples` - Debug screenshots for key pages
- `make screenshot-page PAGE=X NAME=desc` - Screenshot specific page

## Project Structure

### Main Files
- `2025-missverstaendnisse.tex` - Main presentation source
- `makefile` - Build automation with format/build/screenshot targets
- `logo-bitcoin-entdecken.svg/pdf` - Auto-processed logo
- `misconception-count.tex` - Auto-generated counter (11 misconceptions)
- `count-misconceptions.sh` - Dynamic counter script

### Content Guidelines
- Use `\misconceptionslide` macro for consistency
- German language throughout
- Evidence-based responses with proper citations
- Orange Bitcoin color scheme (#F7931A)

### Misconception Slide Macro
```latex
\misconceptionslide[optional-image.jpg]{Title}{Misconception text}{%
    \item Fact 1
    \item Fact 2
    \item Fact 3
}{Conclusion text}
```

**Image behavior**: Appears on first overlay, disappears when facts are revealed on second overlay.

## Technical Features

### Typography
- **microtype package**: Improved font kerning and spacing with character protrusion
- **latexindent**: Consistent code formatting via `make format`

### Dynamic System
- **Counter**: Automatically counts misconceptions, updates titles
- **Logo processing**: SVG → PDF → cropped PDF when SVG changes
- **Build dependencies**: Proper makefile dependency tracking

### Footnote Management
- Use `\footnotemark` in text + `\only<2->{\footnotetext[n]{...}}` pattern
- Prevents premature footnote visibility in overlay-based slides

## Content Status

### Current Misconceptions (11 total)
1. Umweltauswirkungen (with mining.jpg)
2. Kein intrinsischer Wert (with nichts-intrinsisches.jpg)
3. Volatilität (with volatil.jpg)
4. Regulierung (with verbrecher-2.jpg)
5. Skalierbarkeit (with bitcoin-skalieren.jpg)
6. Spekulationsblase (with blase.jpg)
7. Schneeballsystem (with bitcoin-schneeball.jpg)
8. Kriminalität (with kriminalitaet.jpg)
9. Praktische Adoption (with no-bitcoin-in-shop.png)
10. Bedenken von Zentralbanken (with zentralbank.jpg)
11. Technische Sicherheit (with hacking-2.jpg)

### Verified Sources (All URLs functional)
- Cambridge Centre for Alternative Finance & Mining Report 2025
- 21 Energy (Bitcoin heaters)
- Visa Annual Report 2023
- Sygnum Bank Report 2024
- FINMA Guidance 02/2019
- Chainalysis 2024 Crime Report
- UN Illicit Financial Flows Study
- Blocksize War book (Amazon)
- Wikipedia Greshamsches Gesetz

## Development Notes

### Recent Updates
- **microtype integration**: Enhanced typography with character protrusion
- **latexindent integration**: Consistent code formatting via makefile
- **Citation cleanup**: Removed "not found online" comments
- **URL verification**: All hyperlinks tested and functional

### Key Statistics
- **Final PDF**: 28 pages
- **File size**: ~9MB with images
- **Build time**: ~30 seconds with full compilation
- **Images**: 11 misconception images + title image + logo

## Debug Tools

### Screenshots
- `make screenshot-samples` generates: title, index, M1 misconception/facts, summary, sources
- Manual: `./screenshot-page.sh <page> [name]`
- Output: 150 DPI PNG files in `screenshots/` directory

### Build Verification
- Automatic misconception counting ensures consistent numbering
- Logo auto-processing maintains visual consistency
- microtype warnings are normal and don't affect output quality
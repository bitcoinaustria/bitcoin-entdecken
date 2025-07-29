# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository appears to be focused on Bitcoin-related content, specifically addressing common misunderstandings ("häufige Missverständnisse" in German). The project structure is currently minimal and will be populated as development progresses.

## Current State

The repository is newly initialized with only Claude Code configuration present:
- `.claude/settings.json` - Contains permission settings for Claude Code

## Build Commands

### LaTeX Compilation
- **Build PDF**: `make` or `make build`
- **Clean build files**: `make clean`
- **Full clean**: `make clean-all`
- **View presentation**: `make view`
- **IMPORTANT**: Always commit the generated PDF file (`2025-missverstaendnisse.pdf`) along with source changes
- **After editing tex source files, always run the make compilation** to ensure it still compiles and that a maybe opened pdf viewer updates with the newest pdf

### Logo Management
- **Auto-processing**: SVG logo automatically converted to PDF with cropping when needed
- **Build target**: `make logo-bitcoin-entdecken.pdf` (triggers conversion + cropping)
- **Processing chain**: `logo-bitcoin-entdecken.svg` → temp PDF → cropped PDF
- **Dependencies**: Requires `inkscape` and `pdfcrop` (texlive-extra-utils)

### Style Debugging with Screenshots
For visual verification during development:
- **Take sample screenshots**: `make screenshot-samples`
- **Screenshot specific page**: `make screenshot-page PAGE=4 NAME=environment`
- **Manual screenshot**: `./screenshot-page.sh <page> [name]`

Screenshots are saved in `screenshots/` directory as PNG files with 150 DPI resolution.

## Project Structure

This is a LaTeX Beamer presentation project about Bitcoin misconceptions in German:

### Main Files
- `2025-missverstaendnisse.tex` - Main LaTeX Beamer presentation (renamed from presentation.tex)
- `logo-bitcoin-entdecken.svg` - Bitcoin Entdecken logo (original, white with transparency)
- `logo-bitcoin-entdecken.pdf` - Auto-cropped and converted logo for LaTeX
- `makefile` - Build automation with logo processing and screenshot tools
- `screenshot-page.sh` - Script for taking PDF page screenshots (updated for new filename)
- `.gitignore` - Git ignore file excluding auxiliary files and generated PDFs

### LaTeX Content
- use the `\misconceptionslide` macro for the content slides, for consistency!

### Generated Files
- `2025-missverstaendnisse.pdf` - Final presentation (27 pages)
- `2025-missverstaendnisse.aux/nav/out/toc` - LaTeX auxiliary files (auto-ignored)
- `misconception-count.tex` - Auto-generated counter file for dynamic numbering
- `screenshots/` - Directory containing page screenshots for debugging

## Recent Updates & Development History

### Dynamic Counter System (Latest)
- **Automatic misconception counting**: Bash script `count-misconceptions.sh` counts `\stepcounter{mvnum}` occurrences
- **Build integration**: Makefile runs counter script before LaTeX compilation
- **Dynamic title updates**: Section title automatically shows correct number (e.g., "Die 11 häufigsten Missverständnisse")
- **Generated file**: `misconception-count.tex` contains `\totalmisconceptions` macro
- **Maintenance-free**: Adding/removing misconceptions automatically updates all references

### Layout Improvements (Recent)
- **Header fix**: Removed white border above orange header using `\nointerlineskip` and proper beamer sizing
- **Professional appearance**: Clean edge-to-edge orange header without visual gaps
- **Beamer optimization**: Custom frametitle template with proper margin control

### Content Expansion (Recent)  
- **New misconception**: Added M6 "Schneeballsystem" slide with Weltbank and Finma references
- **Enhanced Skalierbarkeit**: Updated with blockchain trilemma, precise TPS numbers, and Sygnum volume data
- **Current statistics**: Bitcoin 20 trillion $ vs Visa 13 trillion $ transaction volume
- **Academic sources**: Added footnotes to Visa Annual Report 2023 and Sygnum Bank Report 2024

### File Renaming (Previous)
- **All files** renamed from `presentation.*` to `2025-missverstaendnisse.*`
- **Makefile updated** to use new filename throughout
- **Screenshot script updated** with new PDF filename
- **Documentation updated** to reflect new naming scheme
- **Git integration** with proper .gitignore for LaTeX projects

### Logo Optimization & Positioning
- **Auto-cropping**: Logo PDF automatically cropped using `pdfcrop` to remove whitespace
- **Optimal sizing**: Logo sized to `height=3ex` with `keepaspectratio` for perfect title bar fit
- **Smart positioning**: Logo moved from separate headline to integrated frametitle bar
- **Consistent margins**: Both title text and logo use matching `2ex` margins for visual balance

### Visual Layout Improvements
- **Title positioning**: Logo positioned at same height as section titles (right side of frametitle)
- **Margin consistency**: Left title margin matches content spacing, logo uses same right margin
- **Aspect ratio preservation**: Logo automatically maintains proportions while fitting available space

## Presentation Features

### Visual Design
- Orange Bitcoin color scheme (#F7931A) 
- Bitcoin Entdecken logo integrated in title bar (top-right, same height as titles)
- Professional Beamer theme with custom colors and optimal spacing
- Step-by-step slide reveals using overlays

### Content Structure
- Cover 11 main Bitcoin misconceptions (automatically counted)
- Each misconception uses 2-step reveal: Misconception → Facts
- German language content throughout
- Factual responses based on current research
- Dynamic numbering system with automatic counter updates

### Box Styling
- Improved margins and spacing around content blocks
- Equal height columns with proper alignment
- Visual separation between misconception and facts

## Development Guidelines

### Content
- All presentation content should be in German
- Use evidence-based responses to misconceptions
- Maintain consistent orange Bitcoin color scheme

### Style Development
- Test visual changes using `make screenshot-samples`
- Use `make screenshot-page PAGE=X NAME=description` for specific slides
- Screenshots help verify:
  - Box alignment and spacing
  - Logo positioning
  - Color consistency
  - Text readability

### Build Process
- **Automated workflow**: Logo converts from SVG → PDF → cropped PDF when SVG changes
- **Dynamic counting**: `count-misconceptions.sh` automatically updates misconception count before build
- **LaTeX compilation**: Handles all dependencies with latexmk for robust builds
- **Screenshot generation**: 150 DPI PNG files for quality review and debugging
- **Git integration**: repository with proper LaTeX .gitignore patterns
- **File naming**: Consistent `2025-missverstaendnisse.*` naming throughout project

### LaTeX Counter System
- **Counter name**: `mvnum` (short for misconception counter)
- **Usage pattern**: `\stepcounter{mvnum}` before each misconception subsection
- **Reference**: Use `\arabic{mvnum}` in subsection titles and frame titles
- **Automatic title**: Section title uses `\totalmisconceptions` from generated file
- **Build dependency**: `misconception-count.tex` automatically regenerated when source changes

## Key Page Numbers for Screenshots
- Page 1: Title slide
- Page 4-5: Layout of Content on Slides
- 2nd Last Page: Key Learnings Slide
- Last Page: Sources and discussion

## Citation Research & Hyperlinks

### Successfully Found URLs (9/11 sources):
- **Cambridge Centre for Alternative Finance**: https://www.jbs.cam.ac.uk/faculty-research/centres/alternative-finance/
- **Cambridge Digital Mining Industry Report 2025**: https://www.jbs.cam.ac.uk/wp-content/uploads/2025/04/2025-04-cambridge-digital-mining-industry-report.pdf
  - Official PDF report by CCAF at Cambridge Judge Business School (April 2025)
  - Authors: Alexander Neumueller, Gina C. Pieters, Kamiar Mohaddes, Valentin Rousseau, Bryan Zheng Zhang
  - Contains comprehensive Bitcoin mining data (49 firms, 48% of network hashrate)
- **21 Energy**: https://21energy.com/
  - Note: Austrian startup specializing in Bitcoin heaters (not hardware recycling as originally thought)
  - Products: Wall-mounted heaters that mine Bitcoin while providing home heating
- **Visa Inc. Annual Report 2023**: https://s29.q4cdn.com/385744025/files/doc_downloads/2023/Visa-Inc-Fiscal-2023-Annual-Report.pdf
  - Official PDF from Visa's CDN (s29.q4cdn.com)
  - Source for TPS data and transaction volume comparisons
- **Sygnum Bank Future Finance Report 2024**: https://www.sygnum.com/wp-content/uploads/2024/11/Sygnum-Future-Finance-Report-2024-institutional-crypto-market_download.pdf
  - Swiss digital asset bank report containing Bitcoin $20T vs Visa $13T transaction volume data
  - Based on Q3 2024 survey of institutional crypto market trends
- **FINMA Guidance 02/2019**: https://www.finma.ch/~/media/finma/dokumente/dokumentencenter/myfinma/4dokumentation/finma-aufsichtsmitteilungen/20190826-finma-aufsichtsmitteilung-02-2019.pdf?sc_lang=en
  - Note: Corrected from 2018 to 2019 (actual publication date: August 26, 2019)
  - Swiss Financial Market Supervisory Authority guidance on blockchain payments
- **Chainalysis 2024 Crypto Crime Report**: https://go.chainalysis.com/crypto-crime-2024.html
  - Note: Corrected illegal transaction percentage from 0.24% to 0.34% (actual 2023 data)
  - Shows illicit activity decreased from 0.42% (2022) to 0.34% (2023)
- **UN Office on Drugs and Crime**: https://www.unodc.org/documents/data-and-analysis/Studies/Illicit_financial_flows_2011_web.pdf
  - "Estimating illicit financial flows resulting from drug trafficking and other transnational organized crimes" (October 2011)
  - Source for 2-5% of global GDP flowing through illegal channels estimate
  - Key finding: $1.6 trillion (2.7% of GDP) laundered in 2009

### Sources Not Found Online (3/11):
- **Emily Stanhope and Charles Brandt in "Review of Economic Philosophy"**: Academic citation not publicly available
  - Journal exists (ISSN: 1376-0971, published by Vrin via Cairn.info)
  - Authors not found in digital indexes - may be citation error or limited availability
- **World Bank Group "Distributed Ledger Technology and Digital Assets" (2022)**: Specific document not found
  - Multiple related World Bank DLT publications exist from other years
  - May be internal document or different title/date
- **Sopra Banking Software 2024**: Specific German quote not found online
  - Related English content exists about crypto-backed lending
  - Quote may be from internal presentation or restricted publication

### Data Corrections Made:
1. **Chainalysis percentage**: 0.24% → 0.34% (verified from official 2024 report)
2. **FINMA guidance year**: 2018 → 2019 (verified publication date: August 26, 2019)
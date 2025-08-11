# CLAUDE.md

This file provides guidance to Claude Code when working with this LaTeX Beamer presentation project about Bitcoin misconceptions in German.

## Project Overview

Bitcoin misconceptions presentation ("Die 11 häufigsten Missverständnisse") - a factual, evidence-based presentation addressing common Bitcoin misunderstandings.

## Git Guidelines

- **Commit Prefix**: "Missverständnisse:"
- **IMPORTANT**: Only commit when explicitly asked by user

## Build Commands

### GitHub Actions (Automated)
- **PDF Build**: Automatically triggered on push to main when `.tex`, `makefile`, `.svg`, or `pix/**` files change
- **Releases**: Automatically created when pushing tags with pattern `missverstaendnisse-*`
- **PDF**: No longer stored in git - built automatically by GitHub Actions

### Local Development Workflow
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
- `makefile` - Build automation with format/build/screenshot targets (requires inkscape, pdfcrop)
- `logo-bitcoin-entdecken.svg/pdf` - Auto-processed logo
- `misconception-count.tex` - Auto-generated counter (11 misconceptions)
- `count-misconceptions.sh` - Dynamic counter script
- `.github/workflows/` - GitHub Actions for automated PDF builds and releases

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

## Release Process

### Creating a New Release
1. **Automatic Method** (Recommended):
   ```bash
   git tag missverstaendnisse-v1.0
   git push origin missverstaendnisse-v1.0
   ```
   - Tag pattern: `missverstaendnisse-*` (e.g., `missverstaendnisse-v1.0`, `missverstaendnisse-2025-01`)
   - GitHub Actions automatically builds PDF and creates GitHub Release
   - PDF becomes downloadable asset in the release

2. **Manual Verification**:
   - Check GitHub Actions success at: https://github.com/bitcoinaustria/bitcoin-entdecken/actions
   - Verify release created at: https://github.com/bitcoinaustria/bitcoin-entdecken/releases

### GitHub Actions Workflows
- **build-pdf.yml**: Builds PDF on main branch changes to LaTeX files
- **release.yml**: Creates releases on `missverstaendnisse-*` tag pushes
- Both workflows install: LaTeX, inkscape, texlive-font-utils
- Concurrency control prevents multiple simultaneous builds

## Development Notes

### Recent Updates
- **GitHub Actions integration**: Automated PDF builds and releases
- **PDF removed from git**: Now built automatically, not stored in repository
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
## AI Image Generation

### Multi-Provider Support
The script now supports both **Replicate.com** and **fal.ai** APIs with Google's Imagen4 model.

```bash
uv --directory generate-images run generate_image.py [options] "prompt"
```

**API Keys Required:**
- `REPLICATE_API` for Replicate models
- `FAL_AI` for fal.ai models

### Basic Examples
```bash
# Basic generation with Replicate (flux-krea-dev default)
uv --directory generate-images run generate_image.py "cybercriminal with bitcoin symbols"

# Generate with Google Imagen4 via fal.ai
uv --directory generate-images run generate_image.py -m imagen4 "bitcoin logo in cyberpunk style"

# Force specific provider
uv --directory generate-images run generate_image.py -p fal -m imagen4 "crypto hacker scene"

# List all available models from both providers
uv --directory generate-images run generate_image.py --list-models
```

### Advanced Features
```bash
# Replace specific slide image (M8 = Kriminalität) with Imagen4
uv --directory generate-images run generate_image.py -m imagen4 -r M8 -n kriminalitaet-neu "cybercriminal silhouette"

# Multiple images with fal.ai (generates 1-4 images)
uv --directory generate-images run generate_image.py -m imagen4 --num-images 3 "bitcoin mining facility"

# Use negative prompts (fal.ai only)
uv --directory generate-images run generate_image.py -m imagen4 --negative-prompt "ugly, blurry" "clean bitcoin symbol"

# Reproducible generation with seed
uv --directory generate-images run generate_image.py -m imagen4 --seed 42 "bitcoin conference crowd"

# Image editing with flux-kontext-pro (with auto-replace)
uv --directory generate-images run generate_image.py -m flux-kontext-pro -i pix/existing.jpg -r M8 -y "make more abstract"
```

### Available Models

**Replicate Models:**
- flux-krea-dev (default)
- flux-kontext-pro (requires input image)
- flux-pro, flux-dev, sdxl

**fal.ai Models:**
- imagen4 (Google's Imagen4)
- imagen4-turbo (faster variant)

**Provider Auto-Detection:** Use `-p auto` (default) to automatically select the right provider based on the model chosen.

### Metadata Tracking

Every generated image is automatically accompanied by a JSON metadata file with the same basename:

```
generated-20250111_153000.jpg       # The generated image
generated-20250111_153000.json      # Metadata with generation parameters
```

**Metadata includes:**
- Original prompt and generation timestamp
- Provider and model used
- All generation parameters (aspect ratio, seed, negative prompt, etc.)
- Slide replacement information (if applicable)
- Input image path (for editing workflows)

**Example metadata:**
```json
{
  "prompt": "cybercriminal with bitcoin symbols",
  "time": "2025-01-11T15:30:00.123456",
  "provider": "fal",
  "model": "imagen4",
  "aspect_ratio": "1:1",
  "negative_prompt": "ugly, blurry",
  "seed": 42,
  "slide_replacement": {
    "slide": "M8",
    "description": "Kriminalität",
    "original_image": "pix/kriminalitaet.jpg"
  }
}
```
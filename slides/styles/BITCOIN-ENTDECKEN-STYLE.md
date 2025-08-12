# Bitcoin Entdecken Style Package

The `bitcoin-entdecken.sty` package provides consistent styling and macros for Bitcoin presentations created by Bitcoin Entdecken / Bitcoin Austria.

## Features

- **Bitcoin Brand Colors**: Predefined Bitcoin orange theme with consistent color scheme
- **Metropolis Integration**: Works seamlessly with the Metropolis Beamer theme
- **Custom Layouts**: Specialized slide layouts for misconception presentations
- **Logo Integration**: Automatic Bitcoin Entdecken logo placement in frame titles
- **Rounded Images**: Support for rounded corner images with aspect ratio control
- **Typography Enhancement**: Microtype integration for better text rendering

## Installation

1. Place `bitcoin-entdecken.sty` in your LaTeX document directory
2. Load the Metropolis theme before importing the style package:

```latex
\documentclass[aspectratio=169,t,9pt]{beamer}
\usetheme[progressbar=foot]{metropolis}
\usepackage{bitcoin-entdecken}
```

## Basic Usage

### Minimal Example

```latex
\documentclass[aspectratio=169,t,9pt]{beamer}

% Load Metropolis theme first
\usetheme[progressbar=foot]{metropolis}

% Load Bitcoin Entdecken style
\usepackage{bitcoin-entdecken}

% Setup title using style helpers
\bitcointitle{Your Presentation Title}{Your Subtitle}
\bitcointitlegraphic{path/to/your/image.jpg}

\begin{document}

% Title slide
\begin{frame}
    \titlepage
\end{frame}

% Regular content slides
\begin{frame}{Your Frame Title}
    Your content here...
\end{frame}

\end{document}
```

## Advanced Features

### Misconception Slides

The package provides a specialized macro for creating consistent misconception slides:

```latex
\misconceptionslide[optional-image.jpg]{Title}{Misconception text}{%
    \item Fact 1
    \item Fact 2
    \item Fact 3
}{Conclusion text}
```

**Parameters:**
- `[optional-image.jpg]` - Optional image displayed on first overlay
- `{Title}` - Frame title (automatically numbered as M1, M2, etc.)
- `{Misconception text}` - The misconception statement in quotes
- `{Facts}` - List items refuting the misconception
- `{Conclusion}` - Final conclusion text

**Example:**

```latex
\misconceptionslide[pix/mining.jpg]{Umweltauswirkungen}{Bitcoin-Mining verbraucht zu viel Energie}{%
    \item Nur 0,54\% des globalen Stromverbrauchs
    \item Über 50\% erneuerbare Energiequellen
    \item Effizienz steigt kontinuierlich
}{Mining wird immer umweltfreundlicher.}
```

### Rounded Images

Create rounded corner images with aspect ratio support:

```latex
\roundedimage{path/to/image.jpg}{0.4\textwidth}{1}
```

**Parameters:**
- `{path}` - Image file path
- `{width}` - Image width (e.g., `0.4\textwidth`)
- `{ratio}` - Aspect ratio: `1` for 1:1, `2` for 2:1

### Title Setup Helpers

Simplified title configuration:

```latex
% Set main title and subtitle
\bitcointitle{Main Title}{Subtitle}

% Set title graphic
\bitcointitlegraphic{path/to/title-image.jpg}
```

## Color Scheme

The package defines Bitcoin brand colors:

- `bitcoinorange` - RGB(247,147,26) - Primary Bitcoin orange
- `bitcoindark` - RGB(33,33,33) - Dark gray for contrast
- `bitcoinlight` - RGB(255,255,255) - Pure white

Use in your content:
```latex
\textcolor{bitcoinorange}{Orange text}
\colorbox{bitcoindark}{\color{bitcoinlight}White text on dark background}
```

## Requirements

### Dependencies
The style package automatically loads these packages:
- `inputenc` (UTF-8 support)
- `xcolor` (Color support)
- `graphicx` (Graphics support)
- `tikz` with `calc` library (Drawing support)
- `amsmath`, `amsfonts` (Math support)
- `booktabs` (Table support)
- `microtype` (Typography enhancement)

### Logo File
Ensure you have `logo-bitcoin-entdecken.pdf` in the root slides directory for automatic logo placement.

### Theme Compatibility
- **Required**: Metropolis Beamer theme must be loaded before the style package
- **Recommended**: Use with `aspectratio=169` for 16:9 presentations

## Customization

### Frame Layout
The package removes default Beamer margins and provides:
- Custom frame title template with logo integration
- Custom footer with frame numbers only
- No text margins for full-width content

### Typography
- Microtype enhancement for better character protrusion
- Tiny footnote font size
- Consistent font handling across elements

## File Structure Example

```
slides/                              # Root directory
├── logo-bitcoin-entdecken.pdf       # Shared logo (auto-generated)
├── styles/
│   └── bitcoin-entdecken.sty        # Style package
└── your-presentation/
    ├── your-presentation.tex         # Main LaTeX file
    └── pix/
        ├── image1.jpg
        ├── image2.jpg
        └── title-image.jpg
```

## Migration from Standalone Implementation

If migrating from a presentation with embedded customizations:

1. **Remove duplicate code** from your `.tex` file:
   - Color definitions
   - Theme customizations
   - Custom macros
   - Package imports

2. **Replace with style package**:
   ```latex
   \usepackage{bitcoin-entdecken}
   ```

3. **Update title setup**:
   ```latex
   % Old way
   \title[Short]{Long Title}
   \subtitle{Subtitle}
   \titlegraphic{...}
   
   % New way
   \bitcointitle{Long Title}{Subtitle}
   \bitcointitlegraphic{path/to/image.jpg}
   ```

4. **Keep content unchanged** - all `\misconceptionslide` calls work as before

## License

[MIT-Lizenz](https://opensource.org/licenses/MIT)

## Support

For issues or contributions, contact Bitcoin Entdecken / Bitcoin Austria.
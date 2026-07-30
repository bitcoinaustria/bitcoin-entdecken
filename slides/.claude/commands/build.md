---
description: Build the LaTeX presentation (format + build)
---

Format and build the LaTeX presentation following the project workflow:

1. Find presentation directory using fuzzy matching
2. Run `make format` to format the LaTeX source with latexindent  
3. Run `make build` to compile the PDF with microtype enhancement

Usage: `/build <keyword>` (e.g. `/build miss` for missverstaendnisse)

!bash
if [ -n "$ARGUMENTS" ]; then
    echo "Building presentation matching: $ARGUMENTS"
    make format PRESENTATION="$ARGUMENTS" && make build PRESENTATION="$ARGUMENTS"
else
    echo "Usage: /build <keyword>"
    echo "Available presentations:"
    ./.claude/find-presentation.sh 2>&1 || true
fi
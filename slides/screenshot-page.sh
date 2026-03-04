#!/bin/bash

# Script to take a screenshot of a specific PDF page
# Usage: ./screenshot-page.sh <pdf_file> <page_number> [output_name]

if [ $# -lt 2 ]; then
    echo "Usage: $0 <pdf_file> <page_number> [output_name]"
    echo "Example: $0 missverstaendnisse/missverstaendnisse.pdf 4 environment_slide"
    echo "         $0 missverstaendnisse/missverstaendnisse.pdf 6 volatility_slide"
    exit 1
fi

PDF_FILE=$1
PAGE_NUMBER=$2
OUTPUT_NAME=${3:-page_${PAGE_NUMBER}}
OUTPUT_FILE="screenshots/${OUTPUT_NAME}.png"

# Create screenshots directory if it doesn't exist
mkdir -p screenshots

# Check if PDF exists
if [ ! -f "$PDF_FILE" ]; then
    echo "Error: $PDF_FILE not found. Run 'make' first to build the presentation."
    exit 1
fi

# Get total pages to validate input
TOTAL_PAGES=$(pdftk "$PDF_FILE" dump_data | grep NumberOfPages | cut -d' ' -f2 2>/dev/null || echo "unknown")
if [ "$TOTAL_PAGES" != "unknown" ] && [ "$PAGE_NUMBER" -gt "$TOTAL_PAGES" ]; then
    echo "Error: Page $PAGE_NUMBER exceeds total pages ($TOTAL_PAGES)"
    exit 1
fi

# Convert specific page to PNG with high resolution
echo "Taking screenshot of page $PAGE_NUMBER..."
pdftoppm -png -f "$PAGE_NUMBER" -l "$PAGE_NUMBER" -r 150 "$PDF_FILE" "screenshots/temp"

# Rename the output file (pdftoppm adds page numbers)
if [ -f "screenshots/temp-$(printf "%02d" $PAGE_NUMBER).png" ]; then
    mv "screenshots/temp-$(printf "%02d" $PAGE_NUMBER).png" "$OUTPUT_FILE"
    echo "Screenshot saved: $OUTPUT_FILE"
    
    # Show image info
    if command -v identify >/dev/null 2>&1; then
        echo "Image info:"
        identify "$OUTPUT_FILE"
    fi
    
    # Note: Auto-opening disabled to prevent popup windows
    # To view: xdg-open "$OUTPUT_FILE"
else
    echo "Error: Failed to generate screenshot"
    exit 1
fi
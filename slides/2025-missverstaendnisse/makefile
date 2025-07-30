# Makefile for Bitcoin Misconceptions Presentation
# 
# This Makefile provides convenient commands to build and manage
# the LaTeX Beamer presentation about Bitcoin misconceptions.

.PHONY: all build clean clean-all view help screenshot-samples

# Default target
all: build

# Convert SVG logo to PDF and crop to content (only if SVG is newer)
logo-bitcoin-entdecken.pdf: logo-bitcoin-entdecken.svg
	@echo "Converting SVG logo to PDF..."
	inkscape --export-type=pdf --export-filename=logo-bitcoin-entdecken-temp.pdf logo-bitcoin-entdecken.svg
	@echo "Cropping PDF to content..."
	pdfcrop logo-bitcoin-entdecken-temp.pdf logo-bitcoin-entdecken.pdf
	@rm -f logo-bitcoin-entdecken-temp.pdf
	@echo "Logo processed: cropped and ready for use"

# Count misconceptions and generate macro file
misconception-count.tex: 2025-missverstaendnisse.tex count-misconceptions.sh
	@echo "Counting misconceptions..."
	./count-misconceptions.sh

# Build the presentation PDF
build: logo-bitcoin-entdecken.pdf misconception-count.tex
	@echo "Building presentation..."
	latexmk -xelatex -f -interaction=nonstopmode -pdf 2025-missverstaendnisse.tex
	@echo "Build complete: 2025-missverstaendnisse.pdf"

# Clean auxiliary files but keep the PDF
clean:
	@echo "Cleaning auxiliary files..."
	latexmk -c 2025-missverstaendnisse.tex
	@echo "Removing additional LaTeX files..."
	@rm -f 2025-missverstaendnisse.nav 2025-missverstaendnisse.snm 2025-missverstaendnisse.vrb
	@echo "Removing generated count file..."
	@rm -f misconception-count.tex
	@echo "Removing screenshots..."
	@rm -rf screenshots/
	@echo "Clean complete"

# Clean everything including the PDF
clean-all:
	@echo "Cleaning all generated files..."
	latexmk -C 2025-missverstaendnisse.tex
	@echo "Deep clean complete"

# View the PDF (requires a PDF viewer)
view: build
	@echo "Opening 2025-missverstaendnisse.pdf..."
	@if command -v xdg-open > /dev/null 2>&1; then \
		xdg-open 2025-missverstaendnisse.pdf; \
	elif command -v open > /dev/null 2>&1; then \
		open 2025-missverstaendnisse.pdf; \
	else \
		echo "No PDF viewer found. Please open 2025-missverstaendnisse.pdf manually."; \
	fi

# Take screenshots of specific slides for style debugging
screenshots/%.png: 2025-missverstaendnisse.pdf screenshot-page.sh
	@echo "Taking screenshot of slide..."
	./screenshot-page.sh $(word 2,$(subst _, ,$*)) $(word 1,$(subst _, ,$*))

# Take sample screenshots for style verification
screenshot-samples: build screenshot-page.sh
	@echo "Taking sample screenshots for style verification..."
	@mkdir -p screenshots
	@TOTAL_PAGES=$$(pdftk "2025-missverstaendnisse.pdf" dump_data | grep NumberOfPages | cut -d' ' -f2 2>/dev/null || echo "27"); \
	echo "Total pages: $$TOTAL_PAGES"; \
	./screenshot-page.sh 1 title; \
	./screenshot-page.sh 2 index; \
	./screenshot-page.sh 5 M1_misconception; \
	./screenshot-page.sh 6 M1_facts; \
	./screenshot-page.sh $$(($$TOTAL_PAGES - 1)) summary; \
	./screenshot-page.sh $$TOTAL_PAGES sources
	@echo "Sample screenshots saved in screenshots/ directory"
	@echo "Use 'make screenshot-page PAGE=X NAME=name' for specific pages"

# Screenshot a specific page
screenshot-page: build screenshot-page.sh
	@if [ -z "$(PAGE)" ]; then \
		echo "Error: Please specify PAGE number. Example: make screenshot-page PAGE=4 NAME=environment"; \
	else \
		./screenshot-page.sh $(PAGE) $(if $(NAME),$(NAME),page_$(PAGE)); \
	fi

# Show help
help:
	@echo "Available commands:"
	@echo "  make              - Build the presentation (default)"
	@echo "  make build        - Build the presentation PDF"
	@echo "  make clean        - Clean auxiliary files, keep PDF"
	@echo "  make clean-all    - Clean all generated files including PDF"
	@echo "  make view         - Build and view the presentation"
	@echo "  make screenshot-samples - Take sample screenshots for debugging"
	@echo "  make screenshot-page PAGE=X NAME=name - Screenshot specific page"
	@echo "  make help         - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make screenshot-page PAGE=4 NAME=environment"
	@echo "  make screenshot-page PAGE=6 NAME=volatility"

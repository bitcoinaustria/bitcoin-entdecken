# Universal Makefile for Bitcoin Entdecken Presentations
# 
# This Makefile works with any presentation following the pattern:
# ./[name]/[name].tex (e.g., ./missverstaendnisse/missverstaendnisse.tex)
#
# Usage: make [target] PRESENTATION=keyword
# The keyword is fuzzy-matched using .claude/find-presentation.sh

.PHONY: all build build-verbose clean clean-all view help screenshot-samples watch watch-quiet format

# Default presentation (if not specified)
ifndef PRESENTATION
    PRESENTATION := erste
endif

# Find presentation directory using fuzzy matching
PRES_DIR := $(shell ./.claude/find-presentation.sh $(PRESENTATION) 2>/dev/null)
PRES_NAME := $(notdir $(PRES_DIR))
TEX_FILE := $(PRES_DIR)/$(PRES_NAME).tex
PDF_FILE := $(PRES_DIR)/$(PRES_NAME).pdf

# Verify presentation was found
ifeq ($(PRES_DIR),)
    $(error No presentation found matching '$(PRESENTATION)'. Run './.claude/find-presentation.sh' to see available presentations)
endif

# Default target
all: build

# Convert SVG logo to PDF and crop to content (only if SVG is newer)
logo-bitcoin-entdecken.pdf: logo-bitcoin-entdecken.svg
	@echo "Converting SVG logo to PDF..."
	@inkscape --export-type=pdf --export-filename=logo-bitcoin-entdecken-temp.pdf logo-bitcoin-entdecken.svg
	@echo "Cropping PDF to content..."
	@pdfcrop logo-bitcoin-entdecken-temp.pdf logo-bitcoin-entdecken.pdf
	@rm -f logo-bitcoin-entdecken-temp.pdf
	@echo "Logo processed: cropped and ready for use"

# Handle presentation-specific generated files (e.g., misconception-count.tex)
# Discovers any count-*.sh script in the presentation directory
COUNT_SCRIPT := $(firstword $(wildcard $(PRES_DIR)/count-*.sh))

$(PRES_DIR)/generated-count.tex: $(TEX_FILE)
	@if [ -n "$(COUNT_SCRIPT)" ]; then \
		echo "Counting content in $(PRES_DIR)..."; \
		cd $(PRES_DIR) && ./$(notdir $(COUNT_SCRIPT)); \
	else \
		echo "No count script found, skipping content counting"; \
		touch $(PRES_DIR)/generated-count.tex; \
	fi

# Build the presentation PDF
build: logo-bitcoin-entdecken.pdf $(PRES_DIR)/generated-count.tex
	@echo "Building $(PRES_NAME) presentation..."
	@cd $(PRES_DIR) && latexmk -xelatex -f -interaction=nonstopmode -silent -pdf $(PRES_NAME).tex || true
	@test -f $(PDF_FILE) || (echo "Build failed. PDF file not created. Run 'make build-verbose PRESENTATION=$(PRESENTATION)' for details." && exit 1)
	@echo "Build complete: $(PDF_FILE)"

# Build with full output for debugging
build-verbose: logo-bitcoin-entdecken.pdf $(PRES_DIR)/generated-count.tex
	@echo "Building $(PRES_NAME) presentation (verbose)..."
	@cd $(PRES_DIR) && latexmk -xelatex -f -interaction=nonstopmode -pdf $(PRES_NAME).tex
	@echo "Build complete: $(PDF_FILE)"

# Clean auxiliary files but keep the PDF
clean:
	@echo "Cleaning auxiliary files in $(PRES_DIR)..."
	@cd $(PRES_DIR) && latexmk -c $(PRES_NAME).tex
	@echo "Removing additional LaTeX files..."
	@cd $(PRES_DIR) && rm -f $(PRES_NAME).nav $(PRES_NAME).snm $(PRES_NAME).vrb
	@echo "Removing generated files..."
	@cd $(PRES_DIR) && rm -f *-count.tex generated-count.tex *.aux *.fdb_latexmk
	@echo "Removing screenshots..."
	@cd $(PRES_DIR) && rm -rf screenshots/
	@echo "Removing latexindent temporary files..."
	@cd $(PRES_DIR) && rm -rf .latexindent-tmp/
	@echo "Clean complete for $(PRES_NAME)"

# Clean everything including the PDF
clean-all:
	@echo "Cleaning all generated files in $(PRES_DIR)..."
	@cd $(PRES_DIR) && latexmk -C $(PRES_NAME).tex
	@echo "Deep clean complete for $(PRES_NAME)"

# View the PDF (requires a PDF viewer)
view: build
	@echo "Opening $(PDF_FILE)..."
	@if command -v xdg-open > /dev/null 2>&1; then \
		xdg-open $(PDF_FILE); \
	elif command -v open > /dev/null 2>&1; then \
		open $(PDF_FILE); \
	else \
		echo "No PDF viewer found. Please open $(PDF_FILE) manually."; \
	fi

# Take sample screenshots for style verification
screenshot-samples: build
	@echo "Taking sample screenshots for $(PRES_NAME)..."
	@cd $(PRES_DIR) && mkdir -p screenshots
	@cd $(PRES_DIR) && TOTAL_PAGES=$$(pdftk "$(PRES_NAME).pdf" dump_data | grep NumberOfPages | cut -d' ' -f2 2>/dev/null || echo "27"); \
	echo "Total pages: $$TOTAL_PAGES"; \
	../screenshot-page.sh $(PRES_NAME).pdf 1 title; \
	../screenshot-page.sh $(PRES_NAME).pdf 2 index; \
	../screenshot-page.sh $(PRES_NAME).pdf 5 slide_1; \
	../screenshot-page.sh $(PRES_NAME).pdf 6 slide_2; \
	../screenshot-page.sh $(PRES_NAME).pdf $$(($$TOTAL_PAGES - 1)) summary; \
	../screenshot-page.sh $(PRES_NAME).pdf $$TOTAL_PAGES sources
	@echo "Sample screenshots saved in $(PRES_DIR)/screenshots/ directory"

# Screenshot a specific page
screenshot-page: build
	@if [ -z "$(PAGE)" ]; then \
		echo "Error: Please specify PAGE number. Example: make screenshot-page PAGE=4 NAME=environment PRESENTATION=$(PRESENTATION)"; \
	else \
		cd $(PRES_DIR) && ../screenshot-page.sh $(PRES_NAME).pdf $(PAGE) $(if $(NAME),$(NAME),page_$(PAGE)); \
	fi

# Format LaTeX source file
format:
	@echo "Formatting $(TEX_FILE)..."
	@cd $(PRES_DIR) && mkdir -p .latexindent-tmp
	@cd $(PRES_DIR) && latexindent -w -c .latexindent-tmp $(PRES_NAME).tex > /dev/null 2>&1 || (echo "Formatting failed. Check LaTeX syntax." && exit 1)
	@echo "LaTeX source formatted for $(PRES_NAME)"

# Watch for changes and rebuild automatically
watch: logo-bitcoin-entdecken.pdf $(PRES_DIR)/generated-count.tex
	@echo "Starting continuous compilation for $(PRES_NAME)..."
	@echo "Press Ctrl+C to stop watching"
	@cd $(PRES_DIR) && latexmk -xelatex -f -interaction=nonstopmode -pdf -pvc $(PRES_NAME).tex

# Watch for changes and rebuild automatically (quiet)
watch-quiet: logo-bitcoin-entdecken.pdf $(PRES_DIR)/generated-count.tex
	@echo "Starting quiet continuous compilation for $(PRES_NAME)..."
	@echo "Press Ctrl+C to stop watching"
	@cd $(PRES_DIR) && latexmk -xelatex -f -interaction=batchmode -silent -pdf -pvc $(PRES_NAME).tex

# Show help
help:
	@echo "Universal Bitcoin Entdecken Presentation Makefile"
	@echo ""
	@echo "Usage: make [target] PRESENTATION=keyword"
	@echo "The keyword is fuzzy-matched to find presentation directories."
	@echo ""
	@echo "Available presentations:"
	@./.claude/find-presentation.sh 2>&1 || true
	@echo ""
	@echo "Available commands:"
	@echo "  make [PRESENTATION=key]    - Build presentation (default: miss)"
	@echo "  make build [PRESENTATION=key] - Build presentation PDF (quiet)"
	@echo "  make build-verbose [PRESENTATION=key] - Build with full LaTeX output"
	@echo "  make format [PRESENTATION=key] - Format LaTeX source"
	@echo "  make clean [PRESENTATION=key] - Clean auxiliary files, keep PDF"
	@echo "  make clean-all [PRESENTATION=key] - Clean all files including PDF"
	@echo "  make view [PRESENTATION=key] - Build and view presentation"
	@echo "  make watch [PRESENTATION=key] - Watch and rebuild (verbose)"
	@echo "  make watch-quiet [PRESENTATION=key] - Watch and rebuild (quiet)"
	@echo "  make screenshot-samples [PRESENTATION=key] - Sample screenshots"
	@echo "  make screenshot-page PAGE=X NAME=name [PRESENTATION=key] - Specific screenshot"
	@echo "  make help - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make PRESENTATION=miss"
	@echo "  make build PRESENTATION=2025"
	@echo "  make screenshot-page PAGE=4 NAME=environment PRESENTATION=miss"
	@echo ""
	@echo "Current target: $(PRES_NAME) ($(PRES_DIR))"
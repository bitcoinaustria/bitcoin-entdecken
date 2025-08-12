#!/bin/bash
# Find a presentation directory by a fuzzy keyword.

# The first argument is the keyword to search for.
KEYWORD=$1

# If no keyword is provided, list all available presentation directories.
if [ -z "$KEYWORD" ]; then
    echo "Usage: ./find-presentation.sh <keyword>" >&2
    echo "Available presentations:" >&2
    find . -maxdepth 1 -type d -not -path '*/.*' -not -name 'styles' -not -name 'generate-images' | sed 's|./||' >&2
    exit 1
fi

# Find the first directory that matches the keyword.
# Exclude common/shared directories.
TARGET_DIR=$(find . -maxdepth 1 -type d -name "*$KEYWORD*" \
    -not -path '*/.*' \
    -not -name 'styles' \
    -not -name 'generate-images' \
    | head -n 1)

# Check if a directory was found.
if [ -z "$TARGET_DIR" ]; then
    echo "Error: No presentation directory found matching '$KEYWORD'." >&2
    exit 1
else
    # Print the cleaned-up directory path.
    echo "$TARGET_DIR" | sed 's|./||'
fi

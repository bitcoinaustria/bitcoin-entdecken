---
description: Create and push a new release tag (triggers GitHub Actions)
---

Create a new release tag and push it to trigger GitHub Actions automated PDF build and release creation.

Usage: `/release <presentation> <type>`
- `<presentation>`: Presentation keyword (e.g., `miss`, `erste`, `2025`)
- `<type>`: `major` or `minor`

Examples:
- `/release erste minor` - Create minor release for erste-schritte
- `/release miss major` - Create major release for missverstaendnisse

Note: We use simple [major].[minor] versioning only (no patch numbers) to keep it clean.

The command will:
1. Find the presentation directory using fuzzy matching
2. Find the latest tag matching `<presentation>-v*`
3. Parse the version and increment appropriately
4. Create and push the new tag
5. GitHub Actions builds PDF and creates release automatically

!bash -c '
# Parse arguments: presentation and type
echo "ARGUMENTS received: [${ARGUMENTS}]"
ARG1=$(echo "${ARGUMENTS}" | cut -d" " -f1 | xargs)
ARG2=$(echo "${ARGUMENTS}" | cut -d" " -f2 | xargs)

# Validate arguments
if [ -z "$ARG1" ] || [ -z "$ARG2" ]; then
  echo "Usage: /release <presentation> <type>"
  echo "Examples: /release erste minor, /release miss major"
  exit 1
fi

PRESENTATION_KEY="$ARG1"
RELEASE_TYPE="$ARG2"

echo "Presentation: $PRESENTATION_KEY, Type: $RELEASE_TYPE"

# Find presentation directory using fuzzy matching
PRESENTATION_DIR=""
for dir in */; do
  if echo "$dir" | grep -i "$PRESENTATION_KEY" > /dev/null; then
    PRESENTATION_DIR=$(basename "$dir")
    break
  fi
done

if [ -z "$PRESENTATION_DIR" ]; then
  echo "✗ No presentation found matching: $PRESENTATION_KEY"
  echo "Available presentations:"
  ls -d */ | sed "s|/||"
  exit 1
fi

echo "Found presentation: $PRESENTATION_DIR"

# Find latest tag for this presentation
# First try to find existing tags by searching for common patterns
POSSIBLE_PREFIXES="$PRESENTATION_DIR $(echo $PRESENTATION_DIR | sed 's/-//g') $(echo $PRESENTATION_KEY)"
TAG_PREFIX=""
latest=""

for prefix in $POSSIBLE_PREFIXES; do
  existing_tags=$(git tag -l "$prefix-v*" | sort -V)
  if [ -n "$existing_tags" ]; then
    TAG_PREFIX="$prefix"
    latest=$(echo "$existing_tags" | tail -1 | sed "s/$prefix-v//")
    echo "Found existing tags with prefix: $TAG_PREFIX"
    break
  fi
done

# If no existing tags found, use directory name as prefix
if [ -z "$TAG_PREFIX" ]; then
  TAG_PREFIX="$PRESENTATION_DIR"
  echo "No existing tags found, using directory name: $TAG_PREFIX"
fi

echo "Latest version for $TAG_PREFIX: $latest"

# Calculate new version
if [ -z "$latest" ]; then
  new_version="v1.0"
else
  major=$(echo $latest | cut -d. -f1 | sed "s/v//")
  minor=$(echo $latest | cut -d. -f2)
  
  if [ "$RELEASE_TYPE" = "major" ]; then
    new_version="v$((major + 1)).0"
  elif [ "$RELEASE_TYPE" = "minor" ]; then
    new_version="v${major}.$((minor + 1))"
  else
    echo "Usage: /release <presentation> major|minor (got: $RELEASE_TYPE)"; exit 1
  fi
fi

NEW_TAG="$TAG_PREFIX-$new_version"
echo "Creating release: $NEW_TAG (from $latest)"

# Create the tag
if git tag "$NEW_TAG"; then
  echo "✓ Tag created successfully: $NEW_TAG"
else
  echo "✗ Failed to create tag"
  exit 1
fi

# Push the tag
if git push origin "$NEW_TAG"; then
  echo "✓ Tag pushed successfully to origin"
  echo "🚀 GitHub Actions should now build PDF and create release for $PRESENTATION_DIR"
else
  echo "✗ Failed to push tag"
  exit 1
fi
'
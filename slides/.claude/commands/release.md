---
description: Create and push a new release tag (triggers GitHub Actions)
---

Create a new release tag and push it to trigger GitHub Actions automated PDF build and release creation.

Usage: `/release major` or `/release minor`
- `major`: Increment major version (e.g., v1.2 → v2.0)
- `minor`: Increment minor version (e.g., v1.2 → v1.3)

Note: We use simple [major].[minor] versioning only (no patch numbers) to keep it clean.

The command will:
1. Find the latest tag matching `missverstaendnisse-v*`
2. Parse the version and increment appropriately
3. Create and push the new tag
4. GitHub Actions builds PDF and creates release automatically

!bash -c '
# Debug: show what ARGUMENTS contains
echo "ARGUMENTS received: [${ARGUMENTS}]"

# Clean up ARGUMENTS (trim whitespace and handle empty)
ARG=$(echo "${ARGUMENTS}" | xargs)
if [ -z "$ARG" ]; then
  ARG="minor"
fi

echo "Using argument: $ARG"

latest=$(git tag -l "missverstaendnisse-v*" | sort -V | tail -1 | sed "s/missverstaendnisse-v//")
echo "Latest version: $latest"

if [ -z "$latest" ]; then
  new_version="v1.0"
else
  major=$(echo $latest | cut -d. -f1 | sed "s/v//")
  minor=$(echo $latest | cut -d. -f2)
  
  if [ "$ARG" = "major" ]; then
    new_version="v$((major + 1)).0"
  elif [ "$ARG" = "minor" ]; then
    new_version="v${major}.$((minor + 1))"
  else
    echo "Usage: /release major|minor (got: $ARG)"; exit 1
  fi
fi

echo "Creating release: missverstaendnisse-$new_version (from $latest)"

# Create the tag
if git tag "missverstaendnisse-$new_version"; then
  echo "✓ Tag created successfully: missverstaendnisse-$new_version"
else
  echo "✗ Failed to create tag"
  exit 1
fi

# Push the tag
if git push origin "missverstaendnisse-$new_version"; then
  echo "✓ Tag pushed successfully to origin"
  echo "🚀 GitHub Actions should now build PDF and create release"
else
  echo "✗ Failed to push tag"
  exit 1
fi
'
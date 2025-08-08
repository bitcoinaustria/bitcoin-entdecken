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
latest=$(git tag -l "missverstaendnisse-v*" | sort -V | tail -1 | sed "s/missverstaendnisse-v//")
if [ -z "$latest" ]; then
  new_version="v1.0"
else
  major=$(echo $latest | cut -d. -f1 | sed "s/v//")
  minor=$(echo $latest | cut -d. -f2)
  if [ "$ARGUMENTS" = "major" ]; then
    new_version="v$((major + 1)).0"
  elif [ "$ARGUMENTS" = "minor" ]; then
    new_version="v${major}.$((minor + 1))"
  else
    echo "Usage: /release major|minor"; exit 1
  fi
fi
echo "Creating release: missverstaendnisse-$new_version (from $latest)"
git tag "missverstaendnisse-$new_version" && git push origin "missverstaendnisse-$new_version"
'
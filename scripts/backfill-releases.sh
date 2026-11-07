#!/usr/bin/env bash
# Backfill git tags and GitHub Releases for versions 0.1.1 to 0.11.0, which
# shipped before release-please managed releases.
#
# Each version is tagged on the first commit of main's first-parent history
# whose .claude-plugin/plugin.json carries that version (the merge commit of
# the pull request that shipped it). Release notes are the version's paragraph
# in migrations/README.md, plus a link to its migration file.
#
# Dry run by default: it only prints what it would do. Run it from a clone of
# the repository with `gh` signed in as a maintainer.
#
#   scripts/backfill-releases.sh                   # dry run
#   scripts/backfill-releases.sh --apply           # create tags and releases
#   scripts/backfill-releases.sh --apply --delete-old-tag
#                                                  # also delete the old tag
#                                                  # ceo-of-agents--v0.1.1
#
# Safe to run again: existing releases are skipped, and an existing tag is
# reused only if it points to the expected commit.
set -euo pipefail

REPO="iamgiolaga/ceo-of-agents"
OLD_TAG="ceo-of-agents--v0.1.1"

# version  commit (merge commit on main)              pull request
VERSIONS=(
  "0.1.1   84c1b880ca57e3cfbf871859fda7483f2c9416a1   #2"
  "0.2.0   8273e4c0514b4dca041a4f7d4069c0907f088448   #8"
  "0.3.0   b2fa95a84215a67fa717c514b046ece00e27988c   #9"
  "0.4.0   3c3d94b296484edfbc954c65b6d6a165eebe2b0e   #11"
  "0.5.0   495dcb053d56170a53a68a6c3174b56b5c546790   #14"
  "0.6.0   b1f63fe43fddc1ddcf26803d58f2002caba10088   #15"
  "0.7.0   2131ca52d7fc489f70c70b0a2776e956e9e855ea   #16"
  "0.8.0   fb2caedb02c24757a63835ef57bf22f0853c9a49   #18"
  "0.8.1   7c7a17fa496413951963f0b4024f31327e85ff4c   #20"
  "0.9.0   aadb638d38eeb37bc05620a73093a3aa8ce47f1a   #34"
  "0.10.0  d0082c61b3c339e9258baca2ce0998f6c1644b17   #35"
  "0.11.0  781151f9d7d7c38d957e89c920054c1510e629ec   #45"
)

apply=false
delete_old_tag=false
for arg in "$@"; do
  case "$arg" in
    --apply) apply=true ;;
    --delete-old-tag) delete_old_tag=true ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

run() {
  if $apply; then
    "$@"
  else
    printf 'would run:'; printf ' %q' "$@"; printf '\n'
  fi
}

cd "$(git rev-parse --show-toplevel)"
command -v gh >/dev/null || { echo "gh is required" >&2; exit 1; }
git fetch --quiet origin main --tags

notes_for() { # version previous_version commit
  local version="$1" previous="$2" commit="$3" migration
  git show origin/main:migrations/README.md |
    awk -v v="Version \`$version\`" 'index($0, v) == 1 { on = 1 } on && /^$/ { exit } on { print }'
  migration="migrations/${previous}-to-${version}.md"
  if [ -n "$previous" ] && git cat-file -e "$commit:$migration" 2>/dev/null; then
    printf '\nUpgrade an existing hq with [%s](https://github.com/%s/blob/v%s/%s).\n' \
      "$migration" "$REPO" "$version" "$migration"
  fi
  if [ -n "$previous" ]; then
    printf '\nFull diff: https://github.com/%s/compare/v%s...v%s\n' "$REPO" "$previous" "$version"
  fi
}

previous=""
last_index=$((${#VERSIONS[@]} - 1))
for i in "${!VERSIONS[@]}"; do
  read -r version commit pr <<<"${VERSIONS[$i]}"
  tag="v$version"
  echo "== $tag on ${commit:0:7} (pull request $pr)"

  git cat-file -e "$commit^{commit}" || { echo "commit $commit not found" >&2; exit 1; }
  git merge-base --is-ancestor "$commit" origin/main || { echo "$commit is not on main" >&2; exit 1; }
  found=$(git show "$commit:.claude-plugin/plugin.json" | sed -n 's/.*"version": *"\([^"]*\)".*/\1/p')
  [ "$found" = "$version" ] || { echo "plugin.json at $commit says $found, expected $version" >&2; exit 1; }

  remote=$(git ls-remote origin "refs/tags/$tag^{}" "refs/tags/$tag" | awk 'NR == 1 { print $1 }')
  if [ -n "$remote" ]; then
    target=$(git ls-remote origin "refs/tags/$tag^{}" | awk '{ print $1 }')
    target=${target:-$remote}
    [ "$target" = "$commit" ] || { echo "tag $tag exists on $target, expected $commit: stop" >&2; exit 1; }
    echo "tag $tag already exists on the expected commit"
  fi

  if gh release view "$tag" -R "$REPO" >/dev/null 2>&1; then
    echo "release $tag already exists: skipped"
  else
    notes=$(mktemp)
    notes_for "$version" "$previous" "$commit" >"$notes"
    if [ ! -s "$notes" ]; then echo "no notes found for $version in migrations/README.md" >&2; exit 1; fi
    latest="--latest=false"
    [ "$i" -eq "$last_index" ] && latest="--latest"
    echo "--- notes for $tag:"; cat "$notes"; echo "---"
    run gh release create "$tag" -R "$REPO" --target "$commit" --title "$tag" --notes-file "$notes" "$latest"
    rm -f "$notes"
  fi
  previous="$version"
done

echo "== old tag $OLD_TAG"
old=$(git ls-remote origin "refs/tags/$OLD_TAG^{}" | awk '{ print $1 }')
if [ -z "$old" ]; then
  echo "not on the remote: nothing to do"
elif ! $delete_old_tag; then
  echo "kept (it points to ${old:0:7}, the same commit as v0.1.1). Pass --delete-old-tag to delete it once v0.1.1 exists."
else
  v011=$(git ls-remote origin "refs/tags/v0.1.1^{}" "refs/tags/v0.1.1" | awk 'NR == 1 { print $1 }')
  if $apply && [ -z "$v011" ]; then
    echo "v0.1.1 does not exist on the remote: the old tag is kept" >&2; exit 1
  fi
  run git push origin --delete "refs/tags/$OLD_TAG"
  run git tag -d "$OLD_TAG"
fi

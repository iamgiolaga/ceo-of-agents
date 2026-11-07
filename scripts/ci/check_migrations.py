#!/usr/bin/env python3
"""Check that every released version ships its migration file.

Rules (see CONTRIBUTING.md, "Every version ships a migration"):
- Each version has an entry in migrations/README.md, "Current status", as a
  paragraph that starts with "Version `X.Y.Z`", in ascending order.
- Each version after the oldest one has exactly one file
  migrations/<previous>-to-<version>.md, where <previous> is the version listed
  just before it, and the README names that file.
- The version in .claude-plugin/plugin.json is listed, so it has a migration
  from the previous version.
- Every migration file belongs to a listed version (no orphans).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MIGRATIONS = ROOT / "migrations"
SEMVER = r"\d+\.\d+\.\d+"
ENTRY = re.compile(rf"^Version `({SEMVER})`", re.MULTILINE)
FILE_NAME = re.compile(rf"^({SEMVER})-to-({SEMVER})\.md$")


def key(version):
    return tuple(int(part) for part in version.split("."))


def main():
    errors = []
    readme = (MIGRATIONS / "README.md").read_text(encoding="utf-8")
    listed = ENTRY.findall(readme)
    plugin_version = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]

    if not listed:
        errors.append("migrations/README.md lists no version (paragraphs starting with \"Version `X.Y.Z`\")")
    if len(set(listed)) != len(listed):
        errors.append("migrations/README.md lists a version twice")
    if listed != sorted(listed, key=key):
        errors.append("migrations/README.md lists versions out of order: " + ", ".join(listed))

    files = {}
    for path in sorted(MIGRATIONS.glob("*.md")):
        if path.name == "README.md":
            continue
        match = FILE_NAME.match(path.name)
        if not match:
            errors.append(f"migrations/{path.name}: name is not <from>-to-<to>.md")
            continue
        source, target = match.groups()
        if key(source) >= key(target):
            errors.append(f"migrations/{path.name}: <from> is not older than <to>")
        if target in files:
            errors.append(f"migrations/{path.name}: second migration to {target} (also {files[target]})")
        files[target] = path.name

    for previous, version in zip(listed, listed[1:]):
        expected = f"{previous}-to-{version}.md"
        if version not in files:
            errors.append(f"version {version}: missing migrations/{expected}")
        elif files[version] != expected:
            errors.append(f"version {version}: migration is {files[version]}, expected {expected} (previous listed version is {previous})")
        elif expected not in readme:
            errors.append(f"version {version}: migrations/README.md does not name {expected}")

    for version, name in files.items():
        if version not in listed:
            errors.append(f"migrations/{name}: version {version} has no entry in migrations/README.md")

    if plugin_version not in listed:
        errors.append(f".claude-plugin/plugin.json version {plugin_version} has no entry in migrations/README.md, so no migration from the previous version")
    else:
        pending = [v for v in listed if key(v) > key(plugin_version)]
        if pending:
            print(f"note: listed but not released yet: {', '.join(pending)}")

    for error in errors:
        print(f"error: {error}")
    print(f"plugin {plugin_version}; {len(listed)} versions listed; {len(files)} migration files; {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

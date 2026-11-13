#!/usr/bin/env python3
"""Fail when this collection's index or a relative link is wrong.

The Stop hook runs this script. A session is not finished while it exits 2.
Error text names the fix, because that text is the instruction the agent reads.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE = re.compile(r"```.*?```", re.DOTALL)


def strip_fences(text: str) -> str:
    return FENCE.sub("", text)


def link_target(raw: str) -> str | None:
    target = raw.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    if " " in target:
        target = target.split()[0]
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    if target.startswith("/"):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    return target or None


def targets_in(path: Path) -> list[str]:
    text = strip_fences(path.read_text(encoding="utf-8"))
    found = []
    for match in LINK.finditer(text):
        target = link_target(match.group(1))
        if target:
            found.append(target)
    return found


def resolve(from_file: Path, target: str) -> Path:
    return (from_file.parent / target).resolve()


def check(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    readme = root / "README.md"
    if not readme.is_file():
        return ["README.md is missing. Add it at the repository root and link every file in notes/."]

    scanned = [readme]
    claude = root / "CLAUDE.md"
    if claude.is_file():
        scanned.append(claude)
    for folder in ("notes", "features"):
        directory = root / folder
        if directory.is_dir():
            scanned.extend(sorted(directory.glob("*.md")))

    notes_dir = root / "notes"
    notes = sorted(notes_dir.glob("*.md")) if notes_dir.is_dir() else []
    readme_links = {resolve(readme, target) for target in targets_in(readme)}
    for note in notes:
        if note.resolve() not in readme_links:
            rel = note.relative_to(root).as_posix()
            errors.append(
                f"{rel} is not linked from README.md. "
                f"Add a Notes table row whose link target is {rel}."
            )

    features_readme = root / "features" / "README.md"
    if not features_readme.is_file():
        errors.append(
            "features/README.md is missing. Add a feature map entry for each flow a person can do here, and link those files from features/README.md."
        )
    else:
        feature_links = {resolve(features_readme, target) for target in targets_in(features_readme)}
        for feature in sorted((root / "features").glob("*.md")):
            if feature.name == "README.md":
                continue
            if feature.resolve() not in feature_links:
                rel = feature.relative_to(root).as_posix()
                errors.append(
                    f"{rel} is not linked from features/README.md. "
                    f"Add a row whose link target is {rel}."
                )

    for path in scanned:
        for target in targets_in(path):
            dest = resolve(path, target)
            try:
                dest.relative_to(root)
            except ValueError:
                rel = path.relative_to(root).as_posix()
                errors.append(
                    f"{rel} links to {target}, which leaves the repository. Use a link inside this repo."
                )
                continue
            if not dest.exists():
                rel = path.relative_to(root).as_posix()
                errors.append(
                    f"{rel} links to {target}, and that file does not exist. Fix the path or add the file."
                )
            elif dest.is_dir():
                rel = path.relative_to(root).as_posix()
                errors.append(
                    f"{rel} links to {target}, which is a directory. Link a file, for example a README.md inside it."
                )
    return errors


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parents[1]
    errors = check(root)
    if errors:
        sys.stderr.write("Collection check failed.\n")
        for error in errors:
            sys.stderr.write(f"- {error}\n")
        return 2
    note_count = len(list((root / "notes").glob("*.md"))) if (root / "notes").is_dir() else 0
    sys.stdout.write(f"ok: {note_count} note(s) linked, relative links resolve\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

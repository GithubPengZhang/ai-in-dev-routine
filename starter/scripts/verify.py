#!/usr/bin/env python3
"""Run the finish checks named in scripts/verify.commands.

Exit 2 when the file is missing, empty, or a command fails. The Stop hook
uses that exit code to keep Claude Code working. A comment-only file is
not a check.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def commands(path: Path) -> list[str]:
    lines = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    return lines


def verify(root: Path) -> list[str]:
    path = root / "scripts" / "verify.commands"
    if not path.is_file():
        return [
            "scripts/verify.commands is missing. Add one finish check per line, "
            "for example: python3 -m pytest. The Stop hook will not let a session "
            "finish until those commands exit 0."
        ]
    chosen = commands(path)
    if not chosen:
        return [
            "scripts/verify.commands has no commands. A comment-only file does not count. "
            "Add one finish check per line. Each command must exit 0."
        ]
    for cmd in chosen:
        proc = subprocess.run(
            ["sh", "-c", cmd],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        if proc.returncode != 0:
            tail = (proc.stdout + "\n" + proc.stderr).strip().splitlines()
            shown = "\n".join(tail[-20:])
            return [
                f"Command failed (exit {proc.returncode}): {cmd}",
                shown or "(no output)",
                "Fix the failure and run scripts/verify.py again. A written summary is not a pass.",
            ]
    return []


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parents[1]
    errors = verify(root)
    if errors:
        sys.stderr.write("Verify failed.\n")
        for error in errors:
            sys.stderr.write(f"{error}\n")
        return 2
    count = len(commands(root / "scripts" / "verify.commands"))
    sys.stdout.write(f"ok: {count} command(s) passed\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

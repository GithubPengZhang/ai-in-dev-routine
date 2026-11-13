#!/usr/bin/env python3
"""Behavior checks for the collection checker and the app-repo verify script."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_collection import check  # noqa: E402


class Fail(Exception):
    pass


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise Fail(message)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def collection_fixture(tmp: Path) -> None:
    write(
        tmp / "README.md",
        "\n".join(
            [
                "# Notes",
                "",
                "See [the note](notes/one.md) and [features](features/README.md).",
                "External [site](https://example.com) and a [section](#top).",
                "",
            ]
        ),
    )
    write(tmp / "CLAUDE.md", "Run [the check](scripts/check_collection.py) later.\n")
    write(tmp / "notes" / "one.md", "Body. See [the map](../features/save.md).\n")
    write(tmp / "features" / "README.md", "Map: [save](save.md).\n")
    write(tmp / "features" / "save.md", "Proof is the command output.\n")
    write(tmp / "scripts" / "check_collection.py", "# present so the CLAUDE link resolves\n")


def test_happy_path() -> None:
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        collection_fixture(tmp)
        expect(check(tmp) == [], f"expected no errors, got {check(tmp)}")


def test_unlinked_note() -> None:
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        collection_fixture(tmp)
        write(tmp / "notes" / "two.md", "Forgot the index.\n")
        errors = check(tmp)
        expect(any("notes/two.md" in error and "README.md" in error for error in errors), errors)


def test_broken_link() -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            collection_fixture(tmp)
            write(tmp / "notes" / "one.md", "See [gone](../missing.md).\n")
            errors = check(tmp)
            expect(any("missing.md" in error for error in errors), errors)


def test_directory_link() -> None:
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        collection_fixture(tmp)
        write(tmp / "README.md", "Notes: [one](notes/one.md).\nFeatures: [dir](features/).\n")
        errors = check(tmp)
        expect(any("directory" in error for error in errors), errors)


def test_fenced_example_is_not_a_link() -> None:
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        collection_fixture(tmp)
        write(
            tmp / "notes" / "one.md",
            "Real [map](../features/save.md).\n\n```markdown\n[not real](../nope.md)\n```\n",
        )
        expect(check(tmp) == [], check(tmp))


def test_this_repo() -> None:
    errors = check(ROOT)
    expect(errors == [], errors)


def run_verify(root: Path) -> subprocess.CompletedProcess[str]:
    script = ROOT / "starter" / "scripts" / "verify.py"
    return subprocess.run(
        [sys.executable, str(script), str(root)],
        text=True,
        capture_output=True,
        check=False,
    )


def test_verify_missing_commands() -> None:
    with tempfile.TemporaryDirectory() as raw:
        proc = run_verify(Path(raw))
        expect(proc.returncode == 2, proc.returncode)
        expect("verify.commands" in proc.stderr, proc.stderr)


def test_verify_comments_only() -> None:
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        write(tmp / "scripts" / "verify.commands", "# python3 -m pytest\n\n")
        proc = run_verify(tmp)
        expect(proc.returncode == 2, proc.stderr)
        expect("no commands" in proc.stderr, proc.stderr)


def test_verify_pass_and_fail() -> None:
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        write(tmp / "scripts" / "verify.commands", "python3 -c 'import sys; sys.exit(0)'\n")
        proc = run_verify(tmp)
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        expect(proc.stdout.startswith("ok:"), proc.stdout)
        write(
            tmp / "scripts" / "verify.commands",
            "python3 -c 'import sys; sys.stderr.write(\"boom\\n\"); sys.exit(1)'\n",
        )
        proc = run_verify(tmp)
        expect(proc.returncode == 2, proc.returncode)
        expect("boom" in proc.stderr, proc.stderr)


def test_stop_hook_on_this_repo() -> None:
    proc = subprocess.run(
        ["sh", str(ROOT / "scripts" / "stop_hook.sh")],
        text=True,
        capture_output=True,
        check=False,
    )
    expect(proc.returncode == 0, proc.stderr)
    expect(proc.stdout.startswith("ok:"), proc.stdout)


def main() -> int:
    tests = [
        test_happy_path,
        test_unlinked_note,
        test_broken_link,
        test_directory_link,
        test_fenced_example_is_not_a_link,
        test_verify_missing_commands,
        test_verify_comments_only,
        test_verify_pass_and_fail,
        test_this_repo,
        test_stop_hook_on_this_repo,
    ]
    failed = 0
    for test in tests:
        try:
            test()
        except Fail as exc:
            failed += 1
            print(f"FAIL {test.__name__}: {exc}")
        except Exception as exc:  # noqa: BLE001 — report and continue
            failed += 1
            print(f"FAIL {test.__name__}: {type(exc).__name__}: {exc}")
        else:
            print(f"ok   {test.__name__}")
    if failed:
        print(f"{failed} failed")
        return 1
    print(f"ok: {len(tests)} checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())

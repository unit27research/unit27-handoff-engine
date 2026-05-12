"""Verify wheel contents for Unit27 Handoff Engine."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path


REQUIRED = {
    "handoff_engine/__init__.py",
    "handoff_engine/cli.py",
    "handoff_engine/core.py",
}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_wheel.py PATH_TO_WHEEL", file=sys.stderr)
        return 2

    wheel = Path(sys.argv[1])
    if not wheel.exists():
        print(f"wheel not found: {wheel}", file=sys.stderr)
        return 2

    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())

    missing = sorted(required for required in REQUIRED if not any(name.endswith(required) for name in names))
    if missing:
        print("missing wheel contents:")
        for item in missing:
            print(f"- {item}")
        return 1

    print("wheel contents verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

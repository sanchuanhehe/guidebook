from __future__ import annotations

from pathlib import Path


LOCALE_DIR = Path("locales")


def normalize(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    normalized = original.rstrip() + "\n"
    if original == normalized:
        return False
    path.write_text(normalized, encoding="utf-8")
    return True


def main() -> int:
    changed = 0
    for path in sorted(LOCALE_DIR.rglob("*.po")):
        if normalize(path):
            changed += 1
            print(f"normalized,{path}")
    print(f"summary,normalized-files,{changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

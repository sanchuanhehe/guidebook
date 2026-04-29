from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from babel.messages import pofile


ROOT = Path(__file__).resolve().parents[2]
LOCALE_DIR = ROOT / "locales/zh_CN/LC_MESSAGES"
CN_GETTEXT_DIR = ROOT / "_build/gettext-cn"


def read_messages(path: Path):
    with path.open(encoding="utf-8") as file:
        catalog = pofile.read_po(file, locale="zh_CN")
    messages = [message for message in catalog if message.id]
    return catalog, messages


def write_catalog(path: Path, catalog) -> None:
    with path.open("wb") as file:
        pofile.write_po(file, catalog, width=79, sort_output=False)
    path.write_text(path.read_text(encoding="utf-8").rstrip() + "\n", encoding="utf-8")


def extract_chinese_gettext() -> None:
    env = os.environ.copy()
    env.setdefault("SOURCE_DATE_EPOCH", "0")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx.cmd.build",
            "-c",
            str(ROOT),
            "-D",
            "root_doc=README",
            "-b",
            "gettext",
            str(ROOT / "l10n/cn"),
            str(CN_GETTEXT_DIR),
        ],
        check=True,
        env=env,
    )


def migrate_catalog(path: Path, overwrite: bool) -> tuple[str, int, str]:
    relative = path.relative_to(LOCALE_DIR)
    source_pot = (CN_GETTEXT_DIR / relative).with_suffix(".pot")
    if not source_pot.exists():
        return str(relative), 0, "missing-cn-source"

    catalog, target_messages = read_messages(path)
    _, source_messages = read_messages(source_pot)

    if len(target_messages) != len(source_messages):
        return (
            str(relative),
            0,
            f"message-count-mismatch:{len(target_messages)}!={len(source_messages)}",
        )

    migrated = 0
    for target, source in zip(target_messages, source_messages, strict=True):
        if target.string and not overwrite:
            continue
        if isinstance(source.id, tuple):
            continue
        target.string = source.id
        target.flags.discard("fuzzy")
        migrated += 1

    write_catalog(path, catalog)
    return str(relative), migrated, "migrated"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Import existing l10n/cn Markdown text into zh_CN gettext catalogs."
    )
    parser.add_argument(
        "--skip-extract",
        action="store_true",
        help="Use an existing _build/gettext-cn directory instead of regenerating it.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing non-empty msgstr values.",
    )
    args = parser.parse_args()

    if not args.skip_extract:
        extract_chinese_gettext()

    migrated_files = 0
    migrated_messages = 0
    skipped = []

    for path in sorted(LOCALE_DIR.rglob("*.po")):
        relative, count, status = migrate_catalog(path, args.overwrite)
        if status == "migrated":
            migrated_files += 1
            migrated_messages += count
            print(f"migrated,{relative},{count}")
        else:
            skipped.append((relative, status))
            print(f"skipped,{relative},{status}")

    print(f"summary,migrated-files,{migrated_files}")
    print(f"summary,migrated-messages,{migrated_messages}")
    print(f"summary,skipped-files,{len(skipped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

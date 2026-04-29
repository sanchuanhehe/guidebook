from __future__ import annotations

from pathlib import Path

from babel.messages import pofile


LOCALE_DIR = Path("locales/zh_CN/LC_MESSAGES")


def catalog_messages(path: Path):
    with path.open(encoding="utf-8") as file:
        catalog = pofile.read_po(file, locale="zh_CN")
    return [message for message in catalog if message.id]


def main() -> int:
    rows = []
    totals = {"messages": 0, "translated": 0, "untranslated": 0, "fuzzy": 0}

    for path in sorted(LOCALE_DIR.rglob("*.po")):
        messages = catalog_messages(path)
        translated = sum(1 for message in messages if message.string)
        fuzzy = sum(1 for message in messages if "fuzzy" in message.flags)
        untranslated = len(messages) - translated

        totals["messages"] += len(messages)
        totals["translated"] += translated
        totals["untranslated"] += untranslated
        totals["fuzzy"] += fuzzy

        rows.append(
            (
                str(path.relative_to(LOCALE_DIR)),
                len(messages),
                translated,
                untranslated,
                fuzzy,
            )
        )

    print("file,messages,translated,untranslated,fuzzy")
    for row in rows:
        print(",".join(str(value) for value in row))

    print(
        "TOTAL,{messages},{translated},{untranslated},{fuzzy}".format(
            **totals,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

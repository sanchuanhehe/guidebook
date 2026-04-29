# Translation maintenance

This page records the current translation workflow and the hosted platform evaluation for discussion 260. The default workflow remains GitHub-only until maintainers decide that an external translation platform is worth the added administration.

## Current workflow

The repository uses Sphinx gettext catalogs under `locales/`. The existing Chinese Markdown tree under `l10n/cn` maps to the Sphinx locale code `zh_CN`.

Use uv for all commands:

```
uv sync
SOURCE_DATE_EPOCH=0 uv run sphinx-build -b gettext . _build/gettext
uv run sphinx-intl update -p _build/gettext -l zh_CN --locale-dir locales
uv run python tools/i18n/normalize_po_files.py
uv run sphinx-build -b html -D language=zh_CN . _build/html/zh_CN
uv run python tools/i18n/catalog_status.py
```

Generated files under `_build/` are local artifacts. Commit gettext `.po` files under `locales/` when translation source changes.

## Existing Chinese Markdown import

The helper below imports existing `l10n/cn` text into `zh_CN` catalogs only when the English and Chinese files have the same extracted message count:

```
uv run python tools/i18n/migrate_cn_markdown.py
```

The first safe import migrated 21 files and 1400 messages. A follow-up manual review pass filled the remaining `zh_CN` catalog entries, bringing the catalog status to `2249` translated messages, `0` untranslated messages, and `0` fuzzy messages.

The files below needed extra review because either the matching Chinese source did not exist, or the extracted message counts differed:

| Catalog | Reason |
| --- | --- |
| `CONTRIBUTING.po` | `65 != 60` messages |
| `CONTRIBUTORS.po` | `52 != 75` messages |
| `README.po` | `7 != 3` messages |
| `getting-started/building-a-strategy.po` | `131 != 130` messages |
| `getting-started/essentials-of-building-a-community.po` | `110 != 112` messages |
| `growing-contributors/project-and-community-governance.po` | `227 != 229` messages |
| `index.po` | no matching Chinese source |
| `measuring-success/announcing-software-releases.po` | `70 != 69` messages |
| `measuring-success/understanding-community-metrics.po` | `114 != 115` messages |

Those files were not accepted by the strict one-to-one import path. Do not fill them by position when source and translated message counts diverge: a source insertion, a translated-only heading, or a deduplicated gettext message can shift every following entry. Future updates to these files need either a file-specific mapping or manual review.

## Hosted platform evaluation

| Option | Strengths | Costs and risks | Decision |
| --- | --- | --- | --- |
| GitHub-only gettext workflow | No new account, service, permission model, or synchronization bot. Works with uv, Sphinx, sphinx-intl, CI artifacts, and normal pull requests. | Translators edit `.po` files directly unless they use a local PO editor. Translation memory and glossary support stay outside the repository. | Recommended default for the first infrastructure phase. |
| Weblate | Official docs describe gettext `.po` and `.pot` support, Sphinx documentation translation support, and addons for `msgmerge` and generated `.mo` files. | Requires project setup and ongoing administration of a hosted or self-hosted service. Adds another review surface outside GitHub. | Good second-phase candidate if the community wants browser-based translation and translation memory. |
| Pontoon | Mozilla describes Pontoon as an open source translation management system driven by community localization and version-control storage. | Self-hosting or instance access must be arranged. Official repository notes Heroku deployment and says production Docker deployment is not recommended. | Defer until maintainers want to operate or join a Pontoon instance. |
| Transifex | Official docs describe gettext PO support, developer comments, context, source references, plural forms, and a GitHub integration that links a Transifex project to a repository through the UI. | Commercial service and account administration. GitHub integration adds branch/sync policy decisions. | Defer until maintainers explicitly want a managed translation platform. |

References:

- uv projects: https://docs.astral.sh/uv/concepts/projects/
- Sphinx internationalization: https://www.sphinx-doc.org/en/master/usage/advanced/intl.html
- sphinx-intl workflow: https://sphinx-intl.readthedocs.io/en/master/basic.html
- Weblate gettext support: https://docs.weblate.org/en/latest/formats/gettext.html
- Pontoon repository and documentation: https://github.com/mozilla/pontoon
- Transifex gettext support: https://help.transifex.com/en/articles/6220794-gettext-po
- Transifex GitHub integration: https://help.transifex.com/en/articles/6265125-github-installation-and-configuration

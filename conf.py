project = "The Open Source Way"
author = "The Open Source Way contributors"

extensions = ["myst_parser"]

source_suffix = {
    ".md": "markdown",
}
root_doc = "index"
exclude_patterns = [
    ".git",
    ".venv",
    "_build",
    "l10n/**",
    "SUMMARY.md",
]

locale_dirs = ["locales/"]
gettext_compact = False

myst_heading_anchors = 3

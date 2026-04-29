project = "The Open Source Way"
author = "The Open Source Way contributors"

extensions = ["myst_parser"]
templates_path = ["_templates"]

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

language = "en"
html_sidebars = {
    "**": [
        "language_switcher.html",
        "globaltoc.html",
        "relations.html",
        "sourcelink.html",
        "searchbox.html",
    ]
}

project = "The Open Source Way"
author = "The Open Source Way contributors"

extensions = ["myst_parser"]
templates_path = ["_templates"]
html_static_path = ["_static"]
html_css_files = ["custom.css"]

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
html_theme = "sphinx_book_theme"
html_title = project
html_theme_options = {
    "repository_url": "https://github.com/theopensourceway/guidebook",
    "repository_branch": "main",
    "path_to_docs": "",
    "use_edit_page_button": True,
    "use_issues_button": True,
    "use_repository_button": True,
    "use_download_button": False,
    "home_page_in_toc": True,
    "show_navbar_depth": 1,
    "max_navbar_depth": 3,
    "show_toc_level": 2,
    "toc_title": "On this page",
}
html_sidebars = {
    "**": [
        "navbar-logo.html",
        "icon-links.html",
        "search-button-field.html",
        "language_switcher.html",
        "sbt-sidebar-nav.html",
    ]
}


def setup(app):
    def localize_theme_options(app, config):
        if config.language == "zh_CN":
            config.html_theme_options["toc_title"] = "本页内容"

    app.connect("config-inited", localize_theme_options)

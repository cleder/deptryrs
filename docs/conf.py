project = "deptryrs"
author = "Christian Ledermann"
release = "0.1.0"

extensions = [
    "myst_parser",
    "sphinxcontrib.mermaid",
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "tasklist",
]

source_suffix = {".md": "myst"}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_title = "deptryrs"
html_theme_options = {
    "source_repository": "https://github.com/christianledermann/deptryrs",
    "source_branch": "main",
    "source_directory": "docs/",
}

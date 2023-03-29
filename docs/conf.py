# Configuration file for the Sphinx documentation builder.

project = "wwt_api_client"
author = "WorldWide Telescope project"
copyright = "2019-2023 " + author

release = "0.dev0"  # cranko project-version

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx_automodapi.automodapi",
    "sphinx_automodapi.smart_resolver",
    "numpydoc",
]

master_doc = "index"
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

numpydoc_class_members_toctree = False

html_theme = "alabaster"
html_static_path = ["_static"]
html_logo = "images/logo.png"

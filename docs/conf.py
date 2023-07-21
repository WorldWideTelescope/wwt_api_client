# -*- coding: utf-8 -*-

project = "wwt_api_client"
author = "WorldWide Telescope project"
copyright = "2019-2023 " + author

release = "0.4.0"  # cranko project-version
version = ".".join(release.split(".")[:2])

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

templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"
todo_include_todos = False

html_theme = "bootstrap-astropy"
html_theme_options = {
    "logotext1": "wwt_api_client",
    "logotext2": "",
    "logotext3": ":docs",
    "astropy_project_menubar": False,
}
html_static_path = ["_static"]
htmlhelp_basename = "wwtapiclientdoc"

intersphinx_mapping = {
    "python": (
        "https://docs.python.org/3/",
        (None, "http://data.astropy.org/intersphinx/python3.inv"),
    ),
    "requests": ("https://requests.readthedocs.io/en/stable/", None),
    "wwt_data_formats": ("https://wwt-data-formats.readthedocs.io/en/stable/", None),
}

numpydoc_show_class_members = False

nitpicky = True
nitpick_ignore = [
    # dataclasses-json stuff that we have to ignore.
    ("py:class", "dataclasses_json.api.A"),
    ("py:class", "dataclasses_json.mm.A"),
    ("py:class", "dataclasses_json.mm.SchemaF"),
]

default_role = "obj"

html_logo = "images/logo.png"

linkcheck_retries = 5
linkcheck_timeout = 10

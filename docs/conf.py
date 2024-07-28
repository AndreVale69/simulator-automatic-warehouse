# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Simulator Automatic Warehouse'
copyright = '2024, Andrea Valentini'
author = 'Andrea Valentini'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.duration"
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# classic theme
# html_theme = 'sphinx_rtd_theme'
# cool theme: https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html
html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
from automatic_warehouse  import __about__
version = __about__.__version__
html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/AndreVale69/simulator-automatic-warehouse/",
            "icon": "fa-brands fa-github",
        }
    ],
    "switcher": {
        "version_match": version,
        "json_url": "https://simulator-automatic-warehouse.readthedocs.io/en/latest/_static/versions.json",
    },
   "navbar_align": "right",
   "header_links_before_dropdown": 3,
   "navbar_end": [
        "theme-switcher",
        "version-switcher",
        "navbar-icon-links"
    ],
    "show_version_warning_banner": True
}

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ALC AiiDAlab Guides'
copyright = '2025, Ada Lovelace Center'
author = 'Dr. Benjamin T. Speake'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon"
]

templates_path = ['_templates']
exclude_patterns = []

source_suffix = ".rst"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'piccolo_theme'
html_static_path = ['_static']
html_css_files = ["custom.css"]
# html_logo = "../../images/alc.svg"

html_theme_options = {
    "source_url": "https://github.com/stfc/alc-ux"
}

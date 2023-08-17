# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'demo'
copyright = '2020, kujiu'
author = 'Kujiu'

# The full version, including alpha/beta/rc tags
release = '0.1'
version = '0.1'


# -- General configuration ---------------------------------------------------

master_doc = 'source/index'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.autodoc',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'nervproject'
epub_theme = 'nervproject'
epub_exclude_files = [
    '_static/sphinx_nervproject_print.css',
    '_static/sphinx_nervproject_theme.css',
    '_static/sphinx_nervproject_theme.js',
    '_static/basic.css',
]
html_theme_options = {
    "logoalt": project,
    "social": [
    ],
    "license": {
        'type': 'CC',
        'subtype': 'BY-SA',
        'version': '4.0',
        'url': 'https://creativecommons.org/licenses/by-sa/4.0/legalcode'
    }
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
weasyprint_theme = 'nervproject'
weasyprint_footer_selector = 'footer.footer'
weasyprint_header_selector = 'header.navbar'
weasyprint_main_selector = 'main.content'

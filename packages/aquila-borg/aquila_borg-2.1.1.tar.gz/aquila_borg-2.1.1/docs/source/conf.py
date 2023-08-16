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
import os
import sys
# sys.path.insert(0, os.path.abspath('.'))
sys.path.append(os.path.abspath('../sphinx_ext/'))
import datetime
now = datetime.datetime.now()
year = '{:02d}'.format(now.year)

# -- Project information -----------------------------------------------------
extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx.ext.autosummary',
    'sphinx.ext.napoleon', 'sphinx_rtd_theme', 'sphinx.ext.mathjax',
    'sphinx.ext.todo', 'nbsphinx',
    'IPython.sphinxext.ipython_console_highlighting', 'sphinx_copybutton',
    'toctree_filter'
]
master_doc = 'index'
source_suffix = '.rst'
rst_prolog = '''
.. |a| replace:: *ARES*
'''

# General information about the project.
project = u'ARES-HADES-BORG'
author = u'the Aquila Consortium'
copyright = u"""
2009-""" + year + """, the Aquila Consortium
"""
#version = "latest"

autosummary_generate = True

todo_include_todos = True

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
#extensions = [
#        'breathe',
#        'exhale',
#]

nbsphinx_execute = 'never'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.inc.rst']
# Excluding the extension .inc.rst avoids compiling "included" rst file
# (otherwise the corresponding .html is produced) and avoids the "duplicate label"
# warning in case a label is found there (Florent Leclercq, 24-10-2020)

#html_extra_path = [os.path.abspath('../_build/html')]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_context = {
    'theme_vcs_pageview_mode': 'view&spa=0'
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
    'css/custom.css',
]

# --- Breathe/Exhale options

breathe_projects = {"ARES libLSS": "./doxyoutput/xml"}

breathe_default_project = "ARES libLSS"

exhale_args = {
    "containmentFolder": "./api",
    "rootFileName": "library_root.rst",
    "rootFileTitle": "Library API",
    "doxygenStripFromPath": "..",
    "createTreeView": True,
    "exhaleExecutesDoxygen": True,
    "exhaleUseDoxyfile": True
}

primary_domain = 'py'
highlight_language = 'py'

# on_rtd is whether we are on readthedocs.org, this line of code grabbed from docs.readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
    toc_filter_exclude = []
    meta={"bitbucket_url": 'https://www.bitbucket.org/bayesian_lss_team/ares'}
    bitbucket_url='https://www.bitbucket.org/bayesian_lss_team/ares'
else:
    toc_filter_exclude = ["aquila"]

import subprocess

os.environ["ARES_BASE"] = os.path.abspath(os.path.join(os.getcwd(), ".."))
#subprocess.call('doxygen Doxyfile', shell=True)

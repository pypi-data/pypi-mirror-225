# -*- coding: utf-8 -*-
#
# dqsegdb2 documentation build configuration file

import glob
import os.path
import re
import sys
from importlib import metadata

# -- metadata

project = "dqsegdb2"
copyright = "2018-2022, Cardiff University"
author = "Duncan Macleod"
release = metadata.version(project)
version = re.split(r"[\w-]", release)[0]

# -- config

default_role = "obj"
pygments_style = "monokai"

# -- extensions

extensions = [
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_automodapi.automodapi",
]

# Intersphinx directory
intersphinx_mapping = {
    "igwn-auth-utils": (
        "https://igwn-auth-utils.readthedocs.io/en/stable/",
        None,
    ),
    "ligo-segments": (
        "https://lscsoft.docs.ligo.org/ligo-segments/",
        None,
    ),
    "python": (
        f"https://docs.python.org/{sys.version_info.major}",
        None,
    ),
    "requests": (
        "https://requests.readthedocs.io/en/stable/",
        None,
    ),
    "scitokens": (
        "https://scitokens.readthedocs.io/en/stable/",
        None,
    ),
}

# don't inherit in automodapi
automodapi_inherited_members = False

# -- theme

html_theme = "sphinx_rtd_theme"

# Licensed under a 3-clause BSD style license - see LICENSE.rst

# Packages may add whatever they like to this file, but
# should keep this content at the top.
# ----------------------------------------------------------------------------
from ._astropy_init import *   # noqa
# ----------------------------------------------------------------------------

# Enforce Python version check during package import.
# This is the same check as the one at the top of setup.py
import sys
from distutils.version import LooseVersion

__minimum_python_version__ = "3.7"

__all__ = []


class UnsupportedPythonError(Exception):
    """
    Wraps an exception to raise if a user tries to use stellarphot
    with an unsupported version of Python.
    """
    pass


if LooseVersion(sys.version) < LooseVersion(__minimum_python_version__):
    raise UnsupportedPythonError("stellarphot does not support Python < {}"
                                 .format(__minimum_python_version__))

from .core import *
from .source_detection import *
from .photometry import *

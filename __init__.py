
# Standard library imports
from datetime import date as _date
from collections import namedtuple as _namedtuple

# Version of pytrans.
#
# See http://semver.org/ for info about Semantic Versioning.  See PEP 440,
# https://www.python.org/dev/peps/pep-0440/ for info about versioning of Python
# projects.
__version__ = '1.0.0'

# Authors of the library wrapper
_Author = _namedtuple('Author', ['name', 'email', 'start', 'end'])
_Author.__new__.__defaults__ = (None,) * len(_Author._fields)

_AUTHORS = sorted([
    _Author('Sveinung Himle', 'sveinung.himle@kartverket.no'),], key=lambda a: a.name.split()[-1]) # Sort on last name

__author__ = ', '.join(a.name for a in _AUTHORS)    # TODO: Use start/end
__contact__ = ', '.join(a.email for a in _AUTHORS)  # TODO: Use start/end

# Copyright of the library wrapper
__copyright__ = ('2022 - {} Norwegian Mapping Authority (Kartverket)'
                 ''.format(_date.today().year))
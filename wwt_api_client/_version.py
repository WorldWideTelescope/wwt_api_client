# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the .Net Foundation
# Distributed under the terms of the revised (3-clause) BSD license.

version_info = (0, 1, 0, 'dev', 0)

_specifier_ = {'alpha': 'a', 'beta': 'b', 'candidate': 'rc', 'final': '', 'dev': 'dev'}
_ext = '' if version_info[3] == 'final' else _specifier_[version_info[3]] + str(version_info[4])
__version__ = '%s.%s.%s%s' % (version_info[0], version_info[1], version_info[2], ext)

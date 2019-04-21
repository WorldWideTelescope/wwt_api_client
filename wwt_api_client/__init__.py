# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the .Net Foundation
# Distributed under the terms of the revised (3-clause) BSD license.

from __future__ import absolute_import, division, print_function

import requests

from ._version import version_info, __version__  # noqa

__all__ = '''
APIResponseError
Client
DEFAULT_API_BASE
'''.split()

DEFAULT_API_BASE = 'http://www.worldwidetelescope.org'


class APIResponseError(Exception):
    """Raised when the API returns an HTTP error.

    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Client(object):
    _api_base = None
    _session = None

    def __init__(self, api_base=None):
        if api_base is None:
            api_base = DEFAULT_API_BASE

        self._api_base = api_base


    @property
    def session(self):
        if self._session is None:
            self._session = requests.session()

        return self._session

    def show_image(self):
        """Do some stuff.

        Parameters
        ----------
        yo : type
           Def

        Returns
        -------
        text : type

        """
        endpoint = self._api_base + '/WWTWeb/ShowImage.aspx'
        resp = self._session.get(endpoint)
        if not resp.ok:
            raise APIResponseError(resp.text)

        return resp.text

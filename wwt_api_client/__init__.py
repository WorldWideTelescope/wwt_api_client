# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the .Net Foundation
# Distributed under the terms of the revised (3-clause) BSD license.

from __future__ import absolute_import, division, print_function

import requests
import six
from six.moves.urllib import parse as url_parse
from xml.sax.saxutils import escape as xml_escape
import warnings

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


class InvalidRequestError(Exception):
    """Raised when an API request is not in a valid state

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

    def show_image(self, name, image_url):
        """Do some stuff.

        Parameters
        ----------
        yo : type
           Def

        Returns
        -------
        text : type

        """
        req = ShowImageRequest(self)
        req.name = name
        req.image_url = image_url
        return req


def _get_our_encoding():
    """Get the encoding that we will use to convert bytes to Unicode.

    We delegate to ``sys.getdefaultencoding()``, but with the wrinkle that if
    that returns "ascii", as sometimes happens, we upgrade to UTF-8.

    """
    import sys

    enc = sys.getdefaultencoding()
    if enc == 'ascii':
        return 'utf-8'
    return enc


def _maybe_as_bytes(obj, xml_esc=False, in_enc=None, out_enc='utf-8'):
    import codecs

    if obj is None:
        return None

    if in_enc is None:
        in_enc = _get_our_encoding()

    if isinstance(obj, six.binary_type):
        # If we don't special-case, b'abc' becomes "b'abc'".
        #
        # It would also be nice if we could validate that *obj* is
        # appropriately encoded (when in_enc = out_enc) without converting and
        # de-converting it to Unicode, but I don't see how to do that, and for
        # this API I don't expect the overhead to be significant.
        text = codecs.decode(obj, in_enc)
    else:
        text = six.text_type(obj)

    if xml_esc:
        text = xml_escape(text)

    return codecs.encode(text, out_enc)


def _is_textable(obj, none_ok=False):
    if obj is None:
        return none_ok

    if isinstance(obj, six.binary_type):
        import codecs

        try:
            codecs.decode(obj, _get_our_encoding())
        except Exception:
            return False
        return True

    try:
        six.text_type(obj)
    except Exception:
        return False
    return True


def _is_absurl(obj, none_ok=False):
    if obj is None:
        return none_ok

    # We're monkey-see-monkey-do here, w.r.t. the proper way to think about
    # encoding and decoding with URLs. The urllib approach seems to be to only
    # allow ASCII in and out.
    import codecs

    if isinstance(obj, six.binary_type):
        # If we don't special-case, b'abc' becomes "b'abc'".
        try:
            text = codecs.decode(obj, 'ascii')
        except Exception:
            return False
    else:
        try:
            text = six.text_type(obj)
        except Exception:
            return False

        # We also need to be able to go the other way:
        try:
            codecs.encode(text, 'ascii')
        except Exception:
            return False

    # OK, now does it parse?
    try:
        parsed = url_parse.urlparse(text)
    except Exception:
        return False

    return parsed.netloc is not None


def _is_scalar(obj, none_ok=False):
    if obj is None:
        return none_ok

    try:
        val = float(obj)
    except Exception:
        return False

    import math
    return math.isfinite(val)


class APIRequest(object):
    _client = None

    def __init__(self, client):
        self._client = client

    def invalidity_reason(self):
        return None

    def make_request(self):
        raise NotImplementedError()

    def send(self):
        invalid = self.invalidity_reason()
        if invalid is not None:
            raise InvalidRequestError(invalid)

        resp = self._client.session.send(self.make_request().prepare())
        if not resp.ok:
            raise APIResponseError(resp.text)

        return resp.text


class ShowImageRequest(APIRequest):
    credits = None

    credits_url = None

    dec_deg = 0.0

    image_url = None

    name = None

    ra_deg = 0.0

    reverse_parity = False

    rotation_deg = 0.0

    scale = 1.0

    thumbnail_url = None

    x_offset_pixels = 0.0

    y_offset_pixels = 0.0

    def invalidity_reason(self):
        if not _is_textable(self.credits, none_ok=True):
            return '"credits" must be None or a string-like object'

        if not _is_absurl(self.credits_url, none_ok=True):
            return '"credits_url" must be None or a valid absolute URL'

        if not _is_scalar(self.dec_deg):
            return '"dec_deg" must be a number'

        dec = float(self.dec_deg)
        if dec < -90 or dec > 90:
            return '"dec_deg" must be between -90 and 90'

        if not _is_absurl(self.image_url):
            return '"image_url" must be a valid absolute URL'

        if not _is_textable(self.name):
            return '"name" must be a string or an object that can be stringified'

        if ',' in str(self.name):
            warnings.warn('ShowImage name {0} contains commas, which will be stripped '
                          'by the server'.format(self.name), UserWarning)

        if not _is_scalar(self.ra_deg):
            return '"ra_deg" must be a number'

        if not isinstance(self.reverse_parity, bool):
            return '"reverse_parity" must be a boolean'

        if not _is_scalar(self.rotation_deg):
            return '"rotation_deg" must be a number'

        if not _is_scalar(self.scale):
            return '"scale" must be a number'

        if not _is_absurl(self.thumbnail_url, none_ok=True):
            return '"thumbnail_url" must be None or a valid absolute URL'

        if not _is_scalar(self.x_offset_pixels):
            return '"x_offset_pixels" must be a number'

        if not _is_scalar(self.y_offset_pixels):
            return '"y_offset_pixels" must be a number'

        return None

    def make_request(self):
        params = [
            ('dec', '%.18e' % float(self.dec_deg)),
            ('imageurl', _maybe_as_bytes(self.image_url, xml_esc=True, in_enc='ascii', out_enc='ascii')),
            ('name', _maybe_as_bytes(self.name, xml_esc=True)),
            ('ra', '%.18e' % (float(self.ra_deg) % 360)),  # The API clips, but we wrap
            ('rotation', '%.18e' % (float(self.rotation_deg) + 180)),  # API is bizarre here
            ('scale', '%.18e' % float(self.scale)),
            ('wtml', 't'),
            ('x', '%.18e' % float(self.x_offset_pixels)),
            ('y', '%.18e' % float(self.y_offset_pixels)),
        ]

        if self.credits is not None:
            params.append(('credits', _maybe_as_bytes(self.credits, xml_esc=True)))

        if self.credits_url is not None:
            params.append(('creditsUrl', _maybe_as_bytes(self.credits_url, xml_esc=True, in_enc='ascii', out_enc='ascii')))

        if self.reverse_parity:
            params.append(('reverseparity', 't'))

        if self.thumbnail_url is not None:
            params.append(('thumb', _maybe_as_bytes(self.thumbnail_url, xml_esc=True, in_enc='ascii', out_enc='ascii')))

        return requests.Request(
            method = 'GET',
            url = self._client._api_base + '/WWTWeb/ShowImage.aspx',
            params = params,
        )

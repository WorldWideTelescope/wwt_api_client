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
__version__
APIRequest
APIResponseError
Client
DEFAULT_API_BASE
InvalidRequestError
ShowImageRequest
version_info
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
    """The main object for accessing the WWT web services.

    Use this object to access the WWT APIs.

    Parameters
    ----------
    api_base : URL string or None
       The base URL to use for accessing the WWT web APIs. Defaults to
       :data:`DEFAULT_API_BASE`, which is probably equal to
       "http://www.worldwidetelescope.org". The API base is configurable to
       make it possible to access testing servers, etc. This value should not
       end in a slash.

    """
    _api_base = None
    _session = None

    def __init__(self, api_base=None):
        if api_base is None:
            api_base = DEFAULT_API_BASE

        self._api_base = api_base

    @property
    def session(self):
        """A ``requests.Session`` object used to talk to the WWT API server."""
        if self._session is None:
            self._session = requests.session()

        return self._session

    def show_image(self, name=None, image_url=None, credits=None, credits_url=None,
                   dec_deg=0.0, ra_deg=0.0, reverse_parity=False, rotation_deg=0.0,
                   scale=1.0, thumbnail_url=None, x_offset_pixels=0.0, y_offset_pixels=0.0):
        """Create a :ref:`ShowImage <endpoint-ShowImage>` request object.

        Parameters are assigned to attributes of the return value; see
        :class:`the class documentation <ShowImageRequest>` for descriptions.

        Examples
        --------
        The only two essential arguments are ``name`` and ``image_url``::

            >>> from wwt_api_client import Client
            >>> req = Client().show_image('My Image', 'http://example.com/space.jpg')
            >>> print(req.send()[:10])  # prints start of a WTML XML document
            <?xml vers

        Returns
        -------
        request : an initialized :class:`ShowImageRequest` object
            The request.

        """
        req = ShowImageRequest(self)
        req.name = name
        req.image_url = image_url
        req.credits = credits
        req.credits_url = credits_url
        req.dec_deg = dec_deg
        req.ra_deg = ra_deg
        req.reverse_parity = reverse_parity
        req.rotation_deg = rotation_deg
        req.scale = scale
        req.thumbnail_url = thumbnail_url
        req.x_offset_pixels = x_offset_pixels
        req.y_offset_pixels = y_offset_pixels
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
        text = xml_escape(text, {'"': '&quot;'})

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

    return bool(parsed.netloc)


def _is_scalar(obj, none_ok=False):
    if obj is None:
        return none_ok

    try:
        val = float(obj)
    except Exception:
        return False

    import math
    return not (math.isinf(val) or math.isnan(val))  # math.isfinite() only available in 3.x


class APIRequest(object):
    """A base class represent various WWT API requests.

    This class provides a generic representation of WWT API requests. For
    instance, every API request instance provides a :meth:`make_request`
    method that gets the underlying HTTP request as a ``requests.Request``
    class.

    You don’t generally need to instantiate requests yourself. Instead, use
    the methods on :class:`Client` to create requests.

    Parameters
    ----------
    client : :class:`Client`
       The client with which this request is associated.

    """
    _client = None

    def __init__(self, client):
        self._client = client

    def invalidity_reason(self):
        """Check whether the parameters of this request are valid.

        Examples
        --------
        You can manually check if a request is correctly set up::

            >>> from wwt_api_client import Client
            >>> req = Client().show_image('My Image', 'http://example.com/space.jpg')
            >>> assert req.invalidity_reason() is None

        Returns
        -------
        reason : string or None
            If None, indicates that this request is valid. Otherwise, the
            returned string explains what about the request’ parameters is
            invalid.

        """
        return None

    def make_request(self):
        """Generate a ``requests.Request`` from the current parameters.

        This method returns a ``requests.Request`` object ready for sending to
        the API server.

        Examples
        --------
        Get the URL that will be accessed for a request::

            >>> from six.moves.urllib.parse import urlparse
            >>> from wwt_api_client import Client
            >>> req = Client().show_image('My Image', 'http://example.com/space.jpg')
            >>> parsed_url = urlparse(req.make_request().prepare().url)
            >>> print(parsed_url.path)
            /WWTWeb/ShowImage.aspx

        Returns
        -------
        request : ``requests.Request`` object
            The HTTP request.

        """
        raise NotImplementedError()

    def send(self):
        """Issue the request and return its result.

        The request’s validity will be checked before sending.

        Examples
        --------
        Send a :ref:`ShowImage <endpoint-ShowImage>` request:

            >>> from wwt_api_client import Client
            >>> req = Client().show_image('My Image', 'http://example.com/space.jpg')
            >>> print(req.send()[:10])  # prints start of a WTML XML document
            <?xml vers

        Returns
        -------
        text : string
            The server response as text. (TODO: more return types!)

        Raises
        ------
        :class:`InvalidRequestError`
            Raised if the request parameters are invalid.
        :class:`APIResponseError`
            Raised if the API call results in an HTTP error code.

        """
        invalid = self.invalidity_reason()
        if invalid is not None:
            raise InvalidRequestError(invalid)

        resp = self._client.session.send(self.make_request().prepare())
        if not resp.ok:
            raise APIResponseError(resp.text)

        return resp.text


class ShowImageRequest(APIRequest):
    """Request a WTML XML document suitable for showing an image in a client.

    This request connects to the :ref:`ShowImage <endpoint-ShowImage>`
    endpoint. Perhaps counterintuitively, this API returns a `WTML collection
    <https://worldwidetelescope.gitbooks.io/worldwide-telescope-data-files-reference/content/collections.html>`_
    XML document that points to a single web-accessible image no larger than
    2048×2048 pixels. The XML document is a fairly straightforward
    transcription of the URL parameters that are passed to the API call.
    Therefore this API is most useful when you are using some *other* web API
    that requires a URL to a WTML file — by passing it a URL involving this
    endpoint, you can point at a “virtual” WTML file that tells WWT how to
    show an image.

    Only the ``name`` and ``image_url`` parameters are essential::

        >>> from wwt_api_client import Client
        >>> req = Client().show_image('My Image', 'http://example.com/space.jpg')
        >>> print(req.send()[:10])  # prints start of a WTML XML document
        <?xml vers

    The image to be shown must be less than 2048×2048 in size and should use a
    tangential projection.

    For details, see the documentation of the :ref:`ShowImage
    <endpoint-ShowImage>` endpoint.

    """
    credits = None
    "Free text describing where the image came from."

    credits_url = None
    "Absolute URL of a webpage with more information about the image."

    dec_deg = 0.0
    "The declination at which to center the view, in degrees."

    image_url = None
    "Absolute URL of the image to show."

    name = None
    """A name to give the image an its enclosing ``<Place>``. Commas will be
    stripped by the server.

    """
    ra_deg = 0.0
    "The right ascension at which to center the view, in degrees."

    reverse_parity = False
    "If true, the image will be flipped left-right before display."

    rotation_deg = 0.0
    "How much to rotate the image in an east-from-north sense, in degrees."

    scale = 1.0
    "The angular size of each image pixel, in arcseconds. Pixels must be square."

    thumbnail_url = None
    "Absolute URL of a 96×45 pixel image thumbnail used to represent the ``<Place>``."

    x_offset_pixels = 0.0
    "The horizontal offset of the image’s lower-left corner from the view center, in pixels."

    y_offset_pixels = 0.0
    "The vertical offset of the image’s lower-left corner from the view center, in pixels."

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

        if float(self.scale) == 0.:
            return '"scale" must not be zero'

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

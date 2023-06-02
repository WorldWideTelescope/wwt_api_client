# Copyright 2023 the .NET Foundation
# Distributed under the MIT license

"""
API client support for WWT Constellations images.
"""

import urllib.parse

from wwt_data_formats.folder import Folder
from wwt_data_formats.imageset import ImageSet

from . import CxClient
from .data import ImageApiPermissions, ImageInfo, ImageUpdate, _strip_nulls_in_place

__all__ = """
ImageClient
""".split()


class ImageClient:
    """
    A client for the WWT Constellations APIs calls related to a specific image.

    Parameters
    ----------
    client : :class:`~wwt_api_client.constellations.CxClient`
        The parent client for making API calls.
    id: str
        The ID of the image of interest.
    """

    client: CxClient
    _url_base: str

    def __init__(
        self,
        client: CxClient,
        id: str,
    ):
        self.client = client
        self._url_base = "/image/" + urllib.parse.quote(id)

    def get(self) -> ImageInfo:
        """
        Get information about this image.

        This method corresponds to the
        :ref:`endpoint-GET-image-_id` API endpoint.
        """
        resp = self.client._send_and_check(self._url_base, http_method="GET")
        resp = resp.json()
        resp.pop("error")
        return ImageInfo.schema().load(resp)

    def permissions(self) -> ImageApiPermissions:
        """
        Get information about the logged-in user's permissions with regards to
        this image.

        This method corresponds to the :ref:`endpoint-GET-image-_id-permissions`
        API endpoint. See that documentation for important guidance about when
        and how to use this API. In most cases you should not use it, and just
        go ahead and attempt whatever operation wish to perform.
        """
        resp = self.client._send_and_check(
            self._url_base + "/permissions", http_method="GET"
        )
        resp = resp.json()
        resp.pop("error")
        return ImageApiPermissions.schema().load(resp)

    def imageset_wtml_url(self) -> str:
        """
        Get a URL that will yield a WTML folder containing this image as an imageset.

        Returns
        -------
        The WTML URL.

        See Also
        --------
        imageset_folder, imageset_object
        """
        return f"{self.client._config.api_url}{self._url_base}/img.wtml"

    def imageset_folder(self) -> Folder:
        """
        Get a WWT WTML Folder object containing this image as an imageset.

        Returns
        -------
        :class:`wwt_data_formats.folder.Folder`

        See Also
        --------
        imageset_wtml_url, imageset_object
        """
        return Folder.from_url(self.imageset_wtml_url())

    def imageset_object(self) -> ImageSet:
        """
        Get a WWT WTML ImageSet object representing this image.

        Returns
        -------
        :class:`wwt_data_formats.imageset.ImageSet`

        See Also
        --------
        imageset_wtml_url, imageset_folder
        """
        return self.imageset_folder().children[0]

    def update(self, updates: ImageUpdate):
        """
        Update various attributes of this image.

        This method corresponds to the :ref:`endpoint-PATCH-image-_id` API
        endpoint.
        """
        resp = self.client._send_and_check(
            self._url_base,
            http_method="PATCH",
            json=_strip_nulls_in_place(updates.to_dict()),
        )
        resp = resp.json()
        resp.pop("error")
        # Might as well return the response, although it's currently vacuous
        return resp

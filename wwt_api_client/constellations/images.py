# Copyright 2023 the .NET Foundation
# Distributed under the MIT license

"""
API client support for WWT Constellations images.
"""

import urllib.parse

from wwt_data_formats.folder import Folder
from wwt_data_formats.imageset import ImageSet

from . import CxClient

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

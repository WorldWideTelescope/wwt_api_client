# Copyright 2023 the .NET Foundation
# Distributed under the MIT license

"""
API client support for WWT Constellations scenes.

Scenes are the individual "posts" that show one or more images.
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json
import urllib.parse

from wwt_data_formats.folder import Folder
from wwt_data_formats.place import Place

from . import CxClient
from .data import HandleInfo, SceneContentHydrated, ScenePlace

__all__ = """
GetSceneResponse
SceneClient
""".split()


@dataclass_json
@dataclass
class GetSceneResponse:
    id: str
    handle_id: str
    handle: HandleInfo
    creation_date: str
    likes: int
    place: ScenePlace
    content: SceneContentHydrated
    text: str


class SceneClient:
    """
    A client for the WWT Constellations APIs calls related to a specific scene.

    Parameters
    ----------
    client : :class:`~wwt_api_client.constellations.CxClient`
        The parent client for making API calls.
    id: str
        The ID of the scene of interest.
    """

    client: CxClient
    _url_base: str

    def __init__(
        self,
        client: CxClient,
        id: str,
    ):
        self.client = client
        self._url_base = "/scene/" + urllib.parse.quote(id)

    def get(self) -> GetSceneResponse:
        """
        Get information about this scene.

        This method corresponds to the
        :ref:`endpoint-GET-scene-_id` API endpoint.
        """
        resp = self.client._send_and_check(self._url_base, http_method="GET")
        resp = resp.json()
        resp.pop("error")
        return GetSceneResponse.schema().load(resp)

    def place_wtml_url(self) -> str:
        """
        Get a URL that will yield a WTML folder representing this scene as a WWT
        Place, if possible.

        Returns
        -------
        The WTML URL.

        Notes
        -----
        The API request will return a 404 error if the scene cannot be
        represented as a WWT Place (as well as if the scene ID is unrecognized).

        See Also
        --------
        place_folder, place_object
        """
        return f"{self.client._config.api_url}{self._url_base}/place.wtml"

    def place_folder(self) -> Folder:
        """
        Get a WWT WTML Folder object containing this scene as a WWT Place, if
        possible.

        Returns
        -------
        :class:`wwt_data_formats.folder.Folder`

        Notes
        -----
        The API request will return a 404 error if the scene cannot be
        represented as a WWT Place (as well as if the scene ID is unrecognized).

        See Also
        --------
        place_wtml_url, place_object
        """
        return Folder.from_url(self.place_wtml_url())

    def place_object(self) -> Place:
        """
        Get a WWT WTML Place object representing this scene, if possible.

        Returns
        -------
        :class:`wwt_data_formats.place.Place`

        Notes
        -----
        The API request will return a 404 error if the scene cannot be
        represented as a WWT Place (as well as if the scene ID is unrecognized).

        See Also
        --------
        place_wtml_url, place_folder
        """
        return self.place_folder().children[0]

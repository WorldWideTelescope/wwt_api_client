# Copyright 2023 the .NET Foundation
# Distributed under the MIT license

"""
API client support for WWT Constellations scenes.

Scenes are the individual "posts" that show one or more images.
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json
import urllib.parse

from . import CxClient
from .data import HandleInfo, ScenePlace

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

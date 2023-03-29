# Copyright 2023 the .NET Foundation
# Distributed under the MIT license

"""
API client support for WWT Constellations handles.

Handles are publicly visible "user" or "channel" names in Constellations.
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, Optional
import urllib.parse

from . import CxClient

__all__ = """
AddSceneRequest
HandleClient
SceneImageLayer
SceneContent
ScenePlace
""".split()


@dataclass_json
@dataclass
class ScenePlace:
    ra_rad: float
    dec_rad: float
    zoom_deg: float
    roll_rad: float


@dataclass_json
@dataclass
class SceneImageLayer:
    image_id: str
    opacity: float


@dataclass_json
@dataclass
class SceneContent:
    image_layers: Optional[List[SceneImageLayer]]


@dataclass_json
@dataclass
class AddSceneRequest:
    place: ScenePlace
    content: SceneContent
    outgoing_url: Optional[str]
    text: str


@dataclass_json
@dataclass
class AddSceneResponse:
    error: bool
    id: str
    rel_url: str


class HandleClient:
    """
    A client for the WWT Constellations APIs calls related to a specific handle.

    Parameters
    ----------
    client : :class:`~wwt_api_client.constellations.CxClient`
        The parent client for making API calls.
    handle: :class:`str`
        The handle to use for the API calls.
    """

    client: CxClient
    _url_base: str

    def __init__(
        self,
        client: CxClient,
        handle: str,
    ):
        self.client = client
        self._url_base = "/handle/" + urllib.parse.quote(handle)

    def add_scene(self, scene: AddSceneRequest) -> str:
        """
        Add a new scene owned by this handle.

        This method corresponds to the
        :ref:`endpoint-POST-handle-_handle-scene` API endpoint.
        """
        resp = self._send_and_check(
            self._url_base + "/scene", http_method="POST", json=scene.to_dict()
        )
        resp = AddSceneResponse.schema().load(resp.json())
        return resp.id

# Copyright 2023 the .NET Foundation
# Distributed under the MIT license

"""
API client support for WWT Constellations handles.

Handles are publicly visible "user" or "channel" names in Constellations.
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json
import math
from typing import List, Optional
import urllib.parse

from wwt_data_formats.place import Place

from . import CxClient, _strip_nulls_in_place

__all__ = """
AddSceneRequest
HandleClient
SceneImageLayer
SceneContent
ScenePlace
""".split()


H2R = math.pi / 15
D2R = math.pi / 180


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
        resp = self.client._send_and_check(
            self._url_base + "/scene",
            http_method="POST",
            json=_strip_nulls_in_place(scene.to_dict()),
        )
        resp = AddSceneResponse.schema().load(resp.json())
        return resp.id

    def add_scene_from_place(self, place: Place) -> str:
        """
        Add a new scene derived from a :class:`wwt_data_formats.place.Place`
        object.

        Parameters
        ----------
        place : :class:`wwt_data_formats.place.Place`
            The WWT place

        Remarks
        -------
        The imagesets referenced by the place must already have been imported
        into the Constellations framework.

        Not all of the Place information is preserved.
        """

        # The trick here is that we need to query the API to
        # get the ID(s) for the imageset(s)

        image_layers = []

        for iset in [
            place.background_image_set,
            place.image_set,
            place.foreground_image_set,
        ]:
            if iset is None:
                continue

            hits = self.client.find_images_by_wwt_url(iset.url)
            if not hits:
                raise Exception(
                    f"unable to find Constellations record for image URL `{iset.url}`"
                )

            image_layers.append(SceneImageLayer(image_id=hits[0].id, opacity=1.0))

        # Now we can build the rest

        api_place = ScenePlace(
            ra_rad=place.ra_hr * H2R,
            dec_rad=place.dec_deg * D2R,
            zoom_deg=place.zoom_level,
            roll_rad=place.rotation_deg * D2R,
        )

        content = SceneContent(image_layers=image_layers)

        req = AddSceneRequest(
            place=api_place,
            content=content,
            text=place.name,
            outgoing_url=None,
        )

        return self.add_scene(req)

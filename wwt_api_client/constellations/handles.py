# Copyright 2023 the .NET Foundation
# Distributed under the MIT license

"""
API client support for WWT Constellations handles.

Handles are publicly visible "user" or "channel" names in Constellations.
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json
import math
from typing import Optional
import urllib.parse

from wwt_data_formats.enums import DataSetType
from wwt_data_formats.imageset import ImageSet
from wwt_data_formats.place import Place

from . import CxClient
from .data import (
    HandleInfo,
    ImageWwt,
    ImageStorage,
    SceneContent,
    SceneImageLayer,
    ScenePlace,
    _strip_nulls_in_place,
)

__all__ = """
AddImageRequest
AddSceneRequest
HandleClient
""".split()


H2R = math.pi / 12
D2R = math.pi / 180


@dataclass_json
@dataclass
class AddImageRequest:
    wwt: ImageWwt
    storage: ImageStorage
    note: str


@dataclass_json
@dataclass
class AddImageResponse:
    id: str
    rel_url: str


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

    def get(self) -> HandleInfo:
        """
        Get basic information about this handle.

        This method corresponds to the
        :ref:`endpoint-GET-handle-_handle` API endpoint.
        """
        resp = self.client._send_and_check(self._url_base, http_method="GET")
        resp = resp.json()
        resp.pop("error")
        return HandleInfo.schema().load(resp)

    def add_image(self, image: AddImageRequest) -> str:
        """
        Add a new image owned by this handle.

        This method corresponds to the
        :ref:`endpoint-POST-handle-_handle-image` API endpoint.
        """
        resp = self.client._send_and_check(
            self._url_base + "/image",
            http_method="POST",
            json=_strip_nulls_in_place(image.to_dict()),
        )
        resp = resp.json()
        resp.pop("error")
        resp = AddImageResponse.schema().load(resp)
        return resp.id

    def add_image_from_set(self, imageset: ImageSet) -> str:
        """
        Add a new Constellations image derived from a
        :class:`wwt_data_formats.imageset.ImageSet` object.

        Parameters
        ----------
        imageset : :class:`wwt_data_formats.imageset.ImageSet`
            The WWT imageset.

        Notes
        -----
        Not all of the imageset information is preserved.
        """

        if imageset.data_set_type != DataSetType.SKY:
            raise ValueError(
                f"Constellations imagesets must be of Sky type; this is {imageset.data_set_type}"
            )
        if imageset.base_tile_level != 0:
            raise ValueError(
                f"Constellations imagesets must have base tile levels of 0"
            )

        api_wwt = ImageWwt(
            base_degrees_per_tile=imageset.base_degrees_per_tile,
            bottoms_up=imageset.bottoms_up,
            center_x=imageset.center_x,
            center_y=imageset.center_y,
            file_type=imageset.file_type,
            offset_x=imageset.offset_x,
            offset_y=imageset.offset_y,
            projection=imageset.projection.value,
            quad_tree_map=imageset.quad_tree_map or "",
            rotation=imageset.rotation_deg,
            tile_levels=imageset.tile_levels,
            width_factor=imageset.width_factor,
            thumbnail_url=imageset.thumbnail_url,
        )

        storage = ImageStorage(
            legacy_url_template=imageset.url,
        )

        req = AddImageRequest(
            wwt=api_wwt,
            storage=storage,
            note=imageset.name,
        )

        return self.add_image(req)

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
        resp = resp.json()
        resp.pop("error")
        resp = AddSceneResponse.schema().load(resp)
        return resp.id

    def add_scene_from_place(self, place: Place) -> str:
        """
        Add a new scene derived from a :class:`wwt_data_formats.place.Place`
        object.

        Parameters
        ----------
        place : :class:`wwt_data_formats.place.Place`
            The WWT place

        Notes
        -----
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

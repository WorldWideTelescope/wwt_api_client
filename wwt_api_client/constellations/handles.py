# Copyright 2023 the .NET Foundation
# Distributed under the MIT license

"""
API client support for WWT Constellations handles.

Handles are publicly visible "user" or "channel" names in Constellations.
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json
import html
import math
from typing import List, Optional
import urllib.parse

from wwt_data_formats.enums import DataSetType
from wwt_data_formats.imageset import ImageSet
from wwt_data_formats.place import Place

from . import CxClient, TimelineResponse
from .data import (
    HandleInfo,
    HandlePermissions,
    HandleStats,
    HandleUpdate,
    ImageWwt,
    ImageContentPermissions,
    ImageStorage,
    ImageSummary,
    SceneContent,
    SceneHydrated,
    SceneImageLayer,
    SceneInfo,
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


@dataclass_json(undefined="EXCLUDE")
@dataclass
class AddImageRequest:
    wwt: ImageWwt
    permissions: ImageContentPermissions
    storage: ImageStorage
    note: str
    alt_text: Optional[str] = None


@dataclass_json(undefined="EXCLUDE")
@dataclass
class AddImageResponse:
    id: str
    rel_url: str


@dataclass_json(undefined="EXCLUDE")
@dataclass
class AddSceneRequest:
    place: ScenePlace
    content: SceneContent
    text: str
    outgoing_url: Optional[str] = None


@dataclass_json(undefined="EXCLUDE")
@dataclass
class AddSceneResponse:
    id: str
    rel_url: str


@dataclass_json(undefined="EXCLUDE")
@dataclass
class ImageInfoResponse:
    total_count: int
    results: List[ImageSummary]


@dataclass_json(undefined="EXCLUDE")
@dataclass
class SceneInfoResponse:
    total_count: int
    results: List[SceneInfo]


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

        Returns
        -------
        A :class:`~wwt_api_client.constellations.data.HandleInfo` object.

        Notes
        -----
        This method corresponds to the
        :ref:`endpoint-GET-handle-_handle` API endpoint.
        """
        resp = self.client._send_and_check(self._url_base, http_method="GET")
        resp = resp.json()
        resp.pop("error")
        return HandleInfo.schema().load(resp)

    def permissions(self) -> HandlePermissions:
        """
        Get information about the logged-in user's permissions with regards to
        this handle.

        Returns
        -------
        A :class:`~wwt_api_client.constellations.data.HandlePermissions` object.

        Notes
        -----
        This method corresponds to the :ref:`endpoint-GET-handle-_handle-permissions`
        API endpoint. See that documentation for important guidance about when
        and how to use this API. In most cases you should not use it, and just
        go ahead and attempt whatever operation wish to perform.
        """
        resp = self.client._send_and_check(
            self._url_base + "/permissions", http_method="GET"
        )
        resp = resp.json()
        resp.pop("error")
        return HandlePermissions.schema().load(resp)

    def stats(self) -> HandleStats:
        """
        Get some statistics about this handle.

        Returns
        -------
        A :class:`~wwt_api_client.constellations.data.HandleStats` object.

        Notes
        -----
        This method corresponds to the :ref:`endpoint-GET-handle-_handle-stats`
        API endpoint. Only administrators of a handle can retrieve its stats.
        """
        resp = self.client._send_and_check(self._url_base + "/stats", http_method="GET")
        resp = resp.json()
        resp.pop("error")
        return HandleStats.schema().load(resp)

    def scene_info(
        self, page_num: int, page_size: Optional[int] = 10
    ) -> List[SceneInfo]:
        """
        Get administrative info about scenes belonging to this handle.

        Parameters
        ----------
        page_num : int
            Which page to retrieve. Page zero gives the most recently-created
            scenes, page one gives the next batch, etc.
        page_size : optinal int, defaults to 10
            The number of items per page to retrieve. Valid values are between
            1 and 100.

        Returns
        -------
        A list of :class:`~wwt_api_client.constellations.data.SceneInfo`
        items.

        Notes
        -----
        This method corresponds to the :ref:`endpoint-GET-handle-_handle-sceneinfo`
        API endpoint. Only administrators of a handle can retrieve the scene info.
        This API returns paginated results.
        """
        try:
            use_page_num = int(page_num)
            assert use_page_num >= 0
        except Exception:
            raise ValueError(f"invalid page_num argument {page_num!r}")

        try:
            use_page_size = int(page_size)
            assert use_page_size >= 1 and use_page_size <= 100
        except Exception:
            raise ValueError(f"invalid page_size argument {page_size!r}")

        resp = self.client._send_and_check(
            self._url_base + "/sceneinfo",
            http_method="GET",
            params={"page": use_page_num, "pagesize": use_page_size},
        )
        resp = resp.json()
        resp.pop("error")
        # For now (?) we just throw away the total count field
        return SceneInfoResponse.schema().load(resp).results

    def image_info(
        self, page_num: int, page_size: Optional[int] = 10
    ) -> List[ImageSummary]:
        """
        Get administrative info about images belonging to this handle.

        Parameters
        ----------
        page_num : int
            Which page to retrieve. Page zero gives the most recently-created
            images, page one gives the next batch, etc.
        page_size : optinal int, defaults to 10
            The number of items per page to retrieve. Valid values are between
            1 and 100.

        Returns
        -------
        A list of :class:`~wwt_api_client.constellations.data.ImageSummary`
        items.

        Notes
        -----
        This method corresponds to the :ref:`endpoint-GET-handle-_handle-imageinfo`
        API endpoint. Only administrators of a handle can retrieve the image info.
        This API returns paginated results.
        """
        try:
            use_page_num = int(page_num)
            assert use_page_num >= 0
        except Exception:
            raise ValueError(f"invalid page_num argument {page_num!r}")

        try:
            use_page_size = int(page_size)
            assert use_page_size >= 1 and use_page_size <= 100
        except Exception:
            raise ValueError(f"invalid page_size argument {page_size!r}")

        resp = self.client._send_and_check(
            self._url_base + "/imageinfo",
            http_method="GET",
            params={"page": use_page_num, "pagesize": use_page_size},
        )
        resp = resp.json()
        resp.pop("error")
        # For now (?) we just throw away the total count field
        return ImageInfoResponse.schema().load(resp).results

    def update(self, updates: HandleUpdate):
        """
        Update various attributes of this handle.

        Returns
        -------
        None.

        Notes
        -----
        This method corresponds to the :ref:`endpoint-PATCH-handle-_handle` API
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

    def add_image(self, image: AddImageRequest) -> str:
        """
        Add a new image owned by this handle.

        Returns
        -------
        The Constellations ID of the newly-created image, as a string.

        Notes
        -----
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

    def add_image_from_set(
        self,
        imageset: ImageSet,
        copyright: str,
        license_spdx_id: str,
        note: Optional[str] = None,
        credits: Optional[str] = None,
        alt_text: Optional[str] = None,
    ) -> str:
        """
        Add a new Constellations image derived from a
        :class:`wwt_data_formats.imageset.ImageSet` object.

        Parameters
        ----------
        imageset : :class:`wwt_data_formats.imageset.ImageSet`
            The WWT imageset.
        copyright : str
            The copyright statement for this image. Preferred form is along the
            lines of "Copyright 2020 Henrietta Swan Leavitt" or "Public domain".
            *Please* provide support in higher-level applications to allow users
            to input valid information here — the correct information for this
            field cannot be determined algorithmically. Note that under the
            world's current regime of intellectual property law, virtually every
            single image in WWT can be presumed to be copyrighted, with the
            major exception of images produced by employees of the US Federal
            government in the course of their duties.
        license_spdx_id : str
            The `SPDX License Identifier <https://spdx.org/licenses/>`_ of the
            license under which this image is made available through WWT. Use
            ``CC-PDDC`` for images in the public domain. For images with known
            licenses that are not in the SPDX list, use ``LicenseRef-$TEXT`` for
            some value of ``$TEXT``; see the `Other licensing information
            detected
            <https://spdx.github.io/spdx-spec/v2-draft/other-licensing-information-detected/>`_
            section of the SPDX specification.
        note : optional str, default None
            An internal note used to describe this image. This is not shown
            publicly. If unspecified, a default note is constructed from the
            imageset name and, if present, the credits URL.
        credits : optional str of restricted HTML text, default None
            Credits text for the image. If provided, this field should be
            encoded as HTML, with a limited set of tags (including ``<a>`` for
            hyperlinks) allowed. If unspecified, the ``credits`` field of the
            imageset is used. It will have HTML special characters (``<``,
            ``>``, and ``&``) escaped, under the assumption that its contents
            do *not* include any markup.
        alt_text : optional str, default None
            Optional "alt text" describing this image for visually impaired users.
            If unspecified, no alt text is provided.

        Returns
        -------
        The Constellations ID of the newly-created image, as a string.

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

        if credits is None:
            credits = html.escape(imageset.credits)

        permissions = ImageContentPermissions(
            copyright=copyright,
            credits=credits,
            license=license_spdx_id,
        )

        if note is None:
            note = imageset.name

            if imageset.credits_url:
                note += f" — {imageset.credits_url}"

        req = AddImageRequest(
            wwt=api_wwt,
            permissions=permissions,
            storage=storage,
            note=note,
            alt_text=alt_text,
        )

        return self.add_image(req)

    def add_scene(self, scene: AddSceneRequest) -> str:
        """
        Add a new scene owned by this handle.

        Returns
        -------
        The Constellations ID of the newly-created scene, as a string.

        Notes
        -----
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

        Returns
        -------
        The Constellations ID of the newly-created scene, as a string.

        Notes
        -----
        The imagesets referenced by the place must already have been imported
        into the Constellations framework.

        Not all of the Place information is preserved.
        """

        # The trick here is that we need to query the API to
        # get the ID(s) for the imageset(s)

        image_layers = []
        outgoing_url = None
        text = None

        for iset in [
            place.background_image_set,
            place.image_set,
            place.foreground_image_set,
        ]:
            if iset is None:
                continue

            if iset.credits_url is not None:
                outgoing_url = iset.credits_url

            if iset.description:
                # This field is not used by the stock WWT implementation but is
                # referenced in the original docs, and provided by
                # wwt_data_formats. So just in case one exists, we can start
                # using it.
                text = iset.description

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
            roll_rad=place.rotation_deg * D2R,
            roi_height_deg=place.zoom_level / 6,
            roi_aspect_ratio=1.0,
        )

        content = SceneContent(image_layers=image_layers)

        if place.description:
            text = place.description
        elif not text:
            text = place.name

        req = AddSceneRequest(
            place=api_place,
            content=content,
            text=text,
            outgoing_url=outgoing_url,
        )

        return self.add_scene(req)

    def get_timeline(self, page_num: int) -> List[SceneHydrated]:
        """
        Get information about a group of scenes on this handle's timeline.

        Parameters
        ----------
        page_num : int
            Which page to retrieve. Page zero gives the top items on the
            timeline, page one gives the next set, etc.

        Returns
        -------
        A list of :class:`~wwt_api_client.constellations.data.SceneHydrated`
        items.

        Notes
        -----
        The page size is not specified externally, nor is it guaranteed to be
        stable from one page to the next. If you care, look at the length of the
        list that you get back from an API.

        This method corresponds to the
        :ref:`endpoint-GET-handle-_handle-timeline` API endpoint.
        """
        try:
            use_page_num = int(page_num)
            assert use_page_num >= 0
        except Exception:
            raise ValueError(f"invalid page_num argument {page_num!r}")

        resp = self.client._send_and_check(
            self._url_base + "/timeline",
            http_method="GET",
            params={"page": use_page_num},
        )
        resp = resp.json()
        resp.pop("error")
        resp = TimelineResponse.schema().load(resp)
        return resp.results

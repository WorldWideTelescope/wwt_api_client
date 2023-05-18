# Copyright 2023 the .NET Foundation
# Distributed under the MIT license

"""
Data classes for WWT Constellations APIs.
"""

from typing import List, Optional

from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json

__all__ = """
HandleImageStats
HandleInfo
HandlePermissions
HandleSceneStats
HandleStats
HandleUpdate
ImageDisplayInfo
ImageStorage
ImageSummary
ImageWwt
SceneContent
SceneContentHydrated
SceneHydrated
SceneImageLayer
SceneImageLayerHydrated
SceneInfo
ScenePermissions
ScenePlace
ScenePreviews
SceneUpdate
""".split()


def _strip_nulls_in_place(d: dict):
    """
    Remove None values a dictionary and its sub-dictionaries.

    For the backend APIs, our convention is to have values be missing entirely
    rather than nulls; that's more future-proof if/when we add new fields to
    things.

    Returns the input for convenience.
    """

    keys_to_remove = []

    for key, val in d.items():
        if isinstance(val, dict):
            _strip_nulls_in_place(val)
        elif val is None:
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del d[key]

    return d


@dataclass_json
@dataclass
class HandleInfo:
    handle: str
    display_name: str


@dataclass_json
@dataclass
class HandlePermissions:
    handle: str
    view_dashboard: bool


@dataclass_json
@dataclass
class HandleUpdate:
    display_name: Optional[str]


@dataclass_json
@dataclass
class HandleImageStats:
    count: int


@dataclass_json
@dataclass
class HandleSceneStats:
    count: int
    impressions: int
    likes: int


@dataclass_json
@dataclass
class HandleStats:
    handle: str
    images: HandleImageStats
    scenes: HandleSceneStats


@dataclass_json
@dataclass
class ImageWwt:
    """A description of the WWT data parameters associated with a Constellations image."""

    base_degrees_per_tile: float
    bottoms_up: bool
    center_x: float
    center_y: float
    file_type: str
    offset_x: float
    offset_y: float
    projection: str
    quad_tree_map: str
    rotation: float
    tile_levels: int
    width_factor: int
    thumbnail_url: str


@dataclass_json
@dataclass
class ImageStorage:
    """A description of data storage associated with a Constellations image."""

    legacy_url_template: Optional[str]


@dataclass_json
@dataclass
class ImageSummary:
    """Summary information about a Constellations image."""

    id: str = field(metadata=config(field_name="_id"))  # 24 hex digits
    handle_id: str  # 24 hex digits
    creation_date: str  # format: 2023-03-28T16:53:18.364Z'
    note: str
    storage: ImageStorage


@dataclass_json
@dataclass
class ImagePermissions:
    copyright: str
    credits: Optional[str]
    license: str


@dataclass_json
@dataclass
class ImageDisplayInfo:
    wwt: ImageWwt
    storage: ImageStorage


@dataclass_json
@dataclass
class ScenePlace:
    ra_rad: float
    dec_rad: float
    roll_rad: float
    roi_height_deg: float
    roi_aspect_ratio: float


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
class SceneImageLayerHydrated:
    image: ImageDisplayInfo
    opacity: float


@dataclass_json
@dataclass
class SceneContentHydrated:
    background: Optional[ImageDisplayInfo]
    image_layers: Optional[List[SceneImageLayerHydrated]]


@dataclass_json
@dataclass
class ScenePreviews:
    video: Optional[str]
    thumbnail: Optional[str]


@dataclass_json
@dataclass
class SceneHydrated:
    id: str
    handle_id: str
    handle: HandleInfo
    creation_date: str
    likes: int
    place: ScenePlace
    content: SceneContentHydrated
    text: str
    previews: ScenePreviews


@dataclass_json
@dataclass
class SceneInfo:
    _id: str
    creation_date: str
    impressions: int
    likes: int


@dataclass_json
@dataclass
class ScenePermissions:
    id: str
    edit: bool


@dataclass_json
@dataclass
class SceneUpdate:
    outgoing_url: Optional[str]
    place: Optional[ScenePlace]
    text: Optional[str]

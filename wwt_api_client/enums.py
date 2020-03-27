# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
# Licensed under the MIT License.

"""Various enumerations.

From ``wwt-website/WWTMVC5/Models/Enum.cs``

"""
from __future__ import absolute_import, division, print_function

__all__ = '''
CategoryType
CommunityType
ContentType
EntityType
HighlightType
PermissionsTab
UserRole
'''.split()

from enum import Enum

class CategoryType(Enum):
    ALL = 'All'
    SOLID_EARTH = 'SolidEarth'
    ANCIENT_EARTH = 'AncientEarth'
    ATMOSPHERE = 'Atmosphere'
    CLIMATE = 'Climate'
    ASTRONOMY = 'Astronomy'
    OCEANS_RIVERS = 'OceansRivers'
    COLD_REGIONS = 'ColdRegions'
    PLANETS = 'Planets'
    GENERAL_INTEREST = 'GeneralInterest'
    HOW_TO = 'HowTo'
    LIFE_SCIENCE = 'LifeScience'
    EARTH_SCIENCE = 'EarthScience'
    NEBULA = 'Nebula'
    GALAXIES = 'Galaxies'
    SURVEYS = 'Surveys'
    BLACK_HOLES = 'BlackHoles'
    SUPERNOVA = 'Supernova'
    STAR_CLUSTERS = 'StarClusters'
    MARS = 'Mars'
    OTHER = 'Other'
    WWT = 'WWT'
    COSMIC_EVENTS = 'CosmicEvents'
    EDUCATORS = 'Educators'


class CommunityType(Enum):
    NONE = 'None'
    COMMUNITY = 'Community'
    FOLDER = 'Folder'
    USER = 'User'


class ContentType(Enum):
    ALL = 'All'
    NONE = 'None'
    TOURS = 'Tours'
    WTML = 'Wtml'
    EXCEL = 'Excel'
    DOC = 'Doc'
    PPT = 'Ppt'
    LINK = 'Link'
    GENERIC = 'Generic'
    WWTL = 'Wwtl'
    VIDEO = 'Video'


class EntityType(Enum):
    ALL = 'All'
    COMMUNITY = 'Community'
    FOLDER = 'Folder'
    CONTENT = 'Content'
    USER = 'User'


class HighlightType(Enum):
    NONE = ''
    FEATURED = 'Featured'
    LATEST = 'Latest'
    POPULAR = 'Popular'
    RELATED = 'Related'
    MOST_DOWNLOADED = 'MostDownloaded'


class PermissionsTab(Enum):
    """Weird name inherited from wwt-website."""

    NONE = 'None'
    USERS = 'Users'
    REQUESTS = 'Requests'
    PROFILE_REQUESTS = 'ProfileRequests'


class UserRole(Enum):
    NONE = 'None'
    VISITOR = 'Visitor'
    READER = 'Reader'
    CONTRIBUTOR = 'Contributor'
    MODERATOR = 'Moderator'
    MODERATOR_INHERITED = 'ModeratorInherited'
    OWNER = 'Owner'
    SITE_ADMIN = 'SiteAdmin'

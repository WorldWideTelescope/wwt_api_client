# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the .Net Foundation
# Distributed under the terms of the revised (3-clause) BSD license.

"""Note! This test suite will hit the network!

"""
import math
import pytest
from xml.etree import ElementTree

from .. import Client


def xml_trees_equal(e1, e2):
    "From https://stackoverflow.com/a/24349916/3760486"

    if e1.tag != e2.tag:
        return False
    if e1.text != e2.text:
        return False
    if e1.tail != e2.tail:
        return False
    if e1.attrib != e2.attrib:
        return False
    if len(e1) != len(e2):
        return False

    return all(xml_trees_equal(c1, c2) for c1, c2 in zip(e1, e2))

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def showimage(client):
    "Return a valid ShowImage request object."
    return client.show_image('name', 'http://localhost/image.jpg')

SHOWIMAGE_BAD_SETTINGS = [
    ('credits', b'\xff not unicodable'),
    ('credits_url', u'http://olé/not_ascii_unicode_url'),
    ('credits_url', b'http://host/\x81/not_ascii_bytes_url'),
    ('credits_url', 'not_absolute_url'),
    ('dec_deg', -90.00001),
    ('dec_deg', 90.00001),
    ('dec_deg', math.nan),
    ('dec_deg', math.inf),
    ('dec_deg', 'not numeric'),
    ('image_url', None),
    ('image_url', u'http://olé/not_ascii_unicode_url'),
    ('image_url', b'http://host/\x81/not_ascii_bytes_url'),
    ('image_url', 'not_absolute_url'),
    ('name', None),
    ('ra_deg', math.nan),
    ('ra_deg', math.inf),
    ('ra_deg', 'not numeric'),
    ('reverse_parity', 1),  # only bools allowed
    ('reverse_parity', 't'),  # only bools allowed
    ('rotation_deg', math.nan),
    ('rotation_deg', math.inf),
    ('rotation_deg', 'not numeric'),
    ('scale', 0.),
    ('scale', math.nan),
    ('scale', math.inf),
    ('scale', 'not numeric'),
    ('thumbnail_url', u'http://olé/not_ascii_unicode_url'),
    ('thumbnail_url', b'http://host/\x81/not_ascii_bytes_url'),
    ('thumbnail_url', 'not_absolute_url'),
    ('x_offset_pixels', math.nan),
    ('x_offset_pixels', math.inf),
    ('x_offset_pixels', 'not numeric'),
    ('y_offset_pixels', math.nan),
    ('y_offset_pixels', math.inf),
    ('y_offset_pixels', 'not numeric'),
]

@pytest.mark.parametrize(('attr', 'val'), SHOWIMAGE_BAD_SETTINGS)
def test_showimage_invalid_settings(showimage, attr, val):
    setattr(showimage, attr, val)
    assert showimage.invalidity_reason() is not None

SHOWIMAGE_GOOD_SETTINGS = [
    ('credits', b'unicodable bytes'),
    ('credits', u'unicode é'),
    ('credits', None),
    ('credits_url', b'http://localhost/absolute_bytes_url'),
    ('credits_url', u'//localhost/absolute_unicode_url'),
    ('credits_url', None),
    ('dec_deg', -90),
    ('dec_deg', 90),
    ('image_url', b'http://localhost/absolute_bytes_url'),
    ('image_url', u'//localhost/absolute_unicode_url'),
    ('name', b'unicodable bytes'),
    ('name', u'unicode é'),
    ('ra_deg', -720.),
    ('ra_deg', 980.),
    ('reverse_parity', False),
    ('reverse_parity', True),
    ('rotation_deg', -1),
    ('scale', -1.),
    ('thumbnail_url', b'http://localhost/absolute_bytes_url'),
    ('thumbnail_url', u'//localhost/absolute_unicode_url'),
    ('thumbnail_url', None),
    ('x_offset_pixels', -1.),
    ('x_offset_pixels', 0),
    ('y_offset_pixels', -1.),
    ('y_offset_pixels', 0),
]

@pytest.mark.parametrize(('attr', 'val'), SHOWIMAGE_GOOD_SETTINGS)
def test_showimage_valid_settings(showimage, attr, val):
    setattr(showimage, attr, val)
    assert showimage.invalidity_reason() is None


SHOWIMAGE_BASIC_RESULT = '''
<?xml version="1.0" encoding="UTF-8"?>
<Folder Name="Objéct" Group="Goto">
 <Place Name="Objéct" RA="0" Dec="0" ZoomLevel="0" DataSetType="Sky" Opacity="100"
        Thumbnail="" Constellation="">
  <ForegroundImageSet>
   <ImageSet DataSetType="Sky" BandPass="Visible" Url="http://localhost/image.jpg"
             TileLevels="0" WidthFactor="2" Rotation="0" Projection="SkyImage"
             FileType=".tif" CenterY="0" CenterX="0" BottomsUp="False" OffsetX="0"
             OffsetY="0" BaseTileLevel="0" BaseDegreesPerTile="0.000277777777777778">
    <Credits></Credits>
    <CreditsUrl></CreditsUrl>
   </ImageSet>
  </ForegroundImageSet>
 </Place>
</Folder>
'''

SHOWIMAGE_RESULTS = [
    (dict(), SHOWIMAGE_BASIC_RESULT),
]

@pytest.mark.parametrize(('attrs', 'expected'), SHOWIMAGE_RESULTS)
def test_showimage_valid_settings(showimage, attrs, expected):
    expected = ElementTree.fromstring(expected)

    for name, value in attrs.items():
        setattr(showimage, name, value)

    found_text = showimage.send()
    found = ElementTree.fromstring(found_text)
    assert xml_trees_equal(expected, found)

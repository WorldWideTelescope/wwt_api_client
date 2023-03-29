# -*- mode: python; coding: utf-8 -*-
# Copyright 2019-2023 the .Net Foundation
# Distributed under the MIT license

"""Note! This test suite will hit the network!

"""
import pytest
from xml.etree import ElementTree

from .. import Client


INF = float("inf")
NAN = float("nan")


def _assert_xml_trees_equal(path, e1, e2, care_text_tags):
    "Derived from https://stackoverflow.com/a/24349916/3760486"

    assert e1.tag == e2.tag, "at XML path {0}, tags {1} and {2} differed".format(
        path, e1.tag, e2.tag
    )

    # We only sometimes care about this; often it's just whitespace
    if e1.tag in care_text_tags:
        assert (
            e1.text == e2.text
        ), "at XML path {0}, texts {1!r} and {2!r} differed".format(
            path, e1.text, e2.text
        )

    # We never care about this, right?
    # assert e1.tail == e2.tail, \
    #    'at XML path {0}, tails {1!r} and {2!r} differed'.format(path, e1.tail, e2.tail)

    assert (
        e1.attrib == e2.attrib
    ), "at XML path {0}, attributes {1!r} and {2!r} differed".format(
        path, e1.attrib, e2.attrib
    )
    assert len(e1) == len(
        e2
    ), "at XML path {0}, number of children {1} and {2} differed".format(
        path, len(e1), len(e2)
    )

    subpath = "{0}>{1}".format(path, e1.tag)

    for c1, c2 in zip(e1, e2):
        _assert_xml_trees_equal(subpath, c1, c2, care_text_tags)


def assert_xml_trees_equal(e1, e2, care_text_tags=()):
    _assert_xml_trees_equal("(root)", e1, e2, care_text_tags)


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def login(client):
    "Return a valid login request object."
    return client.login()


def test_login_basic(login):
    assert login.invalidity_reason() is None
    login.send()


@pytest.fixture
def showimage(client):
    "Return a valid ShowImage request object."
    return client.show_image("http://localhost/image.jpg", "name")


SHOWIMAGE_BAD_SETTINGS = [
    ("credits", b"\xff not unicodable"),
    ("credits_url", "http://olé/not_ascii_unicode_url"),
    ("credits_url", b"http://host/\x81/not_ascii_bytes_url"),
    ("credits_url", "not_absolute_url"),
    ("dec_deg", -90.00001),
    ("dec_deg", 90.00001),
    ("dec_deg", NAN),
    ("dec_deg", INF),
    ("dec_deg", "not numeric"),
    ("image_url", None),
    ("image_url", "http://olé/not_ascii_unicode_url"),
    ("image_url", b"http://host/\x81/not_ascii_bytes_url"),
    ("image_url", "not_absolute_url"),
    ("name", None),
    ("ra_deg", NAN),
    ("ra_deg", INF),
    ("ra_deg", "not numeric"),
    ("reverse_parity", 1),  # only bools allowed
    ("reverse_parity", "t"),  # only bools allowed
    ("rotation_deg", NAN),
    ("rotation_deg", INF),
    ("rotation_deg", "not numeric"),
    ("scale_arcsec", 0.0),
    ("scale_arcsec", NAN),
    ("scale_arcsec", INF),
    ("scale_arcsec", "not numeric"),
    ("thumbnail_url", "http://olé/not_ascii_unicode_url"),
    ("thumbnail_url", b"http://host/\x81/not_ascii_bytes_url"),
    ("thumbnail_url", "not_absolute_url"),
    ("x_offset_pixels", NAN),
    ("x_offset_pixels", INF),
    ("x_offset_pixels", "not numeric"),
    ("y_offset_pixels", NAN),
    ("y_offset_pixels", INF),
    ("y_offset_pixels", "not numeric"),
]


@pytest.mark.parametrize(("attr", "val"), SHOWIMAGE_BAD_SETTINGS)
def test_showimage_invalid_settings(showimage, attr, val):
    setattr(showimage, attr, val)
    assert showimage.invalidity_reason() is not None


SHOWIMAGE_GOOD_SETTINGS = [
    ("credits", b"unicodable bytes"),
    ("credits", "unicode é"),
    ("credits", None),
    ("credits_url", b"http://localhost/absolute_bytes_url"),
    ("credits_url", "//localhost/absolute_unicode_url"),
    ("credits_url", None),
    ("dec_deg", -90),
    ("dec_deg", 90),
    ("image_url", b"http://localhost/absolute_bytes_url"),
    ("image_url", "//localhost/absolute_unicode_url"),
    ("name", b"unicodable bytes"),
    ("name", "unicode é"),
    ("ra_deg", -720.0),
    ("ra_deg", 980.0),
    ("reverse_parity", False),
    ("reverse_parity", True),
    ("rotation_deg", -1),
    ("scale_arcsec", -1.0),
    ("thumbnail_url", b"http://localhost/absolute_bytes_url"),
    ("thumbnail_url", "//localhost/absolute_unicode_url"),
    ("thumbnail_url", None),
    ("x_offset_pixels", -1.0),
    ("x_offset_pixels", 0),
    ("y_offset_pixels", -1.0),
    ("y_offset_pixels", 0),
]


@pytest.mark.parametrize(("attr", "val"), SHOWIMAGE_GOOD_SETTINGS)
def test_showimage_valid_settings(showimage, attr, val):
    setattr(showimage, attr, val)
    assert showimage.invalidity_reason() is None


SHOWIMAGE_CARE_TEXT_TAGS = set(("Credits", "CreditsUrl"))


def _make_showimage_result(credurl="", name="name"):
    return """<?xml version="1.0" encoding="UTF-8"?>
<Folder Name="{name}" Group="Goto">
 <Place Name="{name}" RA="0" Dec="0" ZoomLevel="0" DataSetType="Sky" Opacity="100"
        Thumbnail="" Constellation="">
  <ForegroundImageSet>
   <ImageSet DataSetType="Sky" BandPass="Visible" Url="http://localhost/image.jpg"
             TileLevels="0" WidthFactor="2" Rotation="0" Projection="SkyImage"
             FileType=".tif" CenterY="0" CenterX="0" BottomsUp="False" OffsetX="0"
             OffsetY="0" BaseTileLevel="0" BaseDegreesPerTile="0.0002777777777777778">
    <Credits></Credits>
    <CreditsUrl>{credurl}</CreditsUrl>
   </ImageSet>
  </ForegroundImageSet>
 </Place>
</Folder>
""".format(
        credurl=credurl, name=name
    )


SHOWIMAGE_RESULTS = [
    (dict(), _make_showimage_result()),
    (dict(name='test&xml"esc'), _make_showimage_result(name="test&amp;xml&quot;esc")),
    (
        dict(credits_url="http://a/b&c"),
        _make_showimage_result(credurl="http://a/b&amp;c"),
    ),
]


@pytest.mark.parametrize(("attrs", "expected"), SHOWIMAGE_RESULTS)
def test_showimage_valid_settings(showimage, attrs, expected):
    expected = ElementTree.fromstring(expected)

    for name, value in attrs.items():
        setattr(showimage, name, value)

    found_text = showimage.send()
    found = ElementTree.fromstring(found_text)
    assert_xml_trees_equal(expected, found, SHOWIMAGE_CARE_TEXT_TAGS)


@pytest.fixture
def tileimage(client):
    "Return a valid TileImage request object."
    return client.tile_image(
        "http://www.spitzer.caltech.edu/uploaded_files/images/0009/0848/sig12-011.jpg"
    )


TILEIMAGE_BAD_SETTINGS = [
    ("credits", b"\xff not unicodable"),
    ("credits_url", "http://olé/not_ascii_unicode_url"),
    ("credits_url", b"http://host/\x81/not_ascii_bytes_url"),
    ("credits_url", "not_absolute_url"),
    ("dec_deg", -90.00001),
    ("dec_deg", 90.00001),
    ("dec_deg", NAN),
    ("dec_deg", INF),
    ("dec_deg", "not numeric"),
    ("image_url", None),
    ("image_url", "http://olé/not_ascii_unicode_url"),
    ("image_url", b"http://host/\x81/not_ascii_bytes_url"),
    ("image_url", "not_absolute_url"),
    ("ra_deg", NAN),
    ("ra_deg", INF),
    ("ra_deg", "not numeric"),
    ("rotation_deg", NAN),
    ("rotation_deg", INF),
    ("rotation_deg", "not numeric"),
    ("scale_deg", 0.0),
    ("scale_deg", NAN),
    ("scale_deg", INF),
    ("scale_deg", "not numeric"),
    ("thumbnail_url", "http://olé/not_ascii_unicode_url"),
    ("thumbnail_url", b"http://host/\x81/not_ascii_bytes_url"),
    ("thumbnail_url", "not_absolute_url"),
    ("x_offset_deg", NAN),
    ("x_offset_deg", INF),
    ("x_offset_deg", "not numeric"),
    ("y_offset_deg", NAN),
    ("y_offset_deg", INF),
    ("y_offset_deg", "not numeric"),
]


@pytest.mark.parametrize(("attr", "val"), TILEIMAGE_BAD_SETTINGS)
def test_tileimage_invalid_settings(tileimage, attr, val):
    setattr(tileimage, attr, val)
    assert tileimage.invalidity_reason() is not None


TILEIMAGE_GOOD_SETTINGS = [
    ("credits", b"unicodable bytes"),
    ("credits", "unicode é"),
    ("credits", None),
    ("credits_url", b"http://localhost/absolute_bytes_url"),
    ("credits_url", "//localhost/absolute_unicode_url"),
    ("credits_url", None),
    ("dec_deg", 90),
    ("dec_deg", 90),
    ("dec_deg", None),
    ("image_url", b"http://localhost/absolute_bytes_url"),
    ("image_url", "//localhost/absolute_unicode_url"),
    ("ra_deg", -720.0),
    ("ra_deg", 980.0),
    ("ra_deg", None),
    ("rotation_deg", -1),
    ("rotation_deg", None),
    ("scale_deg", -1.0),
    ("scale_deg", None),
    ("thumbnail_url", b"http://localhost/absolute_bytes_url"),
    ("thumbnail_url", "//localhost/absolute_unicode_url"),
    ("thumbnail_url", None),
    ("x_offset_deg", -1.0),
    ("x_offset_deg", 0),
    ("x_offset_deg", None),
    ("y_offset_deg", -1.0),
    ("y_offset_deg", 0),
    ("y_offset_deg", None),
]


@pytest.mark.parametrize(("attr", "val"), TILEIMAGE_GOOD_SETTINGS)
def test_tileimage_valid_settings(tileimage, attr, val):
    setattr(tileimage, attr, val)
    assert tileimage.invalidity_reason() is None


TILEIMAGE_CARE_TEXT_TAGS = set(("Credits", "CreditsUrl"))


def _make_tileimage_result(credits="", credurl="", ident=None, name="Image File"):
    return """<Folder Name="{name}" Group="Explorer">
  <Place Name="{name}" RA="0" Dec="0" ZoomLevel="32768" DataSetType="Sky"
         Opacity="100" Thumbnail="http://www.worldwidetelescope.org/wwtweb/tilethumb.aspx?name={ident}"
         Constellation="">
    <ForegroundImageSet>
      <ImageSet DataSetType="Sky" Name="{name}" BandPass="Visible"
                Url="http://www.worldwidetelescope.org/wwtweb/GetTile.aspx?q={{1}},{{2}},{{3}},{ident}"
                TileLevels="5" WidthFactor="1" Rotation="0" Projection="Tan" FileType=".png"
                CenterY="0" CenterX="0" BottomsUp="False" OffsetX="0" OffsetY="0"
                BaseTileLevel="0" BaseDegreesPerTile="8192">
        <Credits>{credits}</Credits>
        <CreditsUrl>{credurl}</CreditsUrl>
        <ThumbnailUrl>http://www.worldwidetelescope.org/wwtweb/tilethumb.aspx?name={ident}</ThumbnailUrl>
      </ImageSet>
    </ForegroundImageSet>
  </Place>
</Folder>
""".format(
        credits=credits, credurl=credurl, ident=ident, name=name
    )


TILEIMAGE_RESULTS = [
    (
        dict(),
        _make_tileimage_result(
            credits=" NASA/JPL-Caltech",
            credurl="http://www.spitzer.caltech.edu/images/5259-sig12-011-The-Helix-Nebula-Unraveling-at-the-Seams",
            ident="1176481368",
            name="Helix Nebula",
        ),
    ),
]


@pytest.mark.parametrize(("attrs", "expected"), TILEIMAGE_RESULTS)
def test_tileimage_valid_settings(tileimage, attrs, expected):
    expected = ElementTree.fromstring(expected)

    for name, value in attrs.items():
        setattr(tileimage, name, value)

    found_text = tileimage.send()
    found = ElementTree.fromstring(found_text)
    assert_xml_trees_equal(expected, found, TILEIMAGE_CARE_TEXT_TAGS)

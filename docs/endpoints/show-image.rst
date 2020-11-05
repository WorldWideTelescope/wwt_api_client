.. _endpoint-ShowImage:

``WWTWeb/ShowImage.aspx``
=========================

This API returns a `WTML collection
<https://docs.worldwidetelescope.org/data-guide/1/data-file-formats/collections/>`_
XML document that points to a single web-accessible image no larger than
2048×2048 pixels. The XML document is a fairly straightforward transcription
of the URL parameters that are passed to the API call. Therefore this API is
most useful when you are using some *other* web API that requires a URL to a
WTML file — by passing it a URL involving this endpoint, you can point at a
“virtual” WTML file that tells WWT how to show an image.

The WTML document returned by this API has the following structure, where the
items enclosed in curly braces have textual substitutions applied::

    <?xml version="1.0" encoding="UTF-8"?>
    <Folder Name="{name}" Group="Goto">
      <Place Name="{name}" RA="{ra}" Dec="{dec}" ZoomLevel="{zoom}"
             DataSetType="Sky" Opacity="100" Thumbnail="{thumb}"
             Constellation="">
        <ForegroundImageSet>
          <ImageSet DataSetType="Sky" BandPass="Visible" Url="{url}"
                    TileLevels="0" WidthFactor="2" Rotation="{rotation}"
                    Projection="SkyImage" FileType=".tif" CenterY="{cy}"
                    CenterX="{cx}" BottomsUp="{bottomsup}" OffsetX="{dx}"
                    OffsetY="{dy}" BaseTileLevel="0"
                    BaseDegreesPerTile="{scale}">
            <Credits>{credits}</Credits>
            <CreditsUrl>{creditsurl}</CreditsUrl>
          </ImageSet>
        </ForegroundImageSet>
      </Place>
    </Folder>

Query Parameters
----------------

The ``WWTWeb/ShowImage.aspx`` endpoint processes the following URL query
parameters:

=================  ===========  =========  =======
Name               Type         Required?  Summary
=================  ===========  =========  =======
``credits``        Free text               Brief description of where the image came from.
``creditsUrl``     URL                     URL to a webpage with more information about the image.
``debug``          Existential             If set, response is delivered as ``text/plain`` with no HTTP headers.
``dec``            Degrees                 Declination at which to center the view; nominally the image center.
``imageurl``       URL                     The image to load.
``name``           Free text    yes        User-facing name for the image.
``ra``             Degrees                 Right ascension at which to center the view; nominally the image center.
``reverseparity``  Existential             If provided, the image is flipped horizontally
``rotation``       Degrees                 How much to rotate the image in an east-from-north sense, plus 180 degrees.
``scale``          Arcseconds              The angular size of each image pixel (assumed square).
``thumb``          URL                     URL to a 96×45 pixel thumbnail image for this image.
``wtml``           Existential             If *unset*, the API returns a redirect to ``default.aspx`` rathern than XML.
``x``              Pixels                  The horizontal offset of the image *corner* from the view center.
``y``              Pixels                  The vertical offset of the image *corner* from the view center.
=================  ===========  =========  =======

Some details:

``debug``
  Do not use this parameter. It is only documented to point out that supplying
  it will change the behavior of the API call.

``dec``
  Defaults to 0. *Clipped* to lie between -90 and 90.

``imageurl``
  This parameter is technically not required, but the API call makes little
  sense without it.

``name``
  Commas will be stripped out from this parameter.

``ra``
  Defaults to 0. *Clipped* to lie between 0 and 360.

``reverseparity``
  Causes the image to be mirrored *left-right* before any rotation is applied.
  To cause a mirror to be flipped top-bottom, which is usually what’s desired,
  combine this parameter with a rotation of 180°.

``rotation``
  If left unspecified, the ``Rotation`` parameter in the resulting WTML file
  will be 1 degree. Otherwise, the parameter in the resulting WTML file will
  be whatever is passed in, *minus 180 degrees*. Therefore you should almost
  always specify this as 180.

``scale``
  Mis-documented in the WTML reference, I think. Defaults to 1. The format
  only allows for square pixels.

``wtml``
  Always set this parameter to ``true``. Otherwise the API call will issue a
  redirect intended for user-facing applications.

``x``
  Mis-documented in the WTML reference, I think. Defaults to 0, which means
  that the coordinate center of the image is taken to land on its left edge. A
  value equal to the image’s width in pixels means that the coordinate center
  lands on its right edge. Therefore, in the common case that you want the
  view to be centered on the image, ``x`` should be about half of the image
  width in pixels.

``y``
  Mis-documented in the WTML reference, I think. Defaults to 0, which means
  that the coordinate center of the image is taken to land on its bottom edge.
  A value equal to the image’s height in pixels means that the coordinate
  center lands on its top edge. Therefore, in the common case that you want
  the view to be centered on the image, ``y`` should be about half of the
  image height in pixels.

The ``ZoomLevel`` of the ``<Place>`` element is set to ``scale * y / 360``.
When navigating the ``<Place>`` specified in a WTML file, the ``ZoomLevel`` is
six times the height of the client FOV in degrees. In the baseline case that
``y`` is half of the image height, this means that the final client FOV will
be 83% (5/6) of the image height. If ``y`` is not close to half of the image
height, the discrepancy will be different.

Textual items are not XML-escaped before being inserted into the XML document,
so callers of this API should do the necessary escaping themselves.

URLs are not validated in any way by the API, but it is safest if all
passed-in URLs are absolute.

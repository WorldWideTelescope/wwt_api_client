.. _endpoint-TileImage:

``WWTWeb/TileImage.aspx``
=========================

This API fetches an image from a URL, tiles it on the server side, and returns
a `WTML collection
<https://docs.worldwidetelescope.org/data-guide/1/data-file-formats/collections/>`_
XML document that describes the resulting dataset and allow it to be displayed
in a client.

The WTML document returned by this API has the following structure, where the
items enclosed in curly braces have textual substitutions applied *except* for
the ``{1},{2},{3}`` in the ``ImageSet`` URL::

    <?xml version="1.0" encoding="UTF-8"?>
    <Folder Name="{name}" Group="Explorer">
      <Place Name="{name}" RA="{ra_hr}" Dec="{dec}" ZoomLevel="{zoom}"
             DataSetType="Sky" Opacity="100" Thumbnail="{thumb_url}"
             Constellation="">
        <ForegroundImageSet>
          <ImageSet DataSetType="Sky" Name="{name}" BandPass="Visible"
                    Url="http://www.worldwidetelescope.org/wwtweb/GetTile.aspx?q={1},{2},{3},{ident}"
                    TileLevels="{levels}" WidthFactor="1" Rotation="{rot}"
                    Projection="Tan" FileType=".png" CenterY="{dec}"
                    CenterX="{ra_deg}" BottomsUp="{flip}" OffsetX="{dx}"
                    OffsetY="{dy}" BaseTileLevel="0"
                    BaseDegreesPerTile="{scale}">
            <Credits>{credits}</Credits>
            <CreditsUrl>{credits_url}</CreditsUrl>
            <ThumbnailUrl>{thumb_url}</ThumbnailUrl>
          </ImageSet>
        </ForegroundImageSet>
      </Place>
    </Folder>


Query Parameters
----------------

The ``WWTWeb/TileImage.aspx`` endpoint processes the following URL query
parameters:

=================  ===========  =========  =======
Name               Type         Required?  Summary
=================  ===========  =========  =======
``credits``        Free text               Brief description of where the image came from.
``creditsUrl``     URL                     URL to a webpage with more information about the image.
``debug``          Existential             If set, response is delivered as ``text/plain`` with no HTTP headers.
``dec``            Degrees                 Declination at which to center the view; nominally the image center.
``imageurl``       URL                     The image to load.
``ra``             Degrees                 Right ascension at which to center the view; nominally the image center.
``reverseparity``  Existential             Do not provide this parameter.
``rotation``       Degrees                 How much to rotate the image in an east-from-north sense, plus 180 degrees.
``scale``          Degrees                 The angular size of each image pixel (assumed square).
``thumb``          URL                     URL to a 96×45 pixel thumbnail image for this image.
``x``              Degrees                 The horizontal offset between the image and view centers.
``y``              Degrees                 The vertical offset between the image and view centers.
=================  ===========  =========  =======

Some details:

``credits``
  Defaults to the empty string.

``creditsURL``
  Defaults to the value of the tag ``ReferenceURL`` inside the image AVM tags,
  if available, otherwise the empty string.

``debug``
  Do not use this parameter. It is only documented to point out that supplying
  it will change the behavior of the API call.

``dec``
  Defaults to the second value of the tag ``Spatial.ReferenceValue`` inside
  the image AVM tags, if available, otherwise 0. *Clipped* to lie between -90
  and 90.

``imageurl``
  This is actually optional! If not provided, will default to
  ``http://www.spitzer.caltech.edu/uploaded_files/images/0009/0848/sig12-011.jpg``.

``ra``
  Defaults to the first value of the tag ``Spatial.ReferenceValue`` inside the
  image AVM tags, if available, otherwise 0. *Clipped* to lie between 0
  and 360.

``reverseparity``
  This is presumably supposed to flip the image vertically. However, in my
  experimentation, providing this keyword prevents the image from being
  displayed in either the Windows or the Web clients. So, don’t use it.

``rotation``
  If specified as a parameter to the API call, the parameter in the resulting
  WTML file will be that parameter *minus 180 degrees*. If left unspecified,
  will be derived from AVM tags in the image in the following way. If the AVM
  contains a node ``Spatial.Rotation``, the *negation* of that value will be
  used. Otherwise, if the XMPP RDF contains an *attribute* named
  ``avm:Spatial.Rotation``, the negation of that value will be used.
  Otherwise, if the AVM contains ``Spatial.CDMatrix``, the rotation will be
  derived from that matrix assuming that it can be decomposed into a rotation
  and separate X and Y scalings.

``scale``
  If specified as a parameter to the API call, the height of each image pixel
  in degrees should be given. Note that this uses different units than the
  :ref:`ShowImage <endpoint-ShowImage>` endpoint. Pixels are assumed to be
  square. If left unspecified, ``scale`` will be derived from the image AVM
  tags in the following way. If the AVM contains a node ``Spatial.Scale``, the
  second value contained in that sequence will be used. Otherwise, if the AVM
  contains ``Spatial.CDMatrix``, the scale will be derived from that matrix
  assuming that it can be decomposed into a rotation and separate X and Y
  scalings. The scale may be adjusted if the actual image height differs from
  that described in the image metadata.

``thumb``
  If not specified, will default to a string of the form
  ``http://www.worldwidetelescope.org/wwtweb/tilethumb.aspx?name={ident}``, which
  will return a thumbnail image derived from the tiled image.

``x``
  Defaults to 0. Note that this parameter has different units and semantics than
  the :ref:`ShowImage <endpoint-ShowImage>` endpoint.

``y``
  Defaults to 0. Note that this parameter has different units and semantics than
  the :ref:`ShowImage <endpoint-ShowImage>` endpoint.

The API intends to support a ``name`` parameter, but its implementation is
broken such that it only is activated if ``debug`` is provided. The name used
in the WTML output is the first text item in the ``dc:subject/rdf:Bag`` node
of the image AVM, if available, otherwise the text ``Image File``.

The ``ZoomLevel`` of the ``<Place>`` element is set to four times the height
of the tiled image, which is the power of 2 as big or bigger than the image
height. When navigating the ``<Place>`` specified in a WTML file, the
``ZoomLevel`` is six times the height of the client FOV in degrees, so the
resulting FOV will lie somewhere between 2/3 and 4/3 of the height of the
image of interest.

The ``{ident}`` corresponding to the tiled image is derived from the C# hash
function of the image URL string. This function is not cryptographic and
therefore hash collisions are a plausible outcome.

Textual items are not XML-escaped before being inserted into the XML document,
so callers of this API should do the necessary escaping themselves.

URLs are not validated in any way by the API, but it is safest if all
passed-in URLs are absolute.


Tiling Implementation
---------------------

When invoked, the API will determine an identifier number from the image URL.
(This is the ``{ident}`` mentioned above.) If no cached version of the image
is available on the server, as identified by the unique identifier, the image
will be downloaded. *The server does not currently support HTTPS connections.*
Also, the hashing scheme used to compute the image identifier is not strong,
and so hash collisions are a plausible outcome. If this happens, the tiled
image data will correspond to the colliding image, not the one you intend.

Images should be parsable using C#'s ``System.Drawing.Bitmap`` class.
Supported file formats should be BMP, GIF, JPG, PNG, and TIFF. If the image
cannot be loaded, an empty response with no error code will be returned.

Regardless of whether the image was downloaded fresh or not, the server will
parse the image file for AVM information and create tiles using the
``System.Drawing.Bitmap`` resampling algorithms. Therefore, this API can take
a minute or two to execute. If you intend to use the resulting WTML file
repeatedly, it will be desirable to cache it elsewhere.

Cache expiration policies on the server are unspecified; assume that tiled
images will be cached indefinitely. Therefore, if your image file changes at
all, you should assign it a new URL when making this API call. Note, however,
that the parameters returned in the WTML content are not cached, so if your
underlying image file is not changing, you can tweak URL parameters without
needing to alter your image’s URL.

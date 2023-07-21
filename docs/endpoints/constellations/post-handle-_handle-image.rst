.. _endpoint-POST-handle-_handle-image:

==========================
POST /handle/:handle/image
==========================

This API creates a new Constellations image owned by the specified handle.


Authorization
=============

The request must be made by an account that has permissions to add new images
to the associated handle.


Request Structure
=================

The URL parameter ``:handle`` is the handle that will own the image.

The structure of the request is:

.. code-block:: javascript

  {
    "wwt": {
      // See the `wwt_data_formats` documentation for definitions of these fields
      "base_degrees_per_tile": $number,
      "bottoms_up": $boolean,
      "center_x": $number,
      "center_y": $number,
      "file_type": $string,
      "offset_x": $number,
      "offset_y": $number,
      "projection": $string,
      "quad_tree_map": $string,
      "rotation": $number,
      "thumbnail_url": $string,
      "tile_levels": $number(int),
      "width_factor": $number(int),
    },
    "permissions": {
      // Free plain text giving the copyright statement for this image. Preferred form is
      // along the lines of "Copyright 2020 Henrietta Swan Leavitt" or "Public
      // domain". *Please* provide support in higher-level applications to allow
      // users to input valid information here — the correct information for this
      // field cannot be determined algorithmically. Note that under the world's
      // current regime of intellectual property law, virtually every single image
      // in WWT can be presumed to be copyrighted, with the major exception of
      // images produced by employees of the US Federal government in the course of
      // their duties.
      "copyright": $string,

      // HTML content giving credits to be shown when displaying this image. This is
      // different information than the copyright statement, which specifies who
      // "owns" the image. The credits have no legal significance, except that
      // some images are licensed in a way that requires that specific credit texts
      // are shown alongside them.
      //
      // Only a subset of HTML is allowed here. Allowed tags are `<a>`, `<b>`, `<br>`,
      // `<em>`, `<i>`, and `<strong>`.
      "credits": $string?,

      // The SPDX License Identifier (https://spdx.org/licenses/) of the license
      // under which this image is made available through WWT. Use `CC-PDDC` for
      // images in the public domain. For images with known licenses that are not
      // in the SPDX list, use `LicenseRef-$TEXT` for some value of `$TEXT`; see
      // the "Other licensing information detected" section of the SPDX
      // specification
      // (https://spdx.github.io/spdx-spec/v2-draft/other-licensing-information-detected/).
      "license": $string,
    },
    "storage": {
      // For now, this is the only valid storage type:
      "legacy_url_template": $string // This image's legacy URL
    },
    "note": $string, // Freeform text describing the image; not generally exposed
  }


Response Structure
==================

The structure of the response is:

.. code-block:: javascript

  {
    "error": $bool // Whether an error occurred
    "id": $string(objectID), // the ID of the newly-created image
    "rel_url": $string, // the API-relative URL used to access this image; `/image/:id`
  }

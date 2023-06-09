.. _endpoint-GET-image-_id:

==============
GET /image/:id
==============

This API gets basic information about a specific WWT image.


Request Structure
=================

The request takes no content. The ``:id`` URL parameter gives the ID of the
image to query.


Response Structure
==================

The structure of the response is:

.. code-block:: javascript

  {
    "error": $bool // Whether an error occurred
    "id": $string(objectID), // the ID of this image
    "handle_id": $string(objectID), // the ID of this images's owner
    "handle": { // Information about the owning handle
      "handle": $string, // the unique handle name
      "display_name": $string, // the handle's display name
    },
    "creation_date": $string(iso8601), // the date this image was created
    "wwt": {
      // Astrometric/data fields used by WWT, as in `POST /handle/:handle/image`;
      // see the `wwt_data_formats` documentation for definitions of these fields
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
      // Permissions information; see `POST /handle/:handle/image` for specification.
      "copyright": $string,
      "credits": $string?,
      "license": $string,
    },
    "storage": {
      // Data storage information as in `POST /handle/:handle/image`
      // For now, this is the only valid storage type:
      "legacy_url_template": $string // This image's legacy URL
    },
    "note": $string, // A textual note associated with this image
  }

See :ref:`endpoint-post-handle-_handle-image` for definitions of the contents of the inner
image fields.
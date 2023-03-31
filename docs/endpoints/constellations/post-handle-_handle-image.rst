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
    "storage": {
      // For now, this is the only valid storage type:
      "legacy_url_template": $string // This image's legacy URL
    }
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

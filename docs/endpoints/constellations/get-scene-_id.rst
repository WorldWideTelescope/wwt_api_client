.. _endpoint-GET-scene-_id:

==============
GET /scene/:id
==============

This API gets basic information about a specific WWT scene.


Request Structure
=================

The request takes no content. The ``:id`` URL parameter gives the ID of the
scene to query.


Response Structure
==================

The structure of the response is:

.. code-block:: javascript

  {
    "error": $bool // Whether an error occurred
    "id": $string(objectID), // the ID of this scene
    "handle_id": $string(objectID), // the ID of this scenes's owner
    "handle": { // Information about the owning handle
      "handle": $string, // the unique handle name
      "display_name": $string, // the handle's display name
    },
    "creation_date": $string(iso8601), // the date this scene was created
    "likes": $number, // the number of likes this scene has received
    "place": { // WWT camera information associated with this scene
      // See "POST /handle/:handle/scene" docs for descriptions:
      "ra_rad": $number,
      "dec_rad": $number,
      "zoom_deg": $number,
      "roll_rad": $number,
    },
    "content": { // The contents of this scene
      // Eventually, multiple content forms will likely be supported.
      // For now, the only one is:
      "image_layers": [
        // List of "hydrated" image layer records:
        {
          "image": {
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
            }
            "storage": {
              // Data storage information as in `POST /handle/:handle/image`
              // For now, this is the only valid storage type:
              "legacy_url_template": $string // This image's legacy URL
            }
          },
          "opacity": $number, // between 0 and 1
        }
      ],
    },
    "text": $string, // The text associated with this scene
    "outgoing_url": $string(URL)?, // optional outgoing URL associated with this scene
  }

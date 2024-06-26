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
    "likes": $int, // the number of likes this scene has received
    "liked": $bool, // whether the logged-in user has "liked" this scene
    "impressions": $int, // the number of impressions this scene has received
    "clicks": $int?, // the number of user clicks on the outgoing URL
    "shares": $int?, // the number of times users have activated the share-link flow for this scene
    "place": { // WWT camera information associated with this scene
      // See "POST /handle/:handle/scene" docs for descriptions:
      "ra_rad": $number,
      "dec_rad": $number,
      "roll_rad": $number,
      "roi_height_deg": $number,
      "roi_aspect_ratio": $number,
    },
    "content": { // The contents of this scene
      // Eventually, multiple content forms will likely be supported.
      // For now, the only one is the `image_layers` structure.
      "image_layers": [
        // List of "hydrated" image layer records:
        {
          "image": {
            "id": $string, // the ID of this image
            "wwt": { ... },
            "permissions": { ... },
            "storage": { ... },
          },
          "opacity": $number, // between 0 and 1
        }
      ],
      "background": {
        // Another "hydrated" image record:
        "id": $string, // the ID of this image
        "wwt": { ... },
        "permissions": { ... },
        "storage": { ... },
      },
    },
    "text": $string, // The text associated with this scene
    "outgoing_url": $string(URL)?, // optional outgoing URL associated with this scene
    "astropix": {
      // Optional information about this scene's association with an AstroPix image
      "publisher_id": $string, // the AstroPix image's publisher_id
      "image_id": $string, // the AstroPix image's image_id
    }
  }

See :ref:`endpoint-post-handle-_handle-image` for definitions of the contents of the inner
image fields.
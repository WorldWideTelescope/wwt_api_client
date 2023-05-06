.. _endpoint-POST-handle-_handle-scene:

==========================
POST /handle/:handle/scene
==========================

This API creates a new Constellations “scene” owned by the specified handle.


Authorization
=============

The request must be made by an account that has permissions to add new scenes
to the associated handle.


Request Structure
=================

The URL parameter ``:handle`` is the handle that will own the scene.

The structure of the request is:

.. code-block:: javascript

  {
    "place": {
      "ra_rad": $number, // The RA of the final camera position for this scene, in radians
      "dec_rad": $number, // The dec. of the final camera position for this scene, in radians
      "roll_rad": $number, // The roll of the final camera position, in radians
      "roi_height_deg": $number, // The height of the region of interest, in degrees
      "roi_aspect_ratio": $number, // The aspect ratio (width / height) of the region of interest
    },
    "content": {
      "image_layers": [
        // An optional list of image layers that comprise this scene.
        // Right now this field is not optional because it is the only supported scene
        // type, but that might change.
        {
          "image_id": $string(objectID), // the database ID of the image in question
          "opacity": $number, // the opacity of the final image display, between 0 and 1
        }
      ]
    },
    "outgoing_url": $string?, // A "see more" URL associated with this scene
    "text": $string, // Freeform text describing the scene
  }


Response Structure
==================

The structure of the response is:

.. code-block:: javascript

  {
    "error": $bool // Whether an error occurred
    "id": $string(objectID), // the ID of the newly-created scene
    "rel_url": $string, // the API-relative URL used to access this scene; `/scene/:id`
  }

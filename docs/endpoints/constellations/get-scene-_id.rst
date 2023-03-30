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
    "text": $string, // The text associated with this scene
    "outgoing_url": $string(URL)?, // optional outgoing URL associated with this scene
  }
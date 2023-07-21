.. _endpoint-POST-scene-_id-likes:

=====================
POST /scene/:id/likes
=====================

This API attempts to record a “like” for the specified scene.

In order to succeed, the request must include a valid session cookie from the
WWT Constellations website, and various rate-limiting and self-consistency
measures apply.


Request Structure
=================

The request takes no content. The ``:id`` URL parameter gives the ID of the
scene to update.


Response Structure
==================

The response is as follows:

.. code-block:: javascript

  {
    "error": $bool // Whether an error occurred
    "id": $string, // the ID of the scene that was updated
    "update": $boolean, // whether a like was actually recorded
  }

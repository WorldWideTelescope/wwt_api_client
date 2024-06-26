.. _endpoint-PATCH-scene-_id:

================
PATCH /scene/:id
================

This API updates various attributes of the specified scene.


Authorization
=============

The request must be made by an account that has permissions to make *all* of the
requested modifications. If any of the requested modifications are disallowed,
the entire operation fails.


Request Structure
=================

The URL parameter ``:id`` is the ID of the scene to modify.

The structure of the request is:

.. code-block:: javascript

  {
    "text": $string?,  // New textual content for the scene
    "outgoing_url": $string?,  // New outgoing URL for the scene
    "place": $Place?, // New place information for the scene
    "content": $Content?, // New content information for the scene
    "published": $bool?, // New setting for publication flag
    "astropix": {
      // Optional dict associating this scene with an AstroPix image. Only user accounts
      // with the "manage-astropix" role may set or modify this information.
      "publisher_id": $string,
      "image_id": $string,
    }
  }

For the definition of substructures such as ``Place``, see
:ref:`endpoint-POST-handle-_handle-scene`.


Response Structure
==================

The structure of the response is:

.. code-block:: javascript

  {
    "error": $bool // Whether an error occurred
  }

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
  }


Response Structure
==================

The structure of the response is:

.. code-block:: javascript

  {
    "error": $bool // Whether an error occurred
  }

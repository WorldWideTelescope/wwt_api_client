.. _endpoint-PATCH-image-_id:

================
PATCH /image/:id
================

This API updates various attributes of the specified image.


Authorization
=============

The request must be made by an account that has permissions to make *all* of the
requested modifications. If any of the requested modifications are disallowed,
the entire operation fails.


Request Structure
=================

The URL parameter ``:id`` is the ID of the image to modify.

The structure of the request is:

.. code-block:: javascript

  {
    // New textual note attached to the image
    "note": $string?,

    // See docs for POST /handle/:handle/image for a description of
    // the permissions object.
    "permissions": $object?,
  }

For the definition of substructures such as ``permissions``, see
:ref:`endpoint-POST-handle-_handle-image`.


Response Structure
==================

The structure of the response is:

.. code-block:: javascript

  {
    "error": $bool // Whether an error occurred
  }

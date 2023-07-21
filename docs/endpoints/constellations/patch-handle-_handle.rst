.. _endpoint-PATCH-handle-_handle:

=====================
PATCH /handle/:handle
=====================

This API updates various attributes of the specified handle.


Authorization
=============

The request must be made by an account that has permissions to make *all* of the
requested modifications. If any of the requested modifications are disallowed,
the entire operation fails.


Request Structure
=================

The URL parameter ``:handle`` is the handle that will be modified.

The structure of the request is:

.. code-block:: javascript

  {
    "display_name": $string?,  // A new display name for the handle
  }


Response Structure
==================

The structure of the response is:

.. code-block:: javascript

  {
    "error": $bool // Whether an error occurred
  }

.. _endpoint-GET-handle-_handle:

===================
GET /handle/:handle
===================

This API gets basic information about a specific Constellations handle


Request Structure
=================

The request takes no content. The ``:handle`` URL parameter gives the name of
the handle to query.


Response Structure
==================

The structure of the response is:

.. code-block:: javascript

  {
    "handle": $string, // the unique handle name
    "display_name": $string, // the handle's display name
  }

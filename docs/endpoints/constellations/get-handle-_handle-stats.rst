.. _endpoint-GET-handle-_handle-stats:

=========================
GET /handle/:handle/stats
=========================

This API returns some statistics about the specified handle.


Authorization
=============

The request must be made by an account that has administrative permissions on
the specified handle.


Request Structure
=================

The request takes no content. The ``:handle`` URL parameter gives the handle to
query.


Response Structure
==================

The response is as follows:

.. code-block:: javascript

  {
    "error": $bool // Whether an error occurred
    "handle": $string, // the handle that was queried
    "images": {
      "count": $int, // the number of images owned by this handle
    },
    "scenes": {
      "count": $int, // the number of scenes owned by this handle
      "impressions": $int, // the total number of impressions received by this handle's scenes
      "likes": $int, // the total number of likes received by this handle's scenes
    },
  }

.. _endpoint-GET-handle-_handle-sceneinfo:

=============================
GET /handle/:handle/sceneinfo
=============================

This API returns some statistics about scenes owned by the specified handle.


Authorization
=============

The request must be made by an account that has administrative permissions on
the specified handle.


Request Structure
=================

The request takes no content. The ``:handle`` URL parameter gives the handle to
query.

The ``page`` query parameter is an integer giving a page number of the
collection to query. Page zero gives the most recently-created scenes owned by
the handle, page one gives the next most recent batch, and so on. If
unspecified, it defaults to zero.

The ``pagesize`` query parameter is an integer giving a number of items per
page. Valid values are between 1 and 100. If unspecified, it defaults to ten.


Response Structure
==================

The response is as follows:

.. code-block:: javascript

  {
    "error": $bool, // Whether an error occurred
    "total_count": $int, // the total number of items in the collection
    "results": [
      // One record for each scene in the page of results:
      {
        "_id": $string, // the ID of this scene
        "creation_date": $string[iso8601], // the creation date of this scene in ISO8601 format
        "impressions": $int, // the number of impressions this scene has received
        "likes": $int, // the number of likes this scene has received
      }
    ]
  }

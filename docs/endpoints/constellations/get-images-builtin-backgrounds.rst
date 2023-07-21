.. _endpoint-GET-images-builtin-backgrounds:

===============================
GET /images/builtin-backgrounds
===============================

This API returns a list of images that constitute the set of built-in background
images suggested to users.


Request Structure
=================

The request takes no content.


Response Structure
==================

The structure of the response is:

.. code-block:: javascript

  {
    "error": $bool // Whether an error occurred
    "results": [
      // List of image display objects:
      {
        "_id": $string(objectID), // the ID of this image in the database
        "handle_id": $string(objectID), // the ID of this image's owner
        "creation_date": $string(iso8601), // the date this image record was created
        "note": $string, // freeform text associated with the image
        "storage": {
          "legacy_url_template": $string // This image's legacy URL
        }
      }
    ]
  }

See :ref:`endpoint-post-handle-_handle-image` for definitions of the contents of
the inner fields.

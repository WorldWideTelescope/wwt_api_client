.. _endpoint-POST-images-find-by-legacy-url:

===============================
POST /images/find-by-legacy-url
===============================

This API returns a list of images associated with a specified WWT “legacy” URL.
This functionality can be used to figure out which Constellations content is
associated with legacy WWT content.


Request Structure
=================

The structure of the request is:

.. code-block:: javascript

  {
    "wwt_legacy_url": $string // The URL to search for
  }


Response Structure
==================

The structure of the response is:

.. code-block:: javascript

  {
    "error": $bool // Whether an error occurred
    "results": [
      // List of zero or more image summary objects:
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

In this API call, the ``legacy_url_template`` in each response item will be
equal to the ``wwt_legacy_url`` in the input.

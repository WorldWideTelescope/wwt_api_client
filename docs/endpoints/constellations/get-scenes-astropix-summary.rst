.. _endpoint-GET-scenes-astropix-summary:

============================
GET /scenes/astropix-summary
============================

This API gets a summary of associations between Constellations scenes and images
in the `AstroPix`_ service. This API is generally available, but only expected
to be useful for the AstroPix web server, which can use it to know which
AstroPix images have associated WWT images.

.. _AstroPix: https://www.astropix.org/


Request Structure
=================

The request takes no content.


Response Structure
==================

The structure of the response is:

.. code-block:: javascript

  {
    "error": $bool, // whether an error occurred
    "result": {
      // Outer dictionary of associations, keyed by AstroPix publisher ID
      $publisher_id(str): {
        // Inner dictionary of associations, keyed by AstroPix image ID
        $image_id(str): [
          $wwt_handle(str),  // The WWT Constellations handle of the associated scene, with at-sign
          $wwt_scene_id(str) // The WWT Constellations ID of the associated scene
        ],
      }
    }
  }

For instance, in a world where there were only three WWT scenes associated with
AstroPix content, the result might be:

.. code-block:: javascript

  {
    "error": false,
    "result": {
      "eso": {
        "eso0209g": ["@eso", "6426ed2448ae71323babb17a"],
        "eso0622a": ["@eso", "6426ed2448ae71323babb18b"]
      },
      "ensci": {
        "euclid20231107a": ["@euclid", "647a0909cd45eb52a07076b4"]
      }
    }
  }

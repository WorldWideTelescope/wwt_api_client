.. _endpoint-GET-scenes-home-timeline:

=========================
GET /scenes/home-timeline
=========================

This API gets a list of scenes in the user's "home" timeline.


Request Structure
=================

The ``page`` query parameter is an integer giving a page number of timeline
entries to query. Page zero gives the most recent scenes on the timeline, page
one gives the next most recent batch, and so on. If unspecified, it defaults to
zero.


Response Structure
==================

The structure of the response is:

.. code-block:: javascript

  {
    "error": $bool, // whether an error occurred
    "results": [
      // This list contains a series of "hydrated" scene records
      // as described in the docs for `GET /scene/:id`.
    ]
  }

See :ref:`endpoint-GET-scene-_id` for a description of the ``results`` contents.

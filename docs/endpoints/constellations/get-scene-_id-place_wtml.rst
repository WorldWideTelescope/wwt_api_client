.. _endpoint-GET-scene-_id-place_wtml:

=========================
GET /scene/:id/place.wtml
=========================

This API returns a WTML document expressing this scene as a WWT Place data
structure, if possible.


Request Structure
=================

The request takes no content. The ``:id`` URL parameter gives the ID of the
scene to query.


Response Structure
==================

The response is a WTML folder containing one Place record. It can be parsed
with a package like `wwt_data_formats`_, as implemented in Python methods such
as :meth:`wwt_api_client.constellations.scenes.SceneClient.place_folder`.

.. _wwt_data_formats: https://wwt-data-formats.readthedocs.io/

If the scene cannot be represented as a WWT Place, a 404 Not Found HTTP error is
returned.

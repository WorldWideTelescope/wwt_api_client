.. _endpoint-GET-image-_id-img_wtml:

=======================
GET /image/:id/img.wtml
=======================

This API returns a WTML document expressing this image as a WWT ImageSet data
structure.


Request Structure
=================

The request takes no content. The ``:id`` URL parameter gives the ID of the
image to query.


Response Structure
==================

The response is a WTML folder containing one ImageSet record. It can be parsed
with a package like `wwt_data_formats`_, as implemented in Python methods such
as :meth:`wwt_api_client.constellations.images.ImageClient.imageset_folder`.

.. _wwt_data_formats: https://wwt-data-formats.readthedocs.io/
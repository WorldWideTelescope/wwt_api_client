===================================================================
wwt_api_client: Pythonic access to WorldWide Telescope web services
===================================================================

AAS `WorldWide Telescope <http://worldwidetelescope.org/home>`_ is a free
and powerful visualization engine developed by the `American Astronomical
Society <https://aas.org/>`_ that can display astronomical and planetary data.
This engine is powered by a large (multi-terabyte) collection of astronomical
survey data stored in the cloud. The `wwt_api_client`_ package allows you to
invoke the web APIs that constitute the WWT backend API.

.. _wwt_api_client: https://wwt-api-client.readthedocs.io/


Narrative Documentation
=======================

.. toctree::
   :maxdepth: 2

   installation


Python API Reference
====================

.. toctree::
   :maxdepth: 1

   api/wwt_api_client
   api/wwt_api_client.communities
   api/wwt_api_client.constellations
   api/wwt_api_client.constellations.data
   api/wwt_api_client.constellations.handles
   api/wwt_api_client.constellations.images
   api/wwt_api_client.constellations.scenes
   api/wwt_api_client.enums


Web Endpoint API Reference
==========================

Constellations API endpoints:

.. toctree::
   :maxdepth: 1

   endpoints/constellations/get-handle-_handle
   endpoints/constellations/patch-handle-_handle
   endpoints/constellations/post-handle-_handle-image
   endpoints/constellations/get-handle-_handle-imageinfo
   endpoints/constellations/get-handle-_handle-permissions
   endpoints/constellations/post-handle-_handle-scene
   endpoints/constellations/get-handle-_handle-sceneinfo
   endpoints/constellations/get-handle-_handle-stats
   endpoints/constellations/get-handle-_handle-timeline
   endpoints/constellations/get-image-_id
   endpoints/constellations/patch-image-_id
   endpoints/constellations/get-image-_id-img_wtml
   endpoints/constellations/get-image-_id-permissions
   endpoints/constellations/get-images-builtin-backgrounds
   endpoints/constellations/post-images-find-by-legacy-url
   endpoints/constellations/get-scene-_id
   endpoints/constellations/patch-scene-_id
   endpoints/constellations/post-scene-_id-impressions
   endpoints/constellations/post-scene-_id-likes
   endpoints/constellations/delete-scene-_id-likes
   endpoints/constellations/get-scene-_id-permissions
   endpoints/constellations/get-scene-_id-place_wtml
   endpoints/constellations/get-scenes-home-timeline
   endpoints/constellations/post-session-init

Legacy WWT APIs:

.. toctree::
   :maxdepth: 1

   endpoints/legacy/login
   endpoints/legacy/show-image
   endpoints/legacy/tile-image

Legacy Communities APIs:

- *The Communities service is deprecated and unsupported. See the
  wwt_api_client.communities module for best-effort implementations of these
  APIs.*


Getting help
============

If you run into any issues when using ``wwt_api_client``, please open an issue
`on its GitHub repository
<https://github.com/WorldWideTelescope/wwt_api_client/issues>`_.


Acknowledgments
===============

`wwt_api_client`_ is part of the `AAS`_ `WorldWide Telescope`_ system, a
`.NET Foundation`_ project managed by the non-profit `American Astronomical
Society`_ (AAS). Work on WWT has been supported by the AAS, the US `National
Science Foundation`_ (grants 1550701_, 1642446_, and 2004840_), the `Gordon and Betty
Moore Foundation`_, and `Microsoft`_.

.. _.NET Foundation: https://dotnetfoundation.org/
.. _AAS: https://aas.org/
.. _American Astronomical Society: https://aas.org/
.. _National Science Foundation: https://www.nsf.gov/
.. _1550701: https://www.nsf.gov/awardsearch/showAward?AWD_ID=1550701
.. _1642446: https://www.nsf.gov/awardsearch/showAward?AWD_ID=1642446
.. _2004840: https://www.nsf.gov/awardsearch/showAward?AWD_ID=2004840
.. _Gordon and Betty Moore Foundation: https://www.moore.org/
.. _Microsoft: https://www.microsoft.com/


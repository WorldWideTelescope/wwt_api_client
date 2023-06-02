.. _endpoint-POST-session-init:

==================
POST /session/init
==================

This API initializes the WWT Constellations session cookie for session tracking.


Request Structure
=================

The request takes no content.


Response Structure
==================

The response content is vacuous JSON:

.. code-block:: javascript

  {
    "error": false
  }

The more important aspect of the response is that it will include a
``Set-Cookie`` header that sets a session cookie.

.. _endpoint-GET-handle-_handle-permissions:

===============================
GET /handle/:handle/permissions
===============================

This API returns JSON capturing the logged-in user's permissions with regards to
the specified handle.

The returned information is purely advisory. The final arbiters of what is
actually allowed are the checks implemented for the actual APIs. Furthermore, it
is always possible that the results of this API call end up being out-of-date by
the time that you attempt to act on them. So in almost all circumstances, you
should ignore this API and just attempt the operation that you want to attempt,
and handle any errors that might happen. This API should only be used to
construct UIs that may choose to hide or show certain elements based on the
user's permissions.


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
    "view_dashboard": $boolean, // whether the user can view the handle's admin "dashboard'
  }

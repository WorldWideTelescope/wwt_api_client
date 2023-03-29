.. _endpoint-Login:

``WWTWeb/Login.aspx``
=====================

Windows clients invoke this API when they boot up. They send advisory version
information to the server. The server returns compatibility information that
the clients use to recommend or require updates.

Query Parameters
----------------

The ``WWTWeb/Login.aspx`` endpoint processes the following URL query
parameters:

===========  ==============  =========  =======
Name         Type            Required?  Summary
===========  ==============  =========  =======
``user``     GUID            No         A GUID associated with this user
``Version``  Version string  No         The version number of the client logging in
``Equinox``  Existential     No         If present, indicates a non-ancient client
===========  ==============  =========  =======

The ``user`` and ``Version`` are purely advisory and are not verified in any
way. In particular, the GUID is not coordinated with WWT Communities
activities. These values may be logged for diagnostic purposes.

The ``Equinox`` parameter should always be set to ``true``. The WWT “Equinox”
release came out in 2008, and all subsequent Windows client versions set it to
true.

Reponse Format
--------------

The reponse is plain text. For ``Equinox`` clients, the response may look like::

  ClientVersion:5.5.3.1
  DataVersion:330
  Message:
  WarnVersion:5.5.0.1
  MinVersion:2.2.32.1
  UpdateUrl:https://wwtweb.blob.core.windows.net/drops/WWTSetup.5.5.03.msi

For ancient clients, the response looks like::

  ClientVersion:2.2.32.1
  DataVersion:225
  Message:

  WarnVersion:2.2.31.1
  MinVersion:2.2.32.1
  UpdateUrl:http://content.worldwidetelescope.org/equinox/wwtequinoxsetup.msi

Modern (post-Equinox) Windows clients parse the response in the following way:

- The response is split on ``\n`` characters.
- The first line must start with ``ClientVersion:``; the text after the colon
  is the “latest version”. This version, and all others, have four
  dot-separated components as in the examples above.
- The second line must start with ``DataVersion:``; the text after the colon
  is the “data version”.
- The text after the colon on the third line is the “message”.
- If there are more than three lines, the text after the colon on the fourth
  line is the “warn version”; otherwise the warn version is the latest
  version.
- If there are more than four lines, the text after the colon on the fifth
  line is the “minimum version”; otherwise the minimum version is the latest
  version.
- If there are more than five lines, the text after the colon on the sixth
  line is the “update URL”; otherwise the update URL is
  ``http://www.worldwidetelescope.org/wwtweb/setup.aspx``.

These pieces of data are then acted upon in the following way by the Windows
client:

- If the message is non-empty, it is shown to the user in a dialog box.
- If the version of the running client is less than the minimum version, the
  user will be prompted to download an MSI installer from the update URL.
  The installer will be automatically run if consent is given and successfully
  downloaded. Either way, the Windows client will exit.
- If the warn version is newer than the running client and automatic updates
  are turned on, the user will also be prompted to download an MSI installer
  from the update URL. But if they do not update, the program continues
  running.
- If the user has explicitly asked to check for updates and the latest version
  is newer than the running client, the behavior is as above.
- When the Windows client first logs in, it records the data version with its
  local cache. If the server-provided data version changes, the client will
  consider its cache out-of-date and re-download all data. Note that this
  comparison is purely for textual equality, unlike the software version
  checks.

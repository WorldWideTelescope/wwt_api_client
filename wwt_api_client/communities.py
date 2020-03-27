# Copyright 2019-2020 the .NET Foundation
# Distributed under the terms of the revised (3-clause) BSD license.

"""Interacting with the WWT Communities APIs."""

import json
import os.path
import requests
import sys
from urllib.parse import parse_qs, urlparse

from . import APIRequest, Client

__all__ = '''
CommunitiesAPIRequest
CommunitiesClient
GetLatestCommunityRequest
IsUserRegisteredRequest
interactive_communities_login
'''.split()

LIVE_OAUTH_AUTH_SERVICE = "https://login.live.com/oauth20_authorize.srf"
LIVE_OAUTH_TOKEN_SERVICE = "https://login.live.com/oauth20_token.srf"
LIVE_OAUTH_DESKTOP_ENDPOINT = "https://login.live.com/oauth20_desktop.srf"
LIVE_AUTH_SCOPES = ['wl.emails', 'wl.signin']
WWT_CLIENT_ID = '000000004015657B'
OAUTH_STATE_BASENAME = 'communities-oauth.json'
CLIENT_SECRET_BASENAME = 'communities-client-secret.txt'

class CommunitiesClient(object):
    """A client for WWT Communities API requests.

    Instantiating such a client will make at least one web request, to refresh
    the Microsoft Live OAuth login token.

    In addition, an interactive user login may be necessary. This must be
    explicitly allowed by the caller to prevent random programs from hanging
    waiting for user input. If interactive login is successful, the
    authentication data from such a login are saved in the current user's
    state directory (~/.local/state/wwt_api_client/ on Linux machines) for
    subsequent use.

    """
    _parent = None
    _state_dir = None
    _state = None
    _access_token = None

    def __init__(self, parent_client, oauth_client_secret=None, interactive_login_if_needed=False, state_dir=None):
        self._parent = parent_client

        if state_dir is None:
            import appdirs
            state_dir = appdirs.user_state_dir('wwt_api_client', 'AAS_WWT')

        self._state_dir = state_dir

        # Do we have the client secret? This is saved to disk upon the first
        # login, but it can also be passed in.

        if oauth_client_secret is None:
            try:
                with open(os.path.join(self._state_dir, CLIENT_SECRET_BASENAME), 'rt') as f:
                    oauth_client_secret = f.readline().strip()
            except FileNotFoundError:
                pass

        if oauth_client_secret is None:
            raise Exception('cannot create CommunitiesClient: the \"oauth client secret\" '
                            'is not available to the program')

        # Try to get state from a previous OAuth flow and decide what to do
        # based on where we're at.

        try:
            with open(os.path.join(self._state_dir, OAUTH_STATE_BASENAME), 'rt') as f:
                self._state = json.load(f)
        except FileNotFoundError:
            pass

        # For the record, `http://worldwidetelescope.org/webclient` and
        # `http://www.worldwidetelesope.org/webclient` are valid
        # redirect_uri's.

        token_service_params = {
            'client_id': WWT_CLIENT_ID,
            'client_secret': oauth_client_secret,
            'redirect_uri': LIVE_OAUTH_DESKTOP_ENDPOINT,
        }

        if self._state is not None:
            # We have previous state -- we only need a refresh, which can
            # proceed non-interactively.

            token_service_params['grant_type'] = 'refresh_token'
            token_service_params['refresh_token'] = self._state['refresh_token']
        else:
            # We need to do the interactive authentication flow. This has to
            # be explicitly allowed by the caller because we don't want random
            # programs pausing for user input on the terminal.

            if not interactive_login_if_needed:
                raise Exception('cannot create CommunitiesClient: an interactive login is '
                                'required but unavailable right now')

            params = {
                'client_id': WWT_CLIENT_ID,
                'scope': ' '.join(LIVE_AUTH_SCOPES),
                'redirect_uri': LIVE_OAUTH_DESKTOP_ENDPOINT,
                'response_type': 'code'
            }

            preq = requests.Request(url=LIVE_OAUTH_AUTH_SERVICE, params=params).prepare()

            print()
            print('To use the WWT Communities APIs, interactive authentication to Microsoft')
            print('Live is required. Open this URL in a browser and log in:')
            print()
            print(preq.url)
            print()
            print('When done, copy the URL *that you are redirected to* and paste it here:')
            print('>> ', end='')
            redir_url = input()
            # should look like:
            # 'https://login.live.com/oauth20_desktop.srf?code=MHEXHEXHE-XHEX-HEXH-EXHE-XHEXHEXHEXHE&lc=NNNN'

            parsed = urlparse(redir_url)
            params = parse_qs(parsed.query)
            code = params.get('code')

            if not code:
                raise Exception('didn\'t get "code" parameter from response URL')

            token_service_params['grant_type'] = 'authorization_code'
            token_service_params['code'] = code

        # OK, proceed with the next stage.

        oauth_data = requests.post(
            LIVE_OAUTH_TOKEN_SERVICE,
            data = token_service_params,
        ).json()
        # structure is : {
        #   'token_type': 'bearer',
        #   'expires_in': <seconds>,
        #   'scope': <scopes>,
        #   'access_token': <long hex>,
        #   'refresh_token': <long hex>,
        #   'authentication_token': <long hex>,
        #   'user_id': <...>
        # }

        if 'error' in oauth_data:
            raise Exception(repr(oauth_data))

        # Looks like it worked! Save the results for next time.

        os.makedirs(self._state_dir, exist_ok=True)

        # Sigh, Python not making it easy to be secure ...
        fd = os.open(os.path.join(self._state_dir, OAUTH_STATE_BASENAME), os.O_WRONLY | os.O_CREAT, 0o600)
        f = open(fd, 'wt')
        with f:
            json.dump(oauth_data, f)

        fd = os.open(os.path.join(self._state_dir, CLIENT_SECRET_BASENAME), os.O_WRONLY | os.O_CREAT, 0o600)
        f = open(fd, 'wt')
        with f:
            print(oauth_client_secret, file=f)

        # And for this time:

        self._access_token = oauth_data['access_token']


    def get_latest_community(self):
        """Get information about the most recently created WWT Communities.

        .. testsetup:: [*]

            >>> comm_client = getfixture('communities_client_cached')

        Examples
        --------
        There are no arguments::

            >>> req = comm_client.get_latest_community()
            >>> req.send()

        Returns
        -------
        request : an initialized :class:`GetLatestCommunityRequest` object
            The request.

        """
        return GetLatestCommunityRequest(self)


    def is_user_registered(self):
        """Query whether the logged-in Microsoft Live user is registered with
        the WWT Communities system.

        .. testsetup:: [*]

            >>> comm_client = getfixture('communities_client_cached')

        Examples
        --------
        There are no arguments::

            >>> req = comm_client.is_user_registered()
            >>> print(req.send())
            True

        Returns
        -------
        request : an initialized :class:`IsUserRegisteredRequest` object
            The request.

        """
        return IsUserRegisteredRequest(self)


class CommunitiesAPIRequest(APIRequest):
    """A base class for WWT Communities API requests.

    These require that the user be logged in to a Microsoft Live account.

    """
    _comm_client = None

    def __init__(self, communities_client):
        super(CommunitiesAPIRequest, self).__init__(communities_client._parent)
        self._comm_client = communities_client


class GetLatestCommunityRequest(CommunitiesAPIRequest):
    """Get information about the most recently created WWT Communities. The
    information is returned as a ``wwt_data_formats.folder.Folder`` with
    sub-Folders corresponding to the communities.

    """
    def invalidity_reason(self):
        return None

    def make_request(self):
        return requests.Request(
            method = 'GET',
            url = self._client._api_base + '/Resource/Service/Browse/LatestCommunity',
            headers = {'LiveUserToken': self._comm_client._access_token},
        )

    def _process_response(self, resp):
        from wwt_data_formats.folder import Folder
        from xml.etree import ElementTree as etree
        xml = etree.fromstring(resp.text)
        return Folder.from_xml(xml)


class IsUserRegisteredRequest(CommunitiesAPIRequest):
    """Asks whether the logged-in Microsoft Live user is registered with the WWT
    Communities system.

    """
    def invalidity_reason(self):
        return None

    def make_request(self):
        return requests.Request(
            method = 'GET',
            url = self._client._api_base + '/Resource/Service/User',
            headers = {'LiveUserToken': self._comm_client._access_token},
        )

    def _process_response(self, resp):
        t = resp.text

        if t == 'True':
            return True
        elif t == 'False':
            return False
        raise Exception(f'unexpected response from IsUserRegistered API: {t!r}')


# Command-line utility for initializing the OAuth state.

def interactive_communities_login(args):
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--secret-file',
        metavar = 'PATH',
        help = 'Path to a file from which to read the WWT client secret',
    )
    parser.add_argument(
        '--secret-env',
        metavar = 'ENV-VAR-NAME',
        help = 'Name of an environment variable containing the WWT client secret',
    )

    settings = parser.parse_args(args)

    # Make sure we actually have a secret to work with.

    if settings.secret_file is not None:
        with open(settings.secret_file) as f:
            client_secret = f.readline().strip()
    elif settings.secret_env is not None:
        client_secret = os.environ.get(settings.secret_env)
    else:
        print('error: the WWT \"client secret\" must be provided; '
              'use --secret-file or --secret-env', file=sys.stderr)
        sys.exit(1)

    if not client_secret:
        print('error: the WWT \"client secret\" is empty or unset', file=sys.stderr)
        sys.exit(1)

    # Ready to go ...

    CommunitiesClient(
        Client(),
        oauth_client_secret = client_secret,
        interactive_login_if_needed = True,
    )

    print('OAuth flow successfully completed.')


if __name__ == '__main__':
    interactive_communities_login(sys.argv[1:])

# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
# Distributed under the terms of the revised (3-clause) BSD license.

import json
from mock import Mock
import os.path
import pytest
import shutil
import tempfile

from .. import communities
from ..communities import CommunitiesClient

from .test_core import client


def fake_request_post(url, data=None, json=None, **kwargs):
    rv = Mock()

    if url == communities.LIVE_OAUTH_TOKEN_SERVICE:
        rv.json.return_value = {
            'access_token': 'fake_access_token',
            'refresh_token': 'fake_refresh_token',
        }
    else:
        raise Exception(f'unexpected URL to fake requests.post(): {url}')

    return rv

def fake_request_session_send(request, **kwargs):
    rv = Mock()

    if request.url == 'http://www.worldwidetelescope.org/Resource/Service/User':
        rv.text = 'True'
    else:
        raise Exception(f'unexpected URL to fake requests.Session.send(): {url}')

    return rv


@pytest.fixture
def fake_requests(mocker):
    m = mocker.patch('requests.post')
    m.side_effect = fake_request_post

    m = mocker.patch('requests.Session.send')
    m.side_effect = fake_request_session_send


@pytest.fixture
def communities_client_cached(client, fake_requests):
    temp_state_dir = tempfile.mkdtemp()

    with open(os.path.join(temp_state_dir, communities.CLIENT_SECRET_BASENAME), 'w') as f:
        print('fake_client_secret', file=f)

    with open(os.path.join(temp_state_dir, communities.OAUTH_STATE_BASENAME), 'w') as f:
        oauth_data = {
            'access_token': 'fake_access_token',
            'refresh_token': 'fake_refresh_token',
        }
        json.dump(oauth_data, f)

    yield CommunitiesClient(
        client,
        state_dir = temp_state_dir,
    )

    shutil.rmtree(temp_state_dir)


def test_create_client_cached(communities_client_cached):
    pass


@pytest.fixture
def communities_client_interactive(client, fake_requests, mocker):
    temp_state_dir = tempfile.mkdtemp()

    m = mocker.patch('builtins.input')
    m.return_value = 'http://fakelogin.example.com?code=fake_code'

    yield CommunitiesClient(
        client,
        oauth_client_secret = 'fake_client_secret',
        interactive_login_if_needed=True,
        state_dir = temp_state_dir,
    )

    shutil.rmtree(temp_state_dir)


def test_create_client_interactive(communities_client_interactive):
    pass


def test_cli(communities_client_interactive, mocker):
    m = mocker.patch('wwt_api_client.communities.CommunitiesClient')
    m.return_value = communities_client_interactive

    with pytest.raises(SystemExit):
        communities.interactive_communities_login([])

    os.environ['FAKE_CLIENT_SECRET'] = 'fakey'
    communities.interactive_communities_login(['--secret-env=FAKE_CLIENT_SECRET'])

    f = tempfile.NamedTemporaryFile(mode='wt', delete=False)
    print('fake_client_secret', file=f)
    f.close()
    communities.interactive_communities_login([f'--secret-file={f.name}'])
    os.unlink(f.name)


def test_is_user_registered(communities_client_cached):
    assert communities_client_cached.is_user_registered().send() == 'True'

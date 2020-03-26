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


@pytest.fixture
def fake_requests(mocker):
    m = mocker.patch('requests.post')
    m.side_effect = fake_request_post


@pytest.fixture
def communities_client_cached(client, fake_requests):
    temp_state_dir = tempfile.mkdtemp()

    with open(os.path.join(temp_state_dir, communities.CLIENT_SECRET_BASENAME), 'w') as f:
        print('secret', file=f)

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

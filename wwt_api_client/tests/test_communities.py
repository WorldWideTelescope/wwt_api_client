# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
# Distributed under the terms of the revised (3-clause) BSD license.

import json
from mock import Mock
import os.path
import pytest
import shutil
import tempfile
from xml.etree import ElementTree as etree

from .. import communities
from ..communities import CommunitiesClient

from .test_core import assert_xml_trees_equal, client


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

GET_LATEST_COMMUNITY_XML_TEXT = '''\
<?xml version='1.0' encoding='UTF-8'?>
<Folder Browseable="True" Group="Explorer" Searchable="True"
        Thumbnail="http://www.worldwidetelescope.org/Content/Images/defaultfolderwwtthumbnail.png"
        Type="Earth">
  <Folder Browseable="True" Group="Explorer" Name="AAS Nova" Searchable="True"
          Thumbnail="http://www.worldwidetelescope.org/File/Thumbnail/80a8d8ef-8a76-414a-a398-349337baac8c"
          Url="http://www.worldwidetelescope.org/Resource/Service/Folder/607649"
          Type="Earth" />
</Folder>
'''

def fake_request_session_send(request, **kwargs):
    rv = Mock()

    if request.url == 'http://www.worldwidetelescope.org/Resource/Service/User':
        rv.text = 'True'
    elif request.url == 'http://www.worldwidetelescope.org/Resource/Service/Browse/LatestCommunity':
        rv.text = GET_LATEST_COMMUNITY_XML_TEXT
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


def test_get_latest_community(communities_client_cached):
    expected_xml = etree.fromstring(GET_LATEST_COMMUNITY_XML_TEXT)

    folder = communities_client_cached.get_latest_community()
    observed_xml = folder.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)


def test_is_user_registered(communities_client_cached):
    assert communities_client_cached.is_user_registered().send(raw_response=True).text == 'True'
    assert communities_client_cached.is_user_registered().send() == True

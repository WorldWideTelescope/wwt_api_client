# -*- mode: python; coding: utf-8 -*-
# Copyright 2020-2023 the .NET Foundation
# Distributed under the MIT license

import json
from mock import Mock
import os.path
import pytest
import shutil
import tempfile
from xml.etree import ElementTree as etree

from .. import communities, enums, DEFAULT_API_BASE
from ..communities import CommunitiesClient

from .test_core import assert_xml_trees_equal, client


def fake_request_post(url, data=None, json=None, **kwargs):
    rv = Mock()

    if url == communities.LIVE_OAUTH_TOKEN_SERVICE:
        rv.json.return_value = {
            "access_token": "fake_access_token",
            "refresh_token": "fake_refresh_token",
        }
    else:
        raise Exception(f"unexpected URL to fake requests.post(): {url}")

    return rv


GET_COMMUNITY_INFO_JSON_TEXT = """
{
  "community": {
    "MemberCount": 0,
    "ViewCount": 6,
    "ShareUrl": null,
    "Description": "Testing community",
    "LastUpdated": "44 minutes ago",
    "ActionUrl": null,
    "IsOffensive": false,
    "Id": 800000,
    "Name": "Fake Test",
    "Category": 20,
    "ParentId": 654321,
    "ParentName": "None",
    "ParentType": 3,
    "Tags": "testtag",
    "Rating": 0,
    "RatedPeople": 0,
    "ThumbnailID": "00000000-0000-0000-0000-000000000000",
    "Entity": 1,
    "FileName": null,
    "ContentAzureID": null,
    "UserPermission": 63,
    "AccessType": 2,
    "Producer": "Firstname Lastname",
    "ProducerId": 123456,
    "ContentType": 0,
    "DistributedBy": null
  },
  "permission": {
    "Result": {
      "CurrentUserPermission": 63,
      "PermissionItemList": [
        {
          "Comment": null,
          "Date": "/Date(1585273889157)/",
          "Requested": "44 minutes ago",
          "CommunityId": 800000,
          "CommunityName": "Fake Test",
          "CurrentUserRole": 5,
          "IsInherited": true,
          "CanShowEditLink": false,
          "CanShowDeleteLink": false,
          "Id": 123456,
          "Name": "Firstname Lastname",
          "Role": 5
        }
      ],
      "PaginationDetails": {
        "ItemsPerPage": 8,
        "CurrentPage": 0,
        "TotalPages": 1,
        "TotalCount": 1
      },
      "SelectedPermissionsTab": 1
    },
    "Id": 4,
    "Exception": null,
    "Status": 5,
    "IsCanceled": false,
    "IsCompleted": true,
    "CreationOptions": 0,
    "AsyncState": null,
    "IsFaulted": false
  }
}
"""

GET_LATEST_COMMUNITY_XML_TEXT = """\
<?xml version='1.0' encoding='UTF-8'?>
<Folder Browseable="True" Group="Explorer" 
        Searchable="True"
        Thumbnail="http://www.worldwidetelescope.org/Content/Images/defaultfolderwwtthumbnail.png"
        Type="Earth">
  <Folder Browseable="True" Group="Explorer" Name="AAS Nova" 
          Searchable="True"
          Thumbnail="http://www.worldwidetelescope.org/File/Thumbnail/80a8d8ef-8a76-414a-a398-349337baac8c"
          Url="http://www.worldwidetelescope.org/Resource/Service/Folder/607649"
          Type="Earth" />
</Folder>
"""

GET_MY_PROFILE_JSON_TEXT = """
{
  "ProfileId": 123456,
  "ProfileName": "Firstname Lastname",
  "AboutProfile": "",
  "Affiliation": "Affil Text",
  "ProfilePhotoLink": "~/Content/Images/profile.png",
  "TotalStorage": "5.00 GB",
  "UsedStorage": "0.00 B",
  "AvailableStorage": "5.00 GB",
  "PercentageUsedStorage": "0%",
  "IsCurrentUser": true,
  "IsSubscribed": false
}
"""

GET_PROFILE_ENTITIES_JSON_TEXT = """
{
  "entities": [
    {
      "DownloadCount": 0,
      "Citation": "Hello World Citation",
      "Narrator": null,
      "AssociatedFiles": null,
      "ShareUrl": null,
      "ContentUrl": null,
      "IsLink": false,
      "Size": 0,
      "VideoID": "00000000-0000-0000-0000-000000000000",
      "VideoName": null,
      "Description": "A text file that says Hello, world!",
      "LastUpdated": "4 minutes ago",
      "ActionUrl": null,
      "IsOffensive": false,
      "Id": 82077,
      "Name": "helloworld.txt",
      "Category": 20,
      "ParentId": 610131,
      "ParentName": "None",
      "ParentType": 3,
      "Tags": "",
      "Rating": 0,
      "RatedPeople": 0,
      "ThumbnailID": "00000000-0000-0000-0000-000000000000",
      "Entity": 3,
      "FileName": "helloworld.txt",
      "ContentAzureID": "0672899a-37d0-4277-8436-e1eb73916399",
      "UserPermission": 3,
      "AccessType": 0,
      "Producer": "Peter Williams ",
      "ProducerId": 609582,
      "ContentType": 7,
      "DistributedBy": "Hello World Author"
    }
  ],
  "pageInfo": {
    "ItemsPerPage": 99999,
    "CurrentPage": 1,
    "TotalPages": 1,
    "TotalCount": 1
  }
}
"""


def fake_request_session_send(request, **kwargs):
    rv = Mock()

    if request.url == DEFAULT_API_BASE + "/Community/Create/New":
        rv.text = '{"ID": 800000}'
    elif request.url == DEFAULT_API_BASE + "/Community/Delete/800000/0":
        rv.text = "True"
    elif request.url == DEFAULT_API_BASE + "/Community/Detail/800000":
        rv.text = GET_COMMUNITY_INFO_JSON_TEXT
    elif request.url == DEFAULT_API_BASE + "/Profile/Entities/Content/1/99999":
        rv.text = GET_PROFILE_ENTITIES_JSON_TEXT
    elif request.url == DEFAULT_API_BASE + "/Profile/MyProfile/Get":
        rv.text = GET_MY_PROFILE_JSON_TEXT
    elif request.url == DEFAULT_API_BASE + "/Resource/Service/Browse/LatestCommunity":
        rv.text = GET_LATEST_COMMUNITY_XML_TEXT
    elif request.url == DEFAULT_API_BASE + "/Resource/Service/User":
        rv.text = "True"
    else:
        raise Exception(
            f"unexpected URL to fake requests.Session.send(): {request.url}"
        )

    return rv


@pytest.fixture
def fake_requests(mocker):
    m = mocker.patch("requests.post")
    m.side_effect = fake_request_post

    m = mocker.patch("requests.Session.send")
    m.side_effect = fake_request_session_send


@pytest.fixture
def communities_client_cached(client, fake_requests):
    temp_state_dir = tempfile.mkdtemp()

    with open(
        os.path.join(temp_state_dir, communities.CLIENT_SECRET_BASENAME), "w"
    ) as f:
        print("fake_client_secret", file=f)

    with open(os.path.join(temp_state_dir, communities.OAUTH_STATE_BASENAME), "w") as f:
        oauth_data = {
            "access_token": "fake_access_token",
            "refresh_token": "fake_refresh_token",
        }
        json.dump(oauth_data, f)

    yield CommunitiesClient(
        client,
        state_dir=temp_state_dir,
    )

    shutil.rmtree(temp_state_dir)


def test_create_client_cached(communities_client_cached):
    pass


@pytest.fixture
def communities_client_interactive(client, fake_requests, mocker):
    temp_state_dir = tempfile.mkdtemp()

    m = mocker.patch("builtins.input")
    m.return_value = "http://fakelogin.example.com?code=fake_code"

    yield CommunitiesClient(
        client,
        oauth_client_secret="fake_client_secret",
        interactive_login_if_needed=True,
        state_dir=temp_state_dir,
    )

    shutil.rmtree(temp_state_dir)


def test_create_client_interactive(communities_client_interactive):
    pass


def test_cli(communities_client_interactive, mocker):
    m = mocker.patch("wwt_api_client.communities.CommunitiesClient")
    m.return_value = communities_client_interactive

    with pytest.raises(SystemExit):
        communities.interactive_communities_login([])

    os.environ["FAKE_CLIENT_SECRET"] = "fakey"
    communities.interactive_communities_login(["--secret-env=FAKE_CLIENT_SECRET"])

    f = tempfile.NamedTemporaryFile(mode="wt", delete=False)
    print("fake_client_secret", file=f)
    f.close()
    communities.interactive_communities_login([f"--secret-file={f.name}"])
    os.unlink(f.name)


def test_create_community(communities_client_cached):
    payload = {
        "communityJson": {
            "CategoryID": 20,
            "ParentID": "610131",
            "AccessTypeID": 2,
            "IsOffensive": False,
            "IsLink": False,
            "CommunityType": "Community",
            "Name": "API Test Community",
            "Description": "Community description",
            "Tags": "tag1,tag2",
        }
    }
    new_id = communities_client_cached.create_community(payload=payload).send()
    assert new_id == 800000


def test_delete_community(communities_client_cached):
    assert communities_client_cached.delete_community(id=800000).send()


def test_get_community_info(communities_client_cached):
    expected_json = json.loads(GET_COMMUNITY_INFO_JSON_TEXT)
    observed_json = communities_client_cached.get_community_info(id=800000).send()
    assert observed_json == expected_json


def test_get_latest_community(communities_client_cached):
    expected_xml = etree.fromstring(GET_LATEST_COMMUNITY_XML_TEXT)

    folder = communities_client_cached.get_latest_community().send()
    observed_xml = folder.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)


def test_get_my_profile(communities_client_cached):
    expected_json = json.loads(GET_MY_PROFILE_JSON_TEXT)
    observed_json = communities_client_cached.get_my_profile().send()
    assert observed_json == expected_json


def test_get_profile_entities(communities_client_cached):
    expected_json = json.loads(GET_PROFILE_ENTITIES_JSON_TEXT)
    observed_json = communities_client_cached.get_profile_entities(
        entity_type=enums.EntityType.CONTENT,
        current_page=1,
        page_size=99999,
    ).send()
    assert observed_json == expected_json


def test_is_user_registered(communities_client_cached):
    assert (
        communities_client_cached.is_user_registered().send(raw_response=True).text
        == "True"
    )
    assert communities_client_cached.is_user_registered().send()

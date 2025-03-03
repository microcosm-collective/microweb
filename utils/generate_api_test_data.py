#!/usr/bin/python

import datetime
import json
import sys
import requests
import urllib.parse
import urllib.request, urllib.parse, urllib.error

"""
Utilities for fetching JSON from the microcosm API and writing it to files
for unit testing.
"""


def main():
    if len(sys.argv) != 3:
        print("Usage: python %s <api_subdomain> <access_token>" % sys.argv[0])
        sys.exit(2)

    site_subdomain = sys.argv[1]
    access_token = sys.argv[2]
    failures = {}

    # site
    ident = "Fetching site"
    print(ident)
    url = unparse_api_url(site_subdomain, "api/v1/site", access_token=access_token)
    response = requests.get(url, headers={"Accept-Encoding": "application/json"})
    if response.status_code != 200:
        failures[ident] = response.content
        exit_with_error(failures)
    else:
        site = open("site.json", "w")
        site.write(response.content)
        site.close()

    # whoami
    ident = "Fetching whoami"
    print(ident)
    url = unparse_api_url(site_subdomain, "api/v1/whoami", access_token=access_token)
    response = requests.get(url, headers={"Accept-Encoding": "application/json"})
    if response.status_code != 200:
        failures[ident] = response.content
        exit_with_error(failures)
    else:
        whoami = open("whoami.json", "w")
        whoami.write(response.content)
        whoami.close()
        profile_id = response.json()["data"]["id"]

    # profile
    ident = "Fetching profile ID %s" % profile_id
    print(ident)
    url = unparse_api_url(
        site_subdomain, "api/v1/profiles/%s" % profile_id, access_token=access_token
    )
    response = requests.get(url, headers={"Accept-Encoding": "application/json"})
    if response.status_code != 200:
        failures[ident] = response.content
        exit_with_error(failures)
    else:
        whoami = open("profile.json", "w")
        whoami.write(response.content)
        whoami.close()

    # microcosms
    ident = "Creating microcosm"
    print(ident)
    url = unparse_api_url(
        site_subdomain, "api/v1/microcosms", access_token=access_token
    )
    data = json.dumps(
        {
            "title": "Generated",
            "description": "Generated microcosm",
        }
    )
    response = requests.post(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    if response.status_code != 200:
        failures[ident] = response.content
        exit_with_error(failures)
    else:
        microcosm = open("microcosm.json", "w")
        microcosm.write(response.content)
        microcosm.close()
        microcosm_id = response.json()["data"]["id"]
        print("Created microcosm with ID: %d" % microcosm_id)

    # conversations
    ident = "Creating conversation without comment"
    print(ident)
    url = unparse_api_url(
        site_subdomain, "api/v1/conversations", access_token=access_token
    )
    data = json.dumps(
        {
            "microcosmId": microcosm_id,
            "title": "Generated",
            "description": "Generated conversation",
        }
    )
    response = requests.post(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    if response.status_code != 200:
        failures[ident] = response.content
        exit_with_error(failures)
    else:
        conversation = open("conversation_without_comment.json", "w")
        conversation.write(response.content)
        conversation.close()

    ident = "Creating conversation with comment"
    print(ident)
    url = unparse_api_url(
        site_subdomain, "api/v1/conversations", access_token=access_token
    )
    data = json.dumps(
        {
            "microcosmId": microcosm_id,
            "title": "Generated",
            "description": "Generated conversation",
            "firstComment": "This is the first comment",
        }
    )
    response = requests.post(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    if response.status_code != 200:
        failures[ident] = response.content
        exit_with_error(failures)
    else:
        conversation = open("conversation_with_comment.json", "w")
        conversation.write(response.content)
        conversation.close()
        conversation_id = int(response.json()["data"]["id"])
        print("Created conversation with ID: %d" % conversation_id)

    # generate comments on the conversation so pagination can be tested
    ident = "Creating 30 comments on conversation with ID: %d" % conversation_id
    print(ident)
    url = unparse_api_url(site_subdomain, "api/v1/comments", access_token=access_token)
    for comment_num in range(30):
        data = json.dumps(
            {
                "itemType": "conversation",
                "itemId": conversation_id,
                "markdown": "Here is comment number %d" % comment_num,
            }
        )
        response = requests.post(
            url, data=data, headers={"Content-Type": "application/json"}
        )
        if response.status_code != 200:
            failures[ident] = response.content
            exit_with_error(failures)
        else:
            print("Comment %d done" % comment_num)

    # save conversation as conversation_with_comment_pages
    ident = "Fetching conversation %d" % conversation_id
    print(ident)
    url = unparse_api_url(site_subdomain, "/api/v1/conversations/%d" % conversation_id)
    response = requests.get(url, headers={"Accept-Encoding": "application/json"})
    if response.status_code != 200:
        failures[ident] = response.content
        exit_with_error()
    else:
        paginated_comments = open("conversation_with_paginated_comments.json", "w")
        paginated_comments.write(response.content)
        paginated_comments.close()

    # events
    ident = "Creating event without comment"
    print(ident)
    url = unparse_api_url(site_subdomain, "api/v1/events", access_token=access_token)
    when = (datetime.datetime.utcnow() + datetime.timedelta(weeks=2)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    data = json.dumps(
        {
            "microcosmId": microcosm_id,
            "title": "Generated Event",
            "when": when,
            "duration": 180,
            "where": "The Park",
            "rsvpLimit": 100,
        }
    )
    response = requests.post(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    if response.status_code != 200:
        failures[ident] = response.content
        exit_with_error(failures)
    else:
        event = open("event_without_comment.json", "w")
        event.write(response.content)
        event.close()

    ident = "Creating event with comment"
    print(ident)
    url = unparse_api_url(site_subdomain, "api/v1/events", access_token=access_token)
    when = (datetime.datetime.utcnow() + datetime.timedelta(weeks=2)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    data = json.dumps(
        {
            "microcosmId": microcosm_id,
            "title": "Generated Event",
            "when": when,
            "duration": 180,
            "where": "The Park",
            "rsvpLimit": 100,
            "firstComment": "First generated comment",
        }
    )
    response = requests.post(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    if response.status_code != 200:
        failures[ident] = response.content
        exit_with_error(failures)
    else:
        event = open("event_with_comment.json", "w")
        event.write(response.content)
        event.close()
        event_id = response.json()["data"]["id"]


def unparse_api_url(site_subdomain, path, query_params={}, access_token=""):
    netloc = "%s.microco.sm" % site_subdomain
    if access_token:
        query_params["access_token"] = access_token
    querystring = urllib.parse.urlencode(query_params)
    return urllib.parse.urlunparse(("https", netloc, path, "", querystring, ""))


def exit_with_error(failures):
    print("Failed. Errors follow...")
    print(failures)
    sys.exit(1)


if __name__ == "__main__":
    main()

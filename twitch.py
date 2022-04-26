#  Copyright (c)  2022. Andrea Antonio Perrelli.
#   All rights reserved.

import urllib
import urllib.parse
import urllib.request
import requests
import os

from urllib.error import HTTPError, URLError

import json

import utility
import config
import debug


def get_channel_id(channel_name):
    # https: // api.twitch.tv / helix / channels
    get_channel_id_url = "https://api.twitch.tv/helix/users?login=" + channel_name
    get_channel_id_headers = {'Authorization': 'Bearer ' + os.environ['CLIENT_ACCESS_TOKEN'],
                              'Client-ID': os.environ['CLIENT_ID']}
    utility.print_toscreen(get_channel_id_url)
    response = requests.get(get_channel_id_url, headers=get_channel_id_headers)

    channel_id = 0

    data = response.json()
    utility.print_toscreen(data["data"][0]["id"])
#    utility.print_toscreen(data["access_token"][0])

    result = "0"

    try:
        result = data["data"][0]["id"]

    except IndexError as err:
        debug.output_error(debug.lineno() + " - " + " Bad channel name: " + str(err))
        return result

    return result


async def is_there_clip(clip_id):
    url = "https://api.twitch.tv/helix/clips?id=" + clip_id
    req = urllib.request.Request(url,
                                 headers={
                                     "Client-ID": os.environ['CLIENT_ID'],
                                     "Authorization": "Bearer " + os.environ['CLIENT_ACCESS_TOKEN'],
                                 },
                                 data=None)

    try:
        response = urllib.request.urlopen(req)
    except (HTTPError, URLError) as err:
        debug.output_error(debug.lineno() + " - " + "HTTP Error: " + str(err))
        utility.restart()

    data = json.load(response)
#    utility.print_toscreen(data)

    try:
        result = data["data"][0]["id"]

    except IndexError as err:
        debug.output_error(debug.lineno() + " - " + "Index Error: " + str(err))
        return False

    utility.print_toscreen("true")
    return True


async def create_clip(channel_id):
    url = "https://api.twitch.tv/helix/clips"
    data = urllib.parse.urlencode({
        'has_delay': 'false',
        'broadcaster_id': channel_id,
    })
    data = data.encode('utf-8')

    req = urllib.request.Request(url,
                                 headers={
                                     "Client-ID": os.environ['CLIENT_ID'],
                                     "Authorization": "Bearer " + os.environ['CLIENT_ACCESS_TOKEN'],
                                 }, data=data)

    try:
        response = urllib.request.urlopen(req, data)

    except (HTTPError, URLError) as err:
        debug.output_error("HTTP Error: " + str(err) + debug.lineno())
        return 0

    data = json.load(response)
    utility.print_toscreen(str(data))

    return data["data"][0]


def is_stream_live(channel_id):
    url = "https://api.twitch.tv/helix/streams?user_id=" + channel_id

    utility.print_toscreen(url)

    req = urllib.request.Request(url,
                                 headers={
                                     "Client-ID": os.environ['CLIENT_ID'],
                                     "Authorization": "Bearer " + os.environ['CLIENT_ACCESS_TOKEN'],
                                 },
                                 data=None)

    response = urllib.request.urlopen(req)
    data = json.load(response)
    #    utility.print_toscreen(data)

    try:
        result = data["data"][0]["type"]
        utility.print_toscreen(result)

    except IndexError as err:
        debug.output_error(debug.lineno() + " - " + "Index Error" + str(err))
        utility.print_toscreen("false")
        return False

    utility.print_toscreen("true")
    return True


def test():
    channel_id = get_channel_id("summit1g")
    utility.print_toscreen(channel_id)

    create_clip(channel_id)


utility.print_toscreen("Starting Twitch API")

if __name__ == "__main__":
    utility.print_toscreen("Hello")
    test()

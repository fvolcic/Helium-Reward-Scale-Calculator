"""Utilities for downloading data from the helium api."""

import json
import requests
import datetime

def get_nodes_box(swlat, swlon, nelat, nelon):
    """Downloads the nodes in a given box."""
    endpoint = "https://api.helium.io/v1/hotspots/location/box"
    query = "?swlat={swlat}&swlon={swlon}&nelat={nelat}&nelon={nelon}"
    query = query.format(swlat=swlat, swlon=swlon, nelat=nelat, nelon=nelon)

    print(endpoint+query)

    r = requests.get(endpoint+query)

    return json.loads(r.text)['data']

def compute_miner_earnings(miner_addr):
    """Return the earnings of a given miner in the past 30 days."""
    time_max = datetime.datetime.now()
    time_min = time_max - datetime.timedelta(30)
    endpoint = "https://api.helium.io/v1/hotspots/{}/rewards/sum".format(miner_addr)
    query = "?min_time={t1}&max_time={t2}".format(
        t1 = time_min.isoformat(),
        t2 = time_max.isoformat()
    )
    r = requests.get(endpoint+query)
    miner_data = json.loads(r.text)['data']
    return miner_data

def get_last_poc_challenge(addr):
    endpoint = f"https://api.helium.io/v1/hotspots/{addr}"
    r = requests.get(endpoint)
    data = json.loads(r.text)
    if data['data']['last_poc_challenge'] is None:
        return 0
    return int(data['data']['last_poc_challenge'])

def get_height():
    endpoint = "https://api.helium.io/v1/blocks/height"
    return int(json.loads(requests.get(endpoint).text)['data']['height'])
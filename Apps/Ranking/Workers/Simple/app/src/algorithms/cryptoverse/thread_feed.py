"""
Cryptoverse thread feed with likes
==================================

Version: 0.1.0

Example:

`ranking/cryptoverse_thread_feed;id=claim:0x5bad1020a...6a9b13301b <https://api.userfeeds.io/ranking/cryptoverse_thread_feed;id=claim:0x5bad1020a14a58f358363c35eb4fa3d3eb3b1c58c160196e810e77771205444e7b7336e9c42b99960f189e8e828c9643f6fcf4e42233a0473a5570ee6a9b13301b>`_

"""

from algorithms.utils import claimPattern, tokenPattern, assetPattern, addressPattern
from algorithms.cryptoverse import thread
from algorithms.kuba import reactions
from algorithms.utils import param


@param("id", required=True)
def run(conn_mgr, input, **params):
    result = thread.run(conn_mgr, input, **params)
    result = reactions.run(conn_mgr, result)
    set_types(result["items"])
    return result


def set_types(items):
    for i in items:
        if not isinstance(i["target"], str):
            i["type"] = "like"
            set_type(i["target"])
        else:
            set_type(i)


def set_type(i):
    if tokenPattern.match(i["target"]) or addressPattern.match(i["target"]):
        i["type"] = "boost"
    elif i["about"]:
        if claimPattern.match(i["about"]):
            i["type"] = "regular"
        elif tokenPattern.match(i["about"]):
            i["type"] = "post_to"
        elif addressPattern.match(i["about"]):
            i["type"] = "post_to_simple"
        elif assetPattern.match(i["about"]):
            i["type"] = "post_club"
        else:
            i["type"] = "post_about"
    else:
        i["type"] = "regular"

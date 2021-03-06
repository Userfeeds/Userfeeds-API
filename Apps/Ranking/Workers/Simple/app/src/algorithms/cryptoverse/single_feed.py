"""
Cryptoverse single feed with replies and likes
==============================================

Version: 0.1.0

Example:

`ranking/cryptoverse_single_feed;id=ethereum:0x06012...a266d:341605 <https://api.userfeeds.io/ranking/cryptoverse_single_feed;id=ethereum:0x06012c8cf97bead5deae237070f9587f8e7a266d:341605>`_

"""

from algorithms.utils import tokenPattern, assetPattern, addressPattern
from algorithms.cryptoverse import single
from algorithms.cryptoverse import single_address
from algorithms.kuba import replies, reactions
from algorithms.utils import param


@param("id", required=True)
def run(conn_mgr, input, **params):
    if addressPattern.match(params["id"]):
        result = single_address.run(conn_mgr, input, **params)
    else:
        result = single.run(conn_mgr, input, **params)
    result = replies.run(conn_mgr, result)
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
    if i.get("reply_to"):
        i["type"] = "response"
    elif tokenPattern.match(i["target"]) or addressPattern.match(i["target"]):
        i["type"] = "boost"
    elif i.get("label") in ["github", "twitter", "instagram", "facebook", "discord", "telegram"]:
        i["type"] = "social"
    elif i["about"]:
        if tokenPattern.match(i["about"]):
            i["type"] = "post_to"
        elif addressPattern.match(i["about"]):
            i["type"] = "post_to_simple"
        elif assetPattern.match(i["about"]):
            i["type"] = "post_club"
        else:
            i["type"] = "post_about"
    else:
        i["type"] = "regular"

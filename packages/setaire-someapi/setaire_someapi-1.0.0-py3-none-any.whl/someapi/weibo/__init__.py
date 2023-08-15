'''
 # @ Author: tuweifeng
 # @ Create Time: 2023-02-28 21:42:28
 # @ Modified by: tuweifeng
 # @ Modified time: 2023-02-28 21:42:41
 # @ Description:
    
 '''


import json
from requests import Session, Response
from requests.cookies import RequestsCookieJar


TV_API_COMPONENT_URL = "https://weibo.com/tv/api/component"
AJAX_GETVERSION_VERSION_URL = "https://weibo.com/ajax/getversion"


def get_playinfo(session: Session, cookies: RequestsCookieJar, oid: str) -> Response:
    x_xsrf_token = cookies.get("XSRF-TOKEN")
    return session.post(
        TV_API_COMPONENT_URL,
        params={
            "page": f"/tv/show/{oid}"
        },
        data={
            "data": json.dumps({"Component_Play_Playinfo": {"oid": oid}})
        },
        cookies=cookies,
        headers={
            "x-xsrf-token": x_xsrf_token,
            "page-referer": f"/show/{oid}",
            "referer": f"https://h5.video.weibo.com/show/{oid}"
        },
    )


def get_subchannelinfo(session: Session, cookies: RequestsCookieJar, channel_id: int, subchannel_id: int, next_cursor: str = "") -> Response:
    x_xsrf_token = cookies.get("XSRF-TOKEN")
    return session.post(
        TV_API_COMPONENT_URL,
        params={
            "page": f"/tv/channel/{channel_id}/{subchannel_id}"
        },
        data={
            "data": json.dumps({
                "Component_Channel_Subchannel": {
                    "next_cursor": next_cursor,
                    "cid": channel_id
                } if next_cursor else {
                    "cid": subchannel_id
                }})
        },
        cookies=cookies,
        headers={
            "x-xsrf-token": x_xsrf_token,
            "page-referer": f"/tv/channel/{channel_id}",
            "referer": f"https://weibo.com/tv/channel/{channel_id}/{subchannel_id}"
        },
    )


def get_channelinfo(session: Session, cookies: RequestsCookieJar, channel_id: int) -> Response:
    x_xsrf_token = cookies.get("XSRF-TOKEN")
    return session.post(
        TV_API_COMPONENT_URL,
        params={
            "page": f"/tv/channel/{channel_id}"
        },
        data={
            "data": json.dumps({
                "Component_Channel_Info": {
                    "cid": channel_id
                }})
        },
        cookies=cookies,
        headers={
            "x-xsrf-token": x_xsrf_token,
            "page-referer": f"/tv/channel/{channel_id}",
            "referer": f"https://weibo.com/tv/channel/{channel_id}"
        },
    )


def update_token_cookies(session: Session, cookies: RequestsCookieJar):
    token_cookies = session.get(AJAX_GETVERSION_VERSION_URL).cookies.get_dict()
    cookies.update(token_cookies)

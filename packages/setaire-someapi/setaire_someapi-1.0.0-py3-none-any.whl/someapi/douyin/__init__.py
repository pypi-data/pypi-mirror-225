'''
 # @ Author: tuweifeng
 # @ Create Time: 2023-03-05 15:50:05
 # @ Modified by: tuweifeng
 # @ Modified time: 2023-03-18 14:08:20
 # @ Description:
    获取抖音用户数据、xbogus加密
 '''


import re
import os
from types import MappingProxyType
from urllib import parse
import execjs
from requests import Session, Response
from requests.cookies import RequestsCookieJar
from requests.models import RequestEncodingMixin

AWEME_V1_WEB_AWEME_POST_URL = "https://www.douyin.com/aweme/v1/web/aweme/post/"
AWEME_V1_WEB_USER_PROFILE_OTHER_URL = "https://www.douyin.com/aweme/v1/web/user/profile/other/"
VIDEO_URL = "https://www.douyin.com/video/"


HEADERS = MappingProxyType({
    "origin": "https://www.douyin.com",
    "referer": "https://www.douyin.com/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
})


class InvalidCookiesError(Exception):
    pass


def get_xbogus(params: dict):
    js = os.path.join(os.path.dirname(__file__), "xbogus.js")
    with open(js, "r") as f:
        content = f.read()

    client = execjs.compile(content)
    xbogus = client.call(
        "sign", RequestEncodingMixin._encode_params(params), HEADERS["user-agent"])
    return xbogus


def get_user_videos(session: Session, cookies: RequestsCookieJar, sec_user_id: str, size: int = 10) -> Response:
    params = {
        "device_platform": "webapp",
        "aid": 6383,
        "channel": "channel_pc_web",
        "sec_user_id": sec_user_id,
        # "max_cursor": 1674630472000,
        "locate_query": False,
        "show_live_replay_strategy": 1,
        "count": size,
        "publish_video_strategy_type": 2,
        "pc_client_type": 1,
        "version_code": 170400,
        "version_name": "17.4.0",
        "cookie_enabled": True,
        "screen_width": 1440,
        "screen_height": 900,
        "browser_language": "zh-CN",
        "browser_platform": "MacIntel",
        "browser_name": "Chrome",
        "browser_version": "111.0.0.0",
        "browser_online": True,
        "engine_name": "Blink",
        "engine_version": "111.0.0.0",
        "os_name": "Mac OS",
        "os_version": "10.15.7",
        "cpu_core_num": 4,
        "device_memory": 8,
        "platform": "PC",
        "downlink": 1.25,
        "effective_type": "3g",
        "round_trip_time": 600,
        "webid": 7200371968238700047,
        "msToken": cookies["msToken"]
    }
    params["X-Bogus"] = get_xbogus(params)

    res = session.post(
        "https://www.douyin.com/aweme/v1/web/aweme/post/",
        cookies=cookies,
        headers=HEADERS,
        params=params
    )
    return res


def get_video_playurl(session: Session, cookies: RequestsCookieJar, aweme_id: str) -> str:
    url = VIDEO_URL + aweme_id
    res = session.get(url, cookies=cookies, headers=HEADERS)
    txt = parse.unquote(res.text)
    links = re.search(
        r"//v26-web.douyinvod.com/[^\s|^'|^\"]+", txt)
    if links:
        link = links.group()
        return f"https:{link}"
    raise InvalidCookiesError("未能解析视频源地址")


def get_user_info(session: Session, cookies: RequestsCookieJar, sec_user_id: str) -> Response:
    params = {
        "device_platform": "webapp",
        "aid": 6383,
        "channel": "channel_pc_web",
        "publish_video_strategy_type": 2,
        "source": "channel_pc_web",
        "sec_user_id": sec_user_id,
        "pc_client_type": 1,
        "version_code": 170400,
        "version_name": "17.4.0",
        "cookie_enabled": True,
        "screen_width": 1440,
        "screen_height": 900,
        "browser_language": "zh-CN",
        "browser_platform": "MacIntel",
        "browser_name": "Chrome",
        "browser_version": "111.0.0.0",
        "browser_online": True,
        "engine_name": "Blink",
        "engine_version": "111.0.0.0",
        "os_name": "Mac OS",
        "os_version": "10.15.7",
        "cpu_core_num": 4,
        "device_memory": 8,
        "platform": "PC",
        "downlink": 3.8,
        "effective_type": "4g",
        "round_trip_time": 50,
        "webid": 7200371968238700047,
        "msToken": cookies["msToken"],
    }
    params["X-Bogus"] = get_xbogus(params)

    return session.get(AWEME_V1_WEB_USER_PROFILE_OTHER_URL, cookies=cookies, headers=HEADERS, params=params)

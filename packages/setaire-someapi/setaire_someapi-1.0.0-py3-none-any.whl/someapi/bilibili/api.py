'''
 # @ Author: tuweifeng
 # @ Create Time: 2022-07-12 21:34:08
 # @ Modified by: tuweifeng
 # @ Modified time: 2023-02-23 18:19:15
 # @ Description:

 '''

from requests import Session, Response
from requests.cookies import RequestsCookieJar
from ..bilibili import HEADERS

X_RELATION_FOLLOWERS_URL = "https://api.bilibili.com/x/relation/followers"

X_SPACE_MYINFO_URL = "https://api.bilibili.com/x/space/myinfo"
X_SPACE_ACC_INFO_URL = "https://api.bilibili.com/x/space/acc/info"
X_SPACE_WBI_ARC_SEARCH_URL = "https://api.bilibili.com/x/space/wbi/arc/search"
X_SPACE_WBI_ACC_INFO_URL = "https://api.bilibili.com/x/space/wbi/acc/info"

X_PLAYER_PLAYURL_URL = "https://api.bilibili.com/x/player/playurl"

X_V2_REPLY_ADD_URL = "https://api.bilibili.com/x/v2/reply/add"
X_V2_REPLY_TOP_URL = "https://api.bilibili.com/x/v2/reply/top"

X_WEB_INTERFACE_SEARCH_TYPE_URL = "https://api.bilibili.com/x/web-interface/search/type"
X_WEB_INTERFACE_VIEW_URL = "https://api.bilibili.com/x/web-interface/view"
X_WEB_INTERFACE_VIEW_DETAIL_URL = "https://api.bilibili.com/x/web-interface/view/detail"


def get_followers(session: Session, cookies: RequestsCookieJar) -> Response:
    return session.get(cookies=cookies, url=X_RELATION_FOLLOWERS_URL, headers=HEADERS, params={
        "vmid": cookies.get("DedeUserID"),
        "platform": "web",
        "jsonp": "jsonp"
    })


def get_myinfo(session: Session, cookies: RequestsCookieJar) -> Response:
    return session.get(cookies=cookies, url=X_SPACE_MYINFO_URL,  headers=HEADERS,  params={
        "platform": "web",
        "jsonp": "jsonp"
    })


def get_playurl(session: Session, cookies: RequestsCookieJar, bvid: str, cid: int) -> Response:
    return session.get(url=X_PLAYER_PLAYURL_URL, cookies=cookies,  headers=HEADERS,  params={
        "cid": cid,
        "bvid": bvid,
        "qn": 1,
        "otype": "json",
        "platform": "html5",
        "high_quality": 1
    })


def get_playurl2(session: Session, cookies: RequestsCookieJar, bvid: str, cid: int) -> Response:
    return session.get(url=X_PLAYER_PLAYURL_URL, cookies=cookies,  headers=HEADERS,  params={
        "cid": cid,
        "bvid": bvid,
        "qn": 32,
        "otype": "json",
        "fourk": 1,
        "fnver": 0,
        "fnval": 4048,
    })


def add_reply(session: Session, cookies: RequestsCookieJar, aid: int, message: str) -> Response:
    return session.post(url=X_V2_REPLY_ADD_URL, cookies=cookies,  headers=HEADERS,  data={
        "csrf": cookies["bili_jct"],
        "message": message,
        "oid": aid,
        "plat": 1,
        "type": 1
    })


def top_reply(session: Session, cookies: RequestsCookieJar, aid: int, rpid: int) -> Response:
    return session.post(url=X_V2_REPLY_TOP_URL, cookies=cookies,  headers=HEADERS,  data={
        "action": 1,
        "csrf": cookies["bili_jct"],
        "oid": aid,
        "rpid": rpid,
        "type": 1
    })


def search_user_videos(session: Session, cookies: RequestsCookieJar, mid: int, keyword: str, page: int, page_size: int) -> Response:
    return session.get(cookies=cookies, url=X_SPACE_WBI_ARC_SEARCH_URL,  headers=HEADERS,  params={
        "mid": mid,
        "ps": page_size,
        "tid": 0,
        "pn": page,
        "keyword": keyword,
        "order": "pubdate",
        "order_avoided": True,
        "w_rid": "7c4c1a2c884c9d05370b801bbc29f781",
        "wts": 1677827601,
    })


def search_users(session: Session, cookies: RequestsCookieJar, keyword: str, page: int, page_size: int) -> Response:
    return session.get(cookies=cookies, url=X_WEB_INTERFACE_SEARCH_TYPE_URL,  headers=HEADERS,  params={
        "page": page,
        "page_size": page_size,
        "keyword": keyword,
        "search_type": "bili_user",
    })


def search_videos(session: Session, cookies: RequestsCookieJar, keyword: str, page: int, page_size: int, tid: int, order: str, duration_type: int) -> Response:
    return session.get(cookies=cookies, url=X_WEB_INTERFACE_SEARCH_TYPE_URL,  headers=HEADERS,  params={
        "order": order,
        "duration": duration_type,
        "tids": tid,
        "page": page,
        "page_size": page_size,
        "keyword": keyword,
        "search_type": "video",
        "__refresh__": True,
        "_extra": None,
        "context": None,
        "from_source": None,
        "from_spmid": 333.337,
        "platform": "pc",
        # "highlight": 1,
        "single_column": 0,
        "category_id": None,
        "dynamic_offset": 0,
        "preload": True,
        "com2co": True
    })


def get_spaceinfo(session: Session, cookies: RequestsCookieJar) -> Response:
    return session.get(cookies=cookies, url=X_SPACE_ACC_INFO_URL,  headers=HEADERS,  params={
        "mid": cookies.get("DedeUserID"),
        "platform": "web",
        "jsonp": "jsonp"
    })


def get_videoinfo(session: Session, cookies: RequestsCookieJar, bvid: str) -> Response:
    return session.get(url=X_WEB_INTERFACE_VIEW_URL, cookies=cookies,  headers=HEADERS,  params={"bvid": bvid})


def get_detail_videoinfo(session: Session, cookies: RequestsCookieJar, bvid: str) -> Response:
    return session.get(url=X_WEB_INTERFACE_VIEW_DETAIL_URL, cookies=cookies,  headers=HEADERS,  params={"bvid": bvid})


def get_user_info(session: Session, mid: str) -> Response:
    return session.get(url=X_SPACE_WBI_ACC_INFO_URL, headers=HEADERS, params={"mid": mid})

'''
 # @ Author: tuweifeng
 # @ Create Time: 2022-07-12 21:34:08
 # @ Modified by: tuweifeng
 # @ Modified time: 2023-02-23 18:19:15
 # @ Description:

 '''

import datetime
from requests import Session, Response
from requests.cookies import RequestsCookieJar
from ..bilibili import HEADERS

PREUPLOAD_URL = "https://member.bilibili.com/preupload"

X_VU_WEB_ADD_URL = "https://member.bilibili.com/x/vu/web/add"
X_VU_WEB_COVER_UP_URL = "https://member.bilibili.com/x/vu/web/cover/up"
X_VUPRE_WEB_TOPIC_SEARCH_URL = "https://member.bilibili.com/x/vupre/web/topic/search"
X_VUPRE_WEB_ARCHIVE_TYPES_PREDICT_URL = "https://member.bilibili.com/x/vupre/web/archive/types/predict"
X2_CREATIVE_H5_CLOCK_V4_ACTIVITY_LIST_URL = "https://member.bilibili.com/x2/creative/h5/clock/v4/activity/list"
X2_CREATIVE_H5_CLOCK_V4_ACTIVITY_JOIN_URL = "https://member.bilibili.com/x2/creative/h5/clock/v4/activity/join"


def add_video(session: Session, cookies: RequestsCookieJar, filename: str, title: str, tid: int, tag: str, subtitle: int = 0, recreate: int = 0, up_close_danmu: bool = False, up_close_reply: bool = False, up_selection_reply: bool = False, lang: str = "zh-CN", desc: str = "", dynamic: str = "", open_elec: int = 1, cover: str = "", copyright: int = 1, source: str = "", no_reprint: int = 0, interactive: int = 0, topic_id: int = None) -> Response:
    addinfo = {
        "copyright": copyright,
        "source": source,
        "videos": [{
            "filename": filename,
            "title": title,
            "desc": "",
        }],
        "no_reprint": no_reprint,
        "interactive": interactive,
        "tid": tid,
        "cover": cover,
        "title": title,
        "tag": tag,
        "desc_format_id": 0,
        "desc": desc,
        "dynamic": dynamic,
        "open_elec": open_elec,
        "subtitle": {
            "open": subtitle,
            "lan": lang
        },
        "up_selection_reply": up_selection_reply,
        "up_close_reply": up_close_reply,
        "up_close_danmu": up_close_danmu,
        "recreate": recreate,
    }

    if topic_id:
        addinfo.update({
            "topic_id": topic_id,
            "topic_detail": {
                "from_topic_id": topic_id,
                "from_source": "arc.web.search"
            },
        })

    return session.post(url=X_VU_WEB_ADD_URL, cookies=cookies, params={"csrf": cookies["bili_jct"]}, json=addinfo, headers=HEADERS)


def preupload_video(session: Session, cookies: RequestsCookieJar, name: str, size: int) -> Response:
    return session.get(url=PREUPLOAD_URL, cookies=cookies, headers=HEADERS, params={
        "name": name,
        "size": size,
        "r": "upos",
        "profile": "ugcupos/bup",
        "ssl": "0",
        "version": "2.10.4",
        "build": "2100400",
        "upcdn": "bda2",
        "probe_version": "20200810"
    })


def upload_cover(session: Session, cookies: RequestsCookieJar, cover_base64: bytes) -> Response:
    return session.post(url=X_VU_WEB_COVER_UP_URL, headers=HEADERS, cookies=cookies, data={
        'cover': cover_base64,
        'csrf': cookies["bili_jct"],
    })


def search_topic(session: Session, cookies: RequestsCookieJar, keywords: str, size: int = 20) -> Response:
    params = {
        "keywords": keywords,
        "page_size": size,
        "offset": 0,
        "t": int(datetime.datetime.now().timestamp() * 1000),
    }
    return session.get(X_VUPRE_WEB_TOPIC_SEARCH_URL, headers=HEADERS, cookies=cookies, params=params)


def search_channel(session: Session, cookies: RequestsCookieJar, keywords: str, filename: str) -> Response:
    params = {
        "csrf": cookies["bili_jct"],
        "t": int(datetime.datetime.now().timestamp() * 1000),
    }
    payload = f'''------WebKitFormBoundaryemOwNHRDIk9XcueM
Content-Disposition: form-data; name="title"

{keywords}
------WebKitFormBoundaryemOwNHRDIk9XcueM
Content-Disposition: form-data; name="upload_id"

{cookies['DedeUserID']}_{int(datetime.datetime.now().timestamp() * 1000)}_3919
------WebKitFormBoundaryemOwNHRDIk9XcueM
Content-Disposition: form-data; name="filename"

{filename}
------WebKitFormBoundaryemOwNHRDIk9XcueM--'''
    return session.post(X_VUPRE_WEB_ARCHIVE_TYPES_PREDICT_URL, headers={
        "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryemOwNHRDIk9XcueM",
        **HEADERS
    }, cookies=cookies, params=params, data=payload.encode("utf8"))


def list_activity(session: Session, cookies: RequestsCookieJar) -> Response:
    return session.get(X2_CREATIVE_H5_CLOCK_V4_ACTIVITY_LIST_URL, cookies=cookies, headers=HEADERS, params={
        "act_type": 0,
        "csrf": cookies["bili_jct"],
        "s_locale": "zh_CN",
    })


def join_activity(session: Session, cookies: RequestsCookieJar, act_id: int) -> Response:
    payload = f'''act_id={act_id}&csrf={cookies["bili_jct"]}&s_locale=zh_CN'''
    return session.post(X2_CREATIVE_H5_CLOCK_V4_ACTIVITY_JOIN_URL, cookies=cookies, headers={
        "content-type": "application/x-www-form-urlencoded",
        **HEADERS
    }, data=payload.encode("utf8"))

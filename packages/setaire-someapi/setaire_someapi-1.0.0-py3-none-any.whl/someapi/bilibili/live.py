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

ROOM_V1_ROOM_START_LIVE_URL = "https://api.live.bilibili.com/room/v1/Room/startLive"


def start_live(session: Session, cookies: RequestsCookieJar, room_id: int, area_v2: int) -> Response:
    return session.post(cookies=cookies, url=ROOM_V1_ROOM_START_LIVE_URL, headers=HEADERS, params={
        'room_id': room_id,
        'area_v2': area_v2,
        'platform': "pc",
        'csrf': cookies["bili_jct"],
    })

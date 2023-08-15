'''
 # @ Author: tuweifeng
 # @ Create Time: 2023-03-18 13:00:34
 # @ Modified by: tuweifeng
 # @ Modified time: 2023-03-18 14:09:58
 # @ Description:
    分享视频解析接口
 '''


from requests import Session
from requests.cookies import RequestsCookieJar

from ..bilibili import HEADERS

URL = "https://b23.tv/"


def trans_url(session: Session, cookies: RequestsCookieJar, url: str) -> str:
    res = session.get(url, headers=HEADERS, cookies=cookies)
    return res.url

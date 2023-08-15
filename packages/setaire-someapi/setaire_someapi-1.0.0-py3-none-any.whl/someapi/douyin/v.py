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

from ..douyin import HEADERS

URL = "https://v.douyin.com/"


def trans_url(session: Session, cookies: RequestsCookieJar, url: str) -> str:
    if not url.startswith(URL):
        raise Exception(f"{url} 格式错误, 只能转换分享口令的url {URL}")

    res = session.get(url, headers=HEADERS, cookies=cookies)
    return res.url

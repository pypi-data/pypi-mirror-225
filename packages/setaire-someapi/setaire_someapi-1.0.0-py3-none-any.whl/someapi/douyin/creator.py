from requests import Session, Response
from requests.cookies import RequestsCookieJar

from ..douyin import HEADERS

WEB_API_MEDIA_USER_INFO_URL = "https://creator.douyin.com/web/api/media/user/info/"


def get_userinfo(session: Session, cookies: RequestsCookieJar) -> Response:
    return session.get(WEB_API_MEDIA_USER_INFO_URL, headers=HEADERS, cookies=cookies)

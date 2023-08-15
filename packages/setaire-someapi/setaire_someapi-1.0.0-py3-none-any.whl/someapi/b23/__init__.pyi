
from requests import Session
from requests.cookies import RequestsCookieJar


def trans_url(session: Session, cookies: RequestsCookieJar, url: str) -> str:
    """转换分享口令中url

    Args:
        session (Session): 可能需要代理
        cookies (RequestsCookieJar): 抓包获取
        url (str): 分享口令中的url
            https://b23.tv/hR6J1YF

    Returns:
        str: url

            ```https://space.bilibili.com/255842890?plat_id=1&share_from=space&share_medium=android&share_plat=android&share_session_id=3121be90-dfea-42cb-a95a-807b55a9f34a&share_source=COPY&share_tag=s_i&timestamp=1679276559&unique_k=hR6J1YF```

    """

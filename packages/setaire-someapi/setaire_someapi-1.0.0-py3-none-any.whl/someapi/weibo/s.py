'''
 # @ Author: tuweifeng
 # @ Create Time: 2023-02-28 21:42:28
 # @ Modified by: tuweifeng
 # @ Modified time: 2023-02-28 21:42:41
 # @ Description:
    
 '''


from requests import Session, Response
from requests.cookies import RequestsCookieJar

VIDEO_URL = "https://s.weibo.com/video"


def get_hot_videos(session: Session, cookies: RequestsCookieJar, keyword: str) -> Response:
    """获取热门视频页面

    Args:
        session (Session, optional): Session实例对象
              可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取
        keyword (str): 关键词

    Returns:
        Response: res.text
            热门视频url需要自行通过正则匹配获得 https://video.weibo.com/show?[^']+
    """
    return session.get(
        VIDEO_URL,
        params={
            "q": keyword,
            "xsort": "hot",
            "hasvideo": 1,
            "tw": "video",
            "Refer": "weibo_video"
        },
        headers={
            "referer": "https://s.weibo.com/weibo",
        },
        cookies=cookies
    )

'''
 # @ Author: tuweifeng
 # @ Create Time: 2023-02-28 22:50:37
 # @ Modified by: tuweifeng
 # @ Modified time: 2023-02-28 22:51:35
 # @ Description:
    访客登陆、更新cookies
 '''


from requests import Session
from requests.cookies import RequestsCookieJar

VISITOR_VISITOR_URL = "https://passport.weibo.com/visitor/visitor?a=incarnate&t=NDoke1WIpyqBznWCZhzV81oakviGkNg5q7KlOcH9eW0%3D&w=2&c=095&gc=&cb=cross_domain&from=weibo&_rand=0.1953321038069844"


def update_visitor_cookies(session: Session, cookies: RequestsCookieJar):
    """更新 visitor cookies

    Args:
        session (Session, optional): Session实例对象
              可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取
    """
    visitor_cookies = session.get(VISITOR_VISITOR_URL).cookies.get_dict()
    cookies.update(visitor_cookies)

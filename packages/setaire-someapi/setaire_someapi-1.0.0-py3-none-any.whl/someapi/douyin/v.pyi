
from requests import Session
from requests.cookies import RequestsCookieJar

def trans_url(session: Session, cookies: RequestsCookieJar, url: str) -> str:
    """转换分享口令中url

    Args:
        session (Session): 可能需要代理
        cookies (RequestsCookieJar): 抓包获取
        url (str): 分享口令中的url
            https://v.douyin.com/Sv6pvFW/

    Returns:
        str: url

            ```https://www.iesdouyin.com/share/video/7188795449468259623```

            ```https://www.iesdouyin.com/share/user/MS4wLjABAAAAP9IeZhDHS5xRBl20L8d-rDjNFokqnZTBVOw72A1GxzIIezcDJu6QzDCkNa3FsbY2?u_code=33j71mhi576g&did=MS4wLjABAAAAqbvi59FwZKcrYaSBv56CBxMbNvGA_USubf76VhOHbYh_l-LKLZRswqmxpc8e9HxR&iid=MS4wLjABAAAAaCrdKZNPLJs2-kok2raUSIIDVzT2yimB_c85Ru3D67xLPcI4KU38hus5yDU6k0FE&with_sec_did=1&sec_uid=MS4wLjABAAAAP9IeZhDHS5xRBl20L8d-rDjNFokqnZTBVOw72A1GxzIIezcDJu6QzDCkNa3FsbY2&from_ssr=1&timestamp=1679142632&utm_source=copy&utm_campaign=client_share&utm_medium=android&app=aweme```
    """
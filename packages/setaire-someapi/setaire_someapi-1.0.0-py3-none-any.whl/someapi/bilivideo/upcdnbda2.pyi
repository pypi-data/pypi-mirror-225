from typing import List, Dict, Union
from requests import Session, Response
from requests.cookies import RequestsCookieJar


def post_upload_id(session: Session, cookies: RequestsCookieJar, uri: str, auth: str, endpoint: str = "") -> Response:
    """确认开始文件上传, 获取上传ID
        投稿视频的第 2 步

    Args:
        session (Session): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取
        uri (str): 文件网络地址
            从第1步的结果中获取,注意不是本地地址,是准备上传到哔哩哔哩服务器的网络地址,不包含前缀 upos://
        auth (str): 验证
            从第1步的结果中获取
        endpoint (str, optional): 服务器地址, 可为空使用默认服务器 https://upos-sz-upcdnbda2.bilivideo.com

    Returns:
        Response: 返回结果
            成功 {
                "bucket": "svfboss",
                "upload_id": "287cc6b86022b4",
                "key": "/n230223qn3f298l71j5qgmhwaiq26e5z.zip",
                "OK": 1
            }
    """


def post_partinfo(session: Session, cookies: RequestsCookieJar, uri: str, auth: str, name: str, upload_id: str, biz_id: int, partinfo: List[Dict[str, Union[str, int]]], endpoint: str = "") -> Response:
    """确认结束文件上传
        投稿视频的第 4 步

    Args:
        session (Session): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取
        uri (str): 文件网络地址
            从第1步的结果中获取,注意不是本地地址,是准备上传到哔哩哔哩服务器的网络地址,不包含前缀 upos://
        auth (str): 验证
            从第1步的结果中获取
        name (str): 文件名
        upload_id (str): 上传任务ID
            从第2步的结果中获取
        biz_id (int): 从第1步的结果中获取
        partinfo (List[Dict[str, Union[str, int]]]): 分块上传结果
            从第3步的结果中获取
        endpoint (str, optional): 服务器地址, 可为空使用默认服务器 https://upos-sz-upcdnbda2.bilivideo.com


    Returns:
        Response: 返回结果
            成功 {
                "OK": 1,
                "location": "ugcfx2lf/n230223qniye63yoclpyx1cdkdwslza6.mp4",
                "key": "/n230223qniye63yoclpyx1cdkdwslza6.mp4",
                "bucket": "ugcfx2lf",
                "etag": "63913027"
            }
    """


def upload_file(session: Session, cookies: RequestsCookieJar, uri: str, auth: str,  upload_id: str, filepath: str,
                chunk_retry: int, chunk_timeout: int, chunk_retry_delay: int, chunk_size: int,
                endpoint: str = "", threads: int = None) -> List[Dict[str, Union[str, int]]]:
    """上传文件
        投稿视频的第 3 步,分块上传

    Args:
        session (Session): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取
        uri (str): 文件网络地址
            从第1步的结果中获取,注意不是本地地址,是准备上传到哔哩哔哩服务器的网络地址,不包含前缀 upos://
        auth (str): 验证
            从第1步的结果中获取
        upload_id (str): 上传任务ID
            从第2步的结果中获取
        filepath (str): 本地文件位置
        chunk_retry (int): 重试次数(从第1步的结果中获取)
        chunk_timeout (int): 超时时间(从第1步的结果中获取) 单位秒
        chunk_retry_delay (int): 重试延迟时间(从第1步的结果中获取) 单位秒
        chunk_size (int): 分块大小(从第1步的结果中获取)
        endpoint (str, optional): 服务器地址(从第1步的结果中获取), 可为空使用默认服务器 https://upos-sz-upcdnbda2.bilivideo.com
        threads (int, optional): 线程数量(从第1步的结果中获取)

    Returns:
        List[Dict[str, Union[str, int]]]: 每个分块的上传结果

    """

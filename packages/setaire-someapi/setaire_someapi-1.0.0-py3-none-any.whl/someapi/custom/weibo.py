'''
 # @ Author: tuweifeng
 # @ Create Time: 2023-02-28 22:59:42
 # @ Modified by: tuweifeng
 # @ Modified time: 2023-02-28 23:01:00
 # @ Description:
    封装一些视频接口的方法、比如下载
 '''
from types import MappingProxyType
from sometools.utils.sessions import create_cookies, RestSession
from sometools.https import downloader
from .import utils
from .. import weibo

HEADERS = MappingProxyType({
    "origin": "https://www.bilibili.com",
    "referer": "https://www.bilibili.com/video/BV1iK411i7we/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=757531d6b126670d71e42bf9d8793271",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
})
THREAD = 4
CHUNKSIZE = 1024*1024*2


def download_video(url: str, path: str, cookies: str):
    """下载视频

    Args:
        url (str): 视频页面url
        path (str): 文件保存位置
            例如: https://weibo.com/tv/show/1034:4874232547704963?mid=4874232813323812
        cookies (str): 在浏览器中登录账号抓包获取
    """
    if cookies:
        cookies = create_cookies(cookies)
    oid = utils.get_weibovideo_oid_by_url(url)
    with RestSession(timeout=3, max_retries=1) as session:
        playinfo = weibo.get_playinfo(session, cookies, oid).json()
        videoUrl = playinfo["data"]["Component_Play_Playinfo"]["urls"]["高清 720P"]
    videoUrl = f"http:{videoUrl}"
    downloader.AsyncDownloader(
        videoUrl, path, THREAD, CHUNKSIZE, HEADERS).start()

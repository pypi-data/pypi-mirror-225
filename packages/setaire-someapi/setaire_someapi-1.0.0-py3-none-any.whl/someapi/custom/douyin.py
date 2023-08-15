'''
 # @ Author: tuweifeng
 # @ Create Time: 2023-03-18 12:32:41
 # @ Modified by: tuweifeng
 # @ Modified time: 2023-03-18 14:07:08
 # @ Description:
    抖音相关接口、视频解析下载
 '''


import re
from sometools.utils.sessions import create_cookies, RestSession
from sometools.https import downloader
from .. import douyin
from ..douyin import v


THREAD = 4
CHUNKSIZE = 1024*1024*2


def get_user_info(url: str, cookies: str) -> dict:
    url = re.search(r"http[s]*://[^\s]*", url).group()
    cookies = create_cookies(cookies)
    with RestSession(timeout=10) as session:
        if url.startswith(v.URL):
            url = v.trans_url(session, None, url)

        sec_user_id = re.search(r"user/([\w-]+)", url).group(1)
        data = douyin.get_user_info(session, cookies, sec_user_id).json()
    return data


def parse_video(url: str, cookies: str) -> str:
    url = re.search(r"http[s]*://[^\s]*", url).group()
    cookies = create_cookies(cookies)

    with RestSession(timeout=10) as session:
        if url.startswith(v.URL):
            url = v.trans_url(session, cookies, url)
        res = re.search(r"video/(\d+)", url)
        if not res:
            return
        aweme_id = res.group(1)
        playurl = douyin.get_video_playurl(session, cookies, aweme_id)
    return playurl


def download_video(url: str, videopath: str, cookies: str):
    playurl = parse_video(url, cookies)
    downloader.AsyncDownloader(
        playurl, videopath, THREAD, CHUNKSIZE, douyin.HEADERS).start()

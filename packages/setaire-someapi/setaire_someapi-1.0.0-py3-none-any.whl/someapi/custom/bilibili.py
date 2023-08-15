'''
 # @ Author: tuweifeng
 # @ Create Time: 2023-02-23 19:54:58
 # @ Modified by: tuweifeng
 # @ Modified time: 2023-02-23 19:55:09
 # @ Description:
    与b站相关的一些方法

 '''
import os
import re
import random
from typing import Tuple, Dict
from sometools.utils.sessions import create_cookies, RestSession
from sometools.https import downloader
from sometools.utils.files import img2base64v2
from sometools.videos import patch_moviepy
from moviepy.editor import VideoFileClip
from ..bilibili import api, member, HEADERS
from ..bilivideo import upcdnbda2
from . import utils
from .. import b23
import logging

logger = logging.getLogger(__name__)

patch_moviepy()


THREAD = 4
CHUNKSIZE = 1024*1024*2


def upload_video(cookies: str, filepath: str, title: str, tid: int, tag: str, subtitle: int = 0, recreate: int = 0,
                 up_close_danmu: bool = False, up_close_reply: bool = False, up_selection_reply: bool = False,
                 lang: str = "zh-CN", desc: str = "", dynamic: str = "", open_elec: int = 1, cover: str = "",
                 copyright: int = 1, source: str = "", no_reprint: int = 0, interactive: int = 0, topic_id: int = None) -> dict:

    logger.info(f'''upload_video args:
        filepath: {filepath}, title: {title}, tid: {tid}, tag: {tag}, subtitle: {subtitle}, recreate: {recreate}, up_close_danmu: {up_close_danmu}, up_close_reply: {up_close_reply}, up_selection_reply: {up_selection_reply}, lang: {lang}, desc: {desc}, dynamic: {dynamic}, open_elec: {open_elec}, cover: {cover}, copyright: {copyright}, source: {source}, no_reprint: {no_reprint}, interactive: {interactive}, topic_id: {topic_id}
    ''')
    name = os.path.basename(filepath)
    size = os.path.getsize(filepath)
    cookies = create_cookies(cookies)

    with RestSession(timeout=10, max_retries=1) as session:
        res = member.preupload_video(session, cookies, name, size).json()
        zip_url = res["upos_uri"]
        uri = zip_url[len("upos://"):]
        biz_id = res["biz_id"]
        auth = res["auth"]
        chunk_size = res["chunk_size"]
        chunk_retry = res["chunk_retry"]
        chunk_timeout = res["timeout"]
        chunk_retry_delay = res["chunk_retry_delay"]
        endpoint = f"https:{res['endpoint']}"
        threads = res["threads"]
        res = upcdnbda2.post_upload_id(
            session, cookies, uri, auth, endpoint).json()
        upload_id = res["upload_id"]

    with RestSession() as session:
        partinfo = upcdnbda2.upload_file(session, cookies, uri, auth, upload_id, filepath,
                                         chunk_retry, chunk_timeout, chunk_retry_delay, chunk_size, endpoint, threads)

    with RestSession(timeout=10, max_retries=1) as session:
        upcdnbda2.post_partinfo(session, cookies, uri, auth,
                                name, upload_id, biz_id, partinfo, endpoint).json()

    with RestSession(timeout=10, max_retries=0) as session:
        uploaded_cover_url = ''
        try:
            cover_base64 = img2base64v2(cover)
            if cover_base64:
                res = member.upload_cover(
                    session, cookies, cover_base64).json()
                uploaded_cover_url = res["data"]["url"]
        except Exception as e:
            logger.error(f"上传封面错误 {e}")

    with RestSession(timeout=10, max_retries=1) as session:
        filename = os.path.splitext(uri.split("/")[-1])[0]
        keywords = tag.split(",")[0]

        if not tid:
            channel_info = member.search_channel(
                session, cookies, keywords, filename).json()
            tid = channel_info["data"][0]["id"]

        if not topic_id:
            topic_info = member.search_topic(
                session, cookies, keywords, 10).json()
            topics = topic_info["data"]["result"]["topics"]
            if topics:
                random.shuffle(topics)
                topic_id = topics[0]["id"]

        logger.info(f'''member.add_video args:
        filename: {filename}, title: {title}, tid: {tid}, tag: {tag}, subtitle: {subtitle}, recreate: {recreate}, up_close_danmu: {up_close_danmu}, up_close_reply: {up_close_reply}, up_selection_reply: {up_selection_reply}, lang: {lang}, desc: {desc}, dynamic: {dynamic}, open_elec: {open_elec}, cover: {uploaded_cover_url}, copyright: {copyright}, source: {source}, no_reprint: {no_reprint}, interactive: {interactive}, topic_id: {topic_id}
        ''')
        res = member.add_video(session, cookies, filename, title, tid, tag, subtitle, recreate, up_close_danmu, up_close_reply,
                               up_selection_reply, lang, desc, dynamic, open_elec, uploaded_cover_url, copyright, source, no_reprint, interactive, topic_id).json()
    return res


def view_video(url: str, cookies: str = None) -> Tuple[Dict, Dict, Dict]:
    cookies = create_cookies(cookies)
    bvid = utils.get_bilivideo_bvid_by_url(url)
    with RestSession(timeout=10, max_retries=1) as session:
        viewInfo = api.get_videoinfo(session, cookies, bvid).json()
        cid = viewInfo["data"]["cid"]
        playinfo = api.get_playurl(session, cookies, bvid, cid).json()
        playinfo2 = api.get_playurl2(session, cookies, bvid, cid).json()

    return viewInfo, playinfo, playinfo2


def parse_video(url: str, cookies: str = None) -> str:
    _, playinfo, _ = view_video(url, cookies)
    return playinfo["data"]["durl"][0]["url"]


def parse_video_audio(url: str, cookies: str = None) -> Tuple[str, str]:
    _, _, playinfo2 = view_video(url, cookies)
    video_url = playinfo2["data"]["dash"]["video"][0]["baseUrl"]
    audio_url = playinfo2["data"]["dash"]["audio"][0]["baseUrl"]
    return video_url, audio_url


def download_custom_video(url: str, filepath: str):
    fileUrl = parse_video(url, None)
    downloader.AsyncDownloader(
        fileUrl, filepath, THREAD, CHUNKSIZE, HEADERS).start()


def download_video(url: str, filepath: str, cookies: str = None):
    if not cookies:
        download_custom_video(url, filepath)
        return

    temp_audiopath = f"{filepath}_temp.mp3"
    temp_videopath = f"{filepath}_temp.mp4"
    download_video_audio(url, temp_videopath, temp_audiopath, cookies)

    clip = VideoFileClip(temp_videopath)
    clip = clip.add_loop_audio(temp_audiopath)

    clip.my_write_videofile(filepath, remove_files=(
        temp_audiopath, temp_videopath))


def download_video_audio(url: str, videopath: str, audiopath: str, cookies: str = None):
    video_url, audio_url = parse_video_audio(url, cookies)

    downloader.AsyncDownloader(
        video_url, videopath, THREAD, CHUNKSIZE, HEADERS).start()

    downloader.AsyncDownloader(
        audio_url, audiopath, THREAD, CHUNKSIZE, HEADERS).start()


def download_video_without_audio(url: str, videopath: str, cookies: str = None):
    video_url, _ = parse_video_audio(url, cookies)

    downloader.AsyncDownloader(
        video_url, videopath, THREAD, CHUNKSIZE, HEADERS).start()


def download_audio(url: str,  audiopath: str, cookies: str = None):
    _, audio_url = parse_video_audio(url, cookies)

    downloader.AsyncDownloader(
        audio_url, audiopath, THREAD, CHUNKSIZE, HEADERS).start()


def get_user_videos(mid: int, page: int, page_size: int = 30, keyword: str = "", cookies: str = None) -> dict:
    cookies = create_cookies(cookies)
    with RestSession(timeout=10) as session:
        res = api.search_user_videos(
            session, cookies, mid, keyword, page, page_size).json()
    return res


def download_delogo_video(url: str, videopath: str, cookies: str = None, t_start=0, t_end=0):
    temp_audiopath = f"{videopath}.mp3"
    temp_videopath = f"{videopath}.mp4"
    download_video_audio(url, temp_videopath, temp_audiopath, cookies)

    clip = VideoFileClip(temp_videopath)
    clip = clip.delogo()
    clip = clip.add_loop_audio(temp_audiopath)

    if t_start == 0 and t_end == 0:
        pass
    else:
        if t_end <= 0:
            t_end = clip.duration + t_end
        else:
            t_end = t_end
        clip = clip.subclip(t_start=t_start, t_end=t_end)

    clip.my_write_videofile(videopath, remove_files=(
        temp_audiopath, temp_videopath))


def get_user_info(url: str) -> dict:
    url = re.search(r"http[s]*://[^\s]*", url).group()
    with RestSession(timeout=10) as session:
        if url.startswith(b23.URL):
            url = b23.trans_url(session, None, url)
        mid = re.search(r"space.bilibili.com/(\d+)", url).group(1)
        user_info = api.get_user_info(session, mid).json()
    return user_info


def join_all_activity(cookies: str):
    cookies = create_cookies(cookies)
    with RestSession(timeout=10) as session:
        res = member.list_activity(session, cookies)
        data = res.json()
        for activity in data["data"]["list"]:
            if activity["icon_state"] == 0:
                member.join_activity(session, cookies, activity["act_id"])

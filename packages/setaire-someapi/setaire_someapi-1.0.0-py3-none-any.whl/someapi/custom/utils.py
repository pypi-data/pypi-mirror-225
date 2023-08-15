'''
 # @ Author: tuweifeng
 # @ Create Time: 2023-02-23 20:15:02
 # @ Modified by: tuweifeng
 # @ Modified time: 2023-02-23 20:15:37
 # @ Description:
    一些常用且共用的方法和类
 '''
import re
from typing import List
import logging

logger = logging.getLogger("someapi")


def get_bilivideo_bvid_by_url(url: str):
    result = re.search(r'/video/(\w+)(|[/|^\w]|$)', url)
    if result:
        return result.group(1)
    return ''


def get_weibovideo_oid_by_url(url: str) -> str:
    """从 url 匹配 oid

    Args:
        url (str): 微博视频页面url

    Returns:
        str: oid
    """

    result = re.search(r'(\d{4}:\d+)', url)
    if result:
        return result.group(1)
    return ''


def get_all_weibohotvideos_url_by_htmltxt(html_txt: str) -> List[str]:
    """从html文本中获取所有热门视频的 url

    Args:
        htmlTxt (str): html文本

    Returns:
        List[str]: 热门视频url列表
    """
    urls = re.findall(r"(https://video.weibo.com/show?[^']+)", html_txt)
    return urls

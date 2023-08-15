from typing import Tuple, Dict


def join_all_activity(cookies: str):
    """ 参加所有活动

    Args:
        cookies (str): 抓包获取
    """


def get_user_info(url: str) -> dict:
    """获取用户信息

    Args:
        url (str): 用户空间地址

            ```https://space.bilibili.com/334445736?spm_id_from=333.1007.tianma.1-1-1.click```

            支持分享口令

            ```【浅梦-Dream的个人空间-哔哩哔哩】 https://b23.tv/hR6J1YF```

    Returns:
        dict: 用户基本信息
{
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "mid": 334445736,
    "name": "我真是朱有才",
    "sex": "保密",
    "face": "https://i0.hdslb.com/bfs/face/c0cd7e946e101f7db1845e1c4fc780d9f4198e06.jpg",
    "face_nft": 0,
    "face_nft_type": 0,
    "sign": "一个娱乐博主：荣耀直通车，黄金追梦人！\n合作：youcai1319(请备注来意）",
    "rank": 10000,
    "level": 6,
    "jointime": 0,
    "moral": 0,
    "silence": 0,
    "coins": 0,
    "fans_badge": true,
    "fans_medal": {
      "show": false,
      "wear": false,
      "medal": null
    },
    "official": {
      "role": 2,
      "title": "游戏解说UP主",
      "desc": "",
      "type": 0
    },
    "vip": {
      "type": 2,
      "status": 1,
      "due_date": 1710172800000,
      "vip_pay_type": 0,
      "theme_type": 0,
      "label": {
        "path": "",
        "text": "年度大会员",
        "label_theme": "annual_vip",
        "text_color": "#FFFFFF",
        "bg_style": 1,
        "bg_color": "#FB7299",
        "border_color": "",
        "use_img_label": true,
        "img_label_uri_hans": "",
        "img_label_uri_hant": "",
        "img_label_uri_hans_static": "https://i0.hdslb.com/bfs/vip/8d4f8bfc713826a5412a0a27eaaac4d6b9ede1d9.png",
        "img_label_uri_hant_static": "https://i0.hdslb.com/bfs/activity-plat/static/20220614/e369244d0b14644f5e1a06431e22a4d5/VEW8fCC0hg.png"
      },
      "avatar_subscript": 1,
      "nickname_color": "#FB7299",
      "role": 3,
      "avatar_subscript_url": "",
      "tv_vip_status": 0,
      "tv_vip_pay_type": 0
    },
    "pendant": {
      "pid": 0,
      "name": "",
      "image": "",
      "expire": 0,
      "image_enhance": "",
      "image_enhance_frame": ""
    },
    "nameplate": {
      "nid": 8,
      "name": "知名偶像",
      "image": "https://i1.hdslb.com/bfs/face/27a952195555e64508310e366b3e38bd4cd143fc.png",
      "image_small": "https://i1.hdslb.com/bfs/face/0497be49e08357bf05bca56e33a0637a273a7610.png",
      "level": "稀有勋章",
      "condition": "所有自制视频总播放数>=100万"
    },
    "user_honour_info": {
      "mid": 0,
      "colour": null,
      "tags": []
    },
    "is_followed": false,
    "top_photo": "http://i1.hdslb.com/bfs/space/cb1c3ef50e22b6096fde67febe863494caefebad.png",
    "theme": {},
    "sys_notice": {},
    "live_room": {
      "roomStatus": 1,
      "liveStatus": 0,
      "url": "https://live.bilibili.com/22365333?broadcast_type=0&is_room_feed=0",
      "title": "",
      "cover": "https://s1.hdslb.com/bfs/static/blive/live-assets/common/images/no-cover.png",
      "roomid": 22365333,
      "roundStatus": 0,
      "broadcast_type": 0,
      "watched_show": {
        "switch": true,
        "num": 1,
        "text_small": "1",
        "text_large": "1人看过",
        "icon": "https://i0.hdslb.com/bfs/live/a725a9e61242ef44d764ac911691a7ce07f36c1d.png",
        "icon_location": "",
        "icon_web": "https://i0.hdslb.com/bfs/live/8d9d0f33ef8bf6f308742752d13dd0df731df19c.png"
      }
    },
    "birthday": "",
    "school": {
      "name": ""
    },
    "profession": {
      "name": "",
      "department": "",
      "title": "",
      "is_show": 0
    },
    "tags": null,
    "series": {
      "user_upgrade_status": 3,
      "show_upgrade_window": false
    },
    "is_senior_member": 0,
    "mcn_info": null,
    "gaia_res_type": 0,
    "gaia_data": null,
    "is_risk": false,
    "elec": {
      "show_info": {
        "show": true,
        "state": 1,
        "title": "",
        "icon": "",
        "jump_url": ""
      }
    },
    "contract": null
  }
}
    """


def download_delogo_video(url: str, videopath: str, cookies: str = None, t_start=0, t_end=0):
    """下载去水印视频

    Args:
        url (str): 视频url
        videopath (str): 保存为文件
        cookies (str, optional): 在浏览器中登录账号抓包获取
        t_start (int, optional): 截断开始时间
        t_end (int, optional): 截断结尾时间 如果为 -4 表示截止到结尾前4秒， 如果为 4 则表示截止到第4秒
    """


def get_user_videos(mid: int, page: int, page_size: int = 30, keyword: str = "", cookies: str = None) -> dict:
    """获取用户视频

    Args:
        mid (int): 用户id
        page (int): 页数
        page_size (int, optional): 每页数量
        keyword (str, optional): 关键词
        cookies (str, optional): 可不传

    Returns:
        dict: 接口返回的数据
{
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "list": {
      "tlist": {
        "217": {
          "tid": 217,
          "count": 16,
          "name": "动物圈"
        }
      },
      "vlist": [
        {
          "comment": 17,
          "typeid": 220,
          "play": 36846,
          "pic": "http://i1.hdslb.com/bfs/archive/1fe4470a8ddb7bea6322de3f3f87459921fadb84.jpg",
          "subtitle": "",
          "description": "感谢观看 喜欢的朋友请点个赞吧 谢谢啦",
          "copyright": "1",
          "title": "老鼠：“再见了，世界”",
          "review": 0,
          "author": "乞一世天长地久",
          "mid": 499522409,
          "created": 1677731583,
          "length": "01:37",
          "video_review": 36,
          "aid": 352862224,
          "bvid": "BV1dX4y1S7ux",
          "hide_click": false,
          "is_pay": 0,
          "is_union_video": 0,
          "is_steins_gate": 0,
          "is_live_playback": 0,
          "meta": {
            "id": 927092,
            "title": "老鼠：“再见了，世界”",
            "cover": "https://archive.biliimg.com/bfs/archive/b0910679feb34776e8128759a4ae23f509940439.jpg",
            "mid": 499522409,
            "intro": "⁡ ⁣​⁡⁡",
            "sign_state": 0,
            "attribute": 140,
            "stat": {
              "season_id": 927092,
              "view": 3539367,
              "danmaku": 2145,
              "reply": 1646,
              "favorite": 9141,
              "coin": 2737,
              "share": 2240,
              "like": 98966
            },
            "ep_count": 14,
            "first_aid": 352862224,
            "ptime": 1677731583,
            "ep_num": 0
          },
          "is_avoided": 0,
          "attribute": 0
        },
        {
          "comment": 19,
          "typeid": 220,
          "play": 17382,
          "pic": "http://i2.hdslb.com/bfs/archive/5be1bf00b763812d3322b68a25997446fe419349.jpg",
          "subtitle": "",
          "description": "感谢观看 喜欢的朋友请点个赞吧 谢谢啦",
          "copyright": "1",
          "title": "老鼠：“再见了，世界”",
          "review": 0,
          "author": "乞一世天长地久",
          "mid": 499522409,
          "created": 1677725085,
          "length": "02:57",
          "video_review": 46,
          "aid": 352854295,
          "bvid": "BV1AX4y1D7av",
          "hide_click": false,
          "is_pay": 0,
          "is_union_video": 0,
          "is_steins_gate": 0,
          "is_live_playback": 0,
          "meta": {
            "id": 927092,
            "title": "老鼠：“再见了，世界”",
            "cover": "https://archive.biliimg.com/bfs/archive/b0910679feb34776e8128759a4ae23f509940439.jpg",
            "mid": 499522409,
            "intro": "⁡ ⁣​⁡⁡",
            "sign_state": 0,
            "attribute": 140,
            "stat": {
              "season_id": 927092,
              "view": 3539367,
              "danmaku": 2145,
              "reply": 1646,
              "favorite": 9141,
              "coin": 2737,
              "share": 2240,
              "like": 98966
            },
            "ep_count": 14,
            "first_aid": 352862224,
            "ptime": 1677731583,
            "ep_num": 0
          },
          "is_avoided": 0,
          "attribute": 0
        }
      ]
    },
    "page": {
      "pn": 1,
      "ps": 2,
      "count": 16
    },
    "episodic_button": {
      "text": "播放全部",
      "uri": "//www.bilibili.com/medialist/play/499522409?from=space"
    },
    "is_risk": false,
    "gaia_res_type": 0,
    "gaia_data": null
  }
}
    """


def download_audio(url: str,  audiopath: str, cookies: str = None):
    """下载音频

    Args:
        url (str): 播放页面地址
        audiopath (str): 保存为音频文件位置
        cookies (str, optional): 在浏览器中登录账号抓包获取
            也可不传, 传了后视频清晰度更高
    """


def download_video_without_audio(url: str, videopath: str, cookies: str = None):
    """下载无声视频 (高清晰度)

    Args:
        url (str): 播放页面地址
        videopath (str): 保存为视频文件位置
        cookies (str, optional): 在浏览器中登录账号抓包获取
            也可不传, 传了后视频清晰度更高
    """


def download_video_audio(url: str, videopath: str, audiopath: str, cookies: str = None):
    """下载视频和音频 (高清晰度)
        视频和音频分开，需自行合并
    Args:
        url (str): 播放页面地址
        videopath (str): 保存为视频文件位置
        audiopath (str): 保存为音频文件位置
        cookies (str, optional): 在浏览器中登录账号抓包获取
            也可不传, 传了后视频清晰度更高
    """


def download_custom_video(url: str, filepath: str):
    """下载视频 (低清晰度)
        如果需要高清晰度请用 downloadVideoAudio 方法,分别下载视频和音频，然后自行合并
    Args:
        url (str): 播放页面地址
        filepath (str): 保存为文件位置
    """


def download_video(url: str, filepath: str, cookies: str = None):
    """下载视频

    Args:
        url (str): 播放页面地址
        filepath (str): 保存为文件位置
        cookies (str, optional): 在浏览器中登录账号抓包获取
            也可不传, 传了后视频清晰度更高
    """


def parse_video_audio(url: str, cookies: str = None) -> Tuple[str, str]:
    """解析视频地址 (高清晰度)
        视频和音频分开，需自行合并

    Args:
        url (str): 播放页面地址
        cookies (str, optional): 在浏览器中登录账号抓包获取
            也可不传, 传了后视频清晰度更高

    Returns:
        Tuple[str, str]: 视频和音频文件地址
    """


def parse_video(url: str, cookies: str = None) -> str:
    """解析视频地址 (低清晰度)

    Args:
        url (str): 播放页面地址
        cookies (str, optional): 在浏览器中登录账号抓包获取
            也可不传, 传了后视频清晰度更高

    Returns:
        str: 文件地址
    """


def view_video(url: str, cookies: str = None) -> Tuple[Dict, Dict, Dict]:
    """获取视频信息、播放信息

    Args:
        url (str): 播放页面地址
        cookies (str, optional): 在浏览器中登录账号抓包获取
            也可不传, 传了后视频清晰度更高

    Returns:
        Tuple[Dict, Dict, Dict]: 视频信息, mp4(低清晰度)文件信息, m4a(高清晰度)文件信息
    """


def upload_video(cookies: str, filepath: str, title: str, tid: int, tag: str, subtitle: int = 0, recreate: int = 0,
                 up_close_danmu: bool = False, up_close_reply: bool = False, up_selection_reply: bool = False,
                 lang: str = "zh-CN", desc: str = "", dynamic: str = "", open_elec: int = 1, cover: str = "",
                 copyright: int = 1, source: str = "", no_reprint: int = 0, interactive: int = 0, topic_id: int = None) -> dict:
    """上传视频

    Args:
        cookies (str): 在浏览器中登录账号抓包获取
        filepath (str): 视频文件位置
        title (str): 作品标题
            注意不能和自己的其他作品重复
        tid (int): 分区ID
            搞笑、舞蹈、纪录片、生活、综艺、知识等等分区都有各自的ID
        tag (str): 标签
            多个用逗号隔开“,”egg: 搞笑,综艺
        subtitle (int): 智能字幕开关
            关闭“0”,开启“1”
        recreate (int, optional): 允许二次创作
            禁止“-1”,允许“1”
        up_close_danmu (bool, optional): 弹幕开关
            关闭“True”,开启“False”
        up_close_reply (bool, optional): 评论区开关
            关闭“True”,开启“False”
        up_selection_reply (bool, optional): up精选评论开关
            关闭“False”,开启“True”
        lang (str, optional): 语种
            如果开启,字幕会翻译成相应的语种,默认汉字
        desc (str, optional): 视频简介
        dynamic (str, optional): 视频同时发布到动态,动态标题内容
        open_elec (int, optional): 充电（用户打赏）开关
            关闭“0”,开启“1”
        cover (str, optional): 视频封面,本地图片位置 或者 url
            可以为空,b站会从视频里取一帧作为封面
        copyright (int, optional): 版权
            拥有版权“1”,无版权“2”
        source (str, optional): 视频来源
            视频转载来源,可以不写
        no_reprint (int, optional): 禁止本视频转载
            禁止“1”,允许“0”
        interactive (int, optional): 交互开关
            关闭“0”,开启“1”
        topic_id (int, optional): 参与话题活动
            注意有些话题经常更新,如果话题不存在了也能提交成功

    Returns:
        dict: 返回结果
            成功 {
                "code":0,
                "message":"0",
                "ttl":1,
                "data":{
                    "aid":779951675,
                    "bvid":"BV1Gy4y1o7K1"
                    }
            }
    """

from requests import Session, Response
from requests.cookies import RequestsCookieJar

def get_user_info(session: Session, mid: str) -> Response:
  """获取用户基本信息

  Args:
      session (Session): 可能存在一些需要代理的场景
      mid (str): 用户id

  Returns:
      Response: 返回请求
        成功 
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

def search_user_videos(session: Session, cookies: RequestsCookieJar, mid: int, keyword: str, page: int, page_size: int) -> Response:
    """查询该用户的视频

    Args:
        session (Session, optional): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取
        mid (int): 用户ID
        keyword (str): 关键词
        page (int): 页数
        page_size (int): 每页数量

    Returns:
        Response: 返回请求
          成功 {
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

def get_detail_videoinfo(session: Session, cookies: RequestsCookieJar, bvid: str) -> Response:
    """获取视频详细信息

    Args:
        session (Session, optional): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取
        bvid (str): 视频ID

    Returns:
        Response: 返回结果
        成功 {
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "View": {
      "bvid": "BV16v4y147EP",
      "aid": 566624511,
      "videos": 1,
      "tid": 250,
      "tname": "出行",
      "copyright": 1,
      "pic": "http://i2.hdslb.com/bfs/archive/af4081081cce65740a219dcb68b1e1783e4704f9.jpg",
      "title": "深圳世界之窗春节烟花",
      "pubdate": 1675781219,
      "ctime": 1675781220,
      "desc": "深圳世界之窗春节烟花",
      "desc_v2": [
        {
          "raw_text": "深圳世界之窗春节烟花",
          "type": 1,
          "biz_id": 0
        }
      ],
      "state": 0,
      "duration": 55,
      "mission_id": 1153647,
      "rights": {
        "bp": 0,
        "elec": 0,
        "download": 1,
        "movie": 0,
        "pay": 0,
        "hd5": 0,
        "no_reprint": 1,
        "autoplay": 1,
        "ugc_pay": 0,
        "is_cooperation": 0,
        "ugc_pay_preview": 0,
        "no_background": 0,
        "clean_mode": 0,
        "is_stein_gate": 0,
        "is_360": 0,
        "no_share": 0,
        "arc_pay": 0,
        "free_watch": 0
      },
      "owner": {
        "mid": 1614308159,
        "name": "澎湖湾狠人",
        "face": "https://i2.hdslb.com/bfs/face/4eb307be5329cf4e7fbe944946f3f894207a5ddc.jpg"
      },
      "stat": {
        "aid": 566624511,
        "view": 29,
        "danmaku": 0,
        "reply": 0,
        "favorite": 0,
        "coin": 0,
        "share": 0,
        "now_rank": 0,
        "his_rank": 0,
        "like": 1,
        "dislike": 0,
        "evaluation": "",
        "argue_msg": ""
      },
      "dynamic": "",
      "cid": 997878516,
      "dimension": {
        "width": 1920,
        "height": 1080,
        "rotate": 1
      },
      "premiere": null,
      "teenage_mode": 0,
      "is_chargeable_season": false,
      "is_story": true,
      "no_cache": false,
      "pages": [
        {
          "cid": 997878516,
          "page": 1,
          "from": "vupload",
          "part": "深圳世界之窗春节烟花",
          "duration": 55,
          "vid": "",
          "weblink": "",
          "dimension": {
            "width": 1920,
            "height": 1080,
            "rotate": 1
          },
          "first_frame": "http://i0.hdslb.com/bfs/storyff/n230207qn29v8tglefsgkv36x53mr7b2_firsti.jpg"
        }
      ],
      "subtitle": {
        "allow_submit": false,
        "list": []
      },
      "is_season_display": false,
      "user_garb": {
        "url_image_ani_cut": ""
      },
      "honor_reply": {},
      "like_icon": "",
      "need_jump_bv": false
    },
    "Card": {
      "card": {
        "mid": "1614308159",
        "name": "澎湖湾狠人",
        "approve": false,
        "sex": "保密",
        "rank": "10000",
        "face": "https://i2.hdslb.com/bfs/face/4eb307be5329cf4e7fbe944946f3f894207a5ddc.jpg",
        "face_nft": 0,
        "face_nft_type": 0,
        "DisplayRank": "0",
        "regtime": 0,
        "spacesta": 0,
        "birthday": "",
        "place": "",
        "description": "",
        "article": 0,
        "attentions": [],
        "fans": 2,
        "friend": 12,
        "attention": 12,
        "sign": "",
        "level_info": {
          "current_level": 3,
          "current_min": 0,
          "current_exp": 0,
          "next_exp": 0
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
          "nid": 0,
          "name": "",
          "image": "",
          "image_small": "",
          "level": "",
          "condition": ""
        },
        "Official": {
          "role": 0,
          "title": "",
          "desc": "",
          "type": -1
        },
        "official_verify": {
          "type": -1,
          "desc": ""
        },
        "vip": {
          "type": 0,
          "status": 0,
          "due_date": 0,
          "vip_pay_type": 0,
          "theme_type": 0,
          "label": {
            "path": "",
            "text": "",
            "label_theme": "",
            "text_color": "",
            "bg_style": 0,
            "bg_color": "",
            "border_color": "",
            "use_img_label": true,
            "img_label_uri_hans": "",
            "img_label_uri_hant": "",
            "img_label_uri_hans_static": "https://i0.hdslb.com/bfs/vip/d7b702ef65a976b20ed854cbd04cb9e27341bb79.png",
            "img_label_uri_hant_static": "https://i0.hdslb.com/bfs/activity-plat/static/20220614/e369244d0b14644f5e1a06431e22a4d5/KJunwh19T5.png"
          },
          "avatar_subscript": 0,
          "nickname_color": "",
          "role": 0,
          "avatar_subscript_url": "",
          "tv_vip_status": 0,
          "tv_vip_pay_type": 0,
          "vipType": 0,
          "vipStatus": 0
        },
        "is_senior_member": 0
      },
      "space": {
        "s_img": "http://i1.hdslb.com/bfs/space/768cc4fd97618cf589d23c2711a1d1a729f42235.png",
        "l_img": "http://i1.hdslb.com/bfs/space/cb1c3ef50e22b6096fde67febe863494caefebad.png"
      },
      "following": false,
      "archive_count": 3,
      "article_count": 0,
      "follower": 2,
      "like_num": 81
    },
    "Tags": [
      {
        "tag_id": 189847,
        "tag_name": "2023的第一场旅行",
        "cover": "",
        "head_cover": "",
        "content": "",
        "short_content": "",
        "type": 0,
        "state": 0,
        "ctime": 0,
        "count": {
          "view": 0,
          "use": 0,
          "atten": 0
        },
        "is_atten": 0,
        "likes": 0,
        "hates": 0,
        "attribute": 0,
        "liked": 0,
        "hated": 0,
        "extra_attr": 0,
        "music_id": "",
        "tag_type": "topic",
        "is_activity": false,
        "color": "",
        "alpha": 0,
        "is_season": false,
        "subscribed_count": 0,
        "archive_count": "",
        "featured_count": 0,
        "jump_url": "https://m.bilibili.com/topic-detail?topic_id=189847&topic_name=2023%E7%9A%84%E7%AC%AC%E4%B8%80%E5%9C%BA%E6%97%85%E8%A1%8C"
      },
      {
        "tag_id": 1742,
        "tag_name": "生活",
        "cover": "",
        "head_cover": "",
        "content": "",
        "short_content": "",
        "type": 3,
        "state": 0,
        "ctime": 1436866637,
        "count": {
          "view": 0,
          "use": 23558556,
          "atten": 201210
        },
        "is_atten": 0,
        "likes": 0,
        "hates": 0,
        "attribute": 0,
        "liked": 0,
        "hated": 0,
        "extra_attr": 0,
        "music_id": "",
        "tag_type": "old_channel",
        "is_activity": false,
        "color": "",
        "alpha": 0,
        "is_season": false,
        "subscribed_count": 201210,
        "archive_count": "-",
        "featured_count": 0,
        "jump_url": ""
      },
      {
        "tag_id": 33323205,
        "tag_name": "新春出行游园会",
        "cover": "",
        "head_cover": "",
        "content": "",
        "short_content": "",
        "type": 0,
        "state": 0,
        "ctime": 1673194151,
        "count": {
          "view": 0,
          "use": 117594,
          "atten": 1
        },
        "is_atten": 0,
        "likes": 0,
        "hates": 0,
        "attribute": 0,
        "liked": 0,
        "hated": 0,
        "extra_attr": 0,
        "music_id": "",
        "tag_type": "old_channel",
        "is_activity": false,
        "color": "",
        "alpha": 0,
        "is_season": false,
        "subscribed_count": 1,
        "archive_count": "-",
        "featured_count": 0,
        "jump_url": ""
      }
    ],
    "Reply": {
      "page": {
        "acount": 0,
        "count": 0,
        "num": 1,
        "size": 3
      },
      "replies": null
    },
    "Related": [
      {
        "aid": 694195827,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i0.hdslb.com/bfs/archive/9dff8337718fb46afd4cc81bac55aac07943dd5c.jpg",
        "title": "三年第一次出境，入住香港最便宜酒店，重庆大厦4平米挂壁房",
        "pubdate": 1676120737,
        "ctime": 1676120737,
        "desc": "-",
        "state": 0,
        "duration": 812,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 0,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 35847683,
          "name": "峰哥亡命天涯",
          "face": "https://i2.hdslb.com/bfs/face/ae439693d6fd79a55b1b5f935ed6474ae6fba35b.jpg"
        },
        "stat": {
          "aid": 694195827,
          "view": 2510540,
          "danmaku": 23497,
          "reply": 5224,
          "favorite": 5936,
          "coin": 9934,
          "share": 11865,
          "now_rank": 0,
          "his_rank": 96,
          "like": 51878,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1003788458,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1r24y1W7E1",
        "short_link_v2": "https://b23.tv/BV1r24y1W7E1",
        "up_from_v2": 36,
        "first_frame": "http://i2.hdslb.com/bfs/storyff/n230211adyt04tldzh4jwxyyz2xh5bhz_firsti.jpg",
        "pub_location": "中国香港",
        "bvid": "BV1r24y1W7E1",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 478797072,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i2.hdslb.com/bfs/archive/2791a70936243f6fda88db8904f1aa241bea7afc.jpg",
        "title": "2～3月要来重庆旅游：一定要去🆚千万别去2～3月要来重庆的朋友先别划走⚠️这些景点和美食千万别去❌这些景点和美食一定要去✅-",
        "pubdate": 1675502496,
        "ctime": 1675502496,
        "desc": "-",
        "state": 0,
        "duration": 22,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 2091463359,
          "name": "爱旅行的小笨喵",
          "face": "https://i0.hdslb.com/bfs/face/e9d4d8f6c2d1a2a65f3b9233d30d62e94088cdb6.jpg"
        },
        "stat": {
          "aid": 478797072,
          "view": 11224,
          "danmaku": 0,
          "reply": 55,
          "favorite": 726,
          "coin": 71,
          "share": 291,
          "now_rank": 0,
          "his_rank": 0,
          "like": 381,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 992893951,
        "dimension": {
          "width": 1080,
          "height": 1440,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1ET411d7d6",
        "short_link_v2": "https://b23.tv/BV1ET411d7d6",
        "up_from_v2": 36,
        "first_frame": "http://i0.hdslb.com/bfs/storyff/n230204qn2dbnemwoyarh42kqz3agw1q_firsti.jpg",
        "pub_location": "重庆",
        "bvid": "BV1ET411d7d6",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 436387927,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i0.hdslb.com/bfs/archive/7eca94ff5f8ccb8dbf11cb6b8e75eba07a91d1da.jpg",
        "title": "我在伊朗拍到的一切。",
        "pubdate": 1675740949,
        "ctime": 1675740949,
        "desc": "比起以往，这次的剪辑也许更为粗粝。我尽可能用最真诚的方式，去还原我看到的伊朗，然后用最迫不及待的心情，和你们分享我感受到的一切。我干预的同时，也在纪录，于是它就成为了你们最终看到的样子。当然，当然，我希望你们喜欢。",
        "state": 0,
        "duration": 639,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 0,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 547127171,
          "name": "Miya的宝藏地图",
          "face": "https://i2.hdslb.com/bfs/face/c8923c52bad9d164e35b5d268abdabc8d2f7fb29.jpg"
        },
        "stat": {
          "aid": 436387927,
          "view": 467280,
          "danmaku": 883,
          "reply": 902,
          "favorite": 17703,
          "coin": 10425,
          "share": 3195,
          "now_rank": 0,
          "his_rank": 0,
          "like": 34338,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 996919424,
        "dimension": {
          "width": 3840,
          "height": 2160,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1Lj411M7Rm",
        "short_link_v2": "https://b23.tv/BV1Lj411M7Rm",
        "first_frame": "http://i2.hdslb.com/bfs/storyff/n230207qnbmu72t04mv0e2vxvwv552jt_firsti.jpg",
        "pub_location": "法国",
        "bvid": "BV1Lj411M7Rm",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 651667306,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i0.hdslb.com/bfs/archive/526f7b90b7c9cd9721bb6de42395b63a93045ccc.jpg",
        "title": "1985年“只生一个好，政府来养老。1995年，“只生一个好，政府帮养老”。2005年，“养老不能靠政府！”2012年“延迟退休好，自己来养老”#创客行动",
        "pubdate": 1676178159,
        "ctime": 1676178159,
        "desc": "-",
        "state": 0,
        "duration": 25,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 0,
          "no_reprint": 0,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 523476602,
          "name": "快快乐乐每一天2012",
          "face": "https://i0.hdslb.com/bfs/face/member/noface.jpg"
        },
        "stat": {
          "aid": 651667306,
          "view": 5907,
          "danmaku": 2,
          "reply": 37,
          "favorite": 25,
          "coin": 55,
          "share": 11,
          "now_rank": 0,
          "his_rank": 0,
          "like": 400,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1004384559,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1ie4y1P7n2",
        "short_link_v2": "https://b23.tv/BV1ie4y1P7n2",
        "up_from_v2": 35,
        "first_frame": "http://i2.hdslb.com/bfs/storyff/n230212qn1xfqjz6rcjrey17232men19_firsti.jpg",
        "pub_location": "甘肃",
        "bvid": "BV1ie4y1P7n2",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 780365475,
        "videos": 1,
        "tid": 21,
        "tname": "日常",
        "copyright": 1,
        "pic": "http://i2.hdslb.com/bfs/archive/a0bfdaaffda4fc142eb164977fab2470f62acc56.jpg",
        "title": "FINE HOTEL|客官，您是\"蹦迪\"还是\"住店\"？-成都W酒店入住体验分享",
        "pubdate": 1677663000,
        "ctime": 1677654932,
        "desc": "#成都高新区\n#成都W酒店\n#潮堂\n#型乐中餐厅\n#组织向南\n#夜生活",
        "state": 0,
        "duration": 398,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 382297912,
          "name": "Cherry在度假",
          "face": "https://i1.hdslb.com/bfs/face/f65f6feb134742408d17951ff36f91dc86ded897.jpg"
        },
        "stat": {
          "aid": 780365475,
          "view": 670,
          "danmaku": 3,
          "reply": 10,
          "favorite": 12,
          "coin": 12,
          "share": 4,
          "now_rank": 0,
          "his_rank": 0,
          "like": 34,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "认真耍，慢慢活~客官，您是\"蹦迪\"还是\"住店\"？-成都W酒店入住体验分享",
        "cid": 1032662129,
        "dimension": {
          "width": 3840,
          "height": 2160,
          "rotate": 0
        },
        "season_id": 869244,
        "short_link": "https://b23.tv/BV1k24y1V7Jm",
        "short_link_v2": "https://b23.tv/BV1k24y1V7Jm",
        "first_frame": "http://i1.hdslb.com/bfs/storyff/n230301a22pwjzjpsix1xdltzh88uek9_firsti.jpg",
        "pub_location": "北京",
        "bvid": "BV1k24y1V7Jm",
        "season_type": 1,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 224572990,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i1.hdslb.com/bfs/archive/3c2cf4957b6f2f7e54a51b0720b0d4ea3e335646.jpg",
        "title": "受邀参观中国海军导弹驱逐舰“南宁号”",
        "pubdate": 1676706334,
        "ctime": 1676706334,
        "desc": "-",
        "state": 0,
        "duration": 189,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 38363039,
          "name": "dong-hao",
          "face": "https://i2.hdslb.com/bfs/face/b62dcb6f0b546dac7863d709ecd8c1017a8c9d20.jpg"
        },
        "stat": {
          "aid": 224572990,
          "view": 222609,
          "danmaku": 743,
          "reply": 719,
          "favorite": 794,
          "coin": 576,
          "share": 326,
          "now_rank": 0,
          "his_rank": 0,
          "like": 8150,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1013737070,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1Ab411d7qe",
        "short_link_v2": "https://b23.tv/BV1Ab411d7qe",
        "up_from_v2": 8,
        "first_frame": "http://i1.hdslb.com/bfs/storyff/n230218ad699xoacz3mpw1c94ly542nx_firsti.jpg",
        "pub_location": "阿联酋",
        "bvid": "BV1Ab411d7qe",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 779170123,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i0.hdslb.com/bfs/archive/2bd6d66f2a65d4f7401b2d517fc521fb404b5e1d.jpg",
        "title": "【中国高铁】真的强！！中国如何仅用20年建成超4万公里的高铁网？",
        "pubdate": 1676030400,
        "ctime": 1676011936,
        "desc": "2003年中国首条高速铁路秦沈客运专线开通运营，开启了属于中国的高铁时代。我们有幸见证了中国高铁经历的从少到多、从引进到创新、从追赶到领跑、从走得了变成走得好的转变，在中华大地上勾画了新时期“八纵八横”高速铁路网的宏大蓝图。",
        "state": 0,
        "duration": 1501,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 0,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 448378306,
          "name": "简办动态演示",
          "face": "https://i1.hdslb.com/bfs/face/031312e67370bccbdba2de2cce9e471160cf30f7.jpg"
        },
        "stat": {
          "aid": 779170123,
          "view": 557194,
          "danmaku": 8398,
          "reply": 2392,
          "favorite": 15049,
          "coin": 24049,
          "share": 3873,
          "now_rank": 0,
          "his_rank": 0,
          "like": 32104,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "制作时间巨巨巨长的中国高铁发展史来啦~",
        "cid": 1001533232,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "season_id": 530402,
        "short_link": "https://b23.tv/BV1714y1c7Mn",
        "short_link_v2": "https://b23.tv/BV1714y1c7Mn",
        "first_frame": "http://i1.hdslb.com/bfs/storyff/n230210qn2of4qcvgrytiixg3sslwd9v_firsti.jpg",
        "pub_location": "广东",
        "bvid": "BV1714y1c7Mn",
        "season_type": 1,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 481627061,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i2.hdslb.com/bfs/archive/e94dc5c74365edfaf15471bdb14f249103a516f9.jpg",
        "title": "福建人的钱，都是大风刮来的吗？参加游神一晚上看的烟花，比我前半生看的都多",
        "pubdate": 1676173408,
        "ctime": 1676173408,
        "desc": "有个朋友，在上期视频评论说，他们村今年游神，请魁星花了四十万。我的妈呀！四十万，都够我买房的首付了。\n我惊讶，不是说我不相信，是我好奇这请神的四十万，是怎么来的。我坐在180平的房子里思考着，忽然，我又想到，福建的每个村子，每年组织游神的钱是怎么来的？\n \n刚好正月十九晚上，附近又有一场游神活动，我决定去一探究竟。",
        "state": 0,
        "duration": 633,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 383264834,
          "name": "北漂阿飞",
          "face": "http://i2.hdslb.com/bfs/face/951f6b9d19f4d55647886e07c4eb814bafad3cca.jpg"
        },
        "stat": {
          "aid": 481627061,
          "view": 133950,
          "danmaku": 818,
          "reply": 1025,
          "favorite": 1047,
          "coin": 1035,
          "share": 422,
          "now_rank": 0,
          "his_rank": 0,
          "like": 4808,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1004255410,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV13T411Q78j",
        "short_link_v2": "https://b23.tv/BV13T411Q78j",
        "first_frame": "http://i0.hdslb.com/bfs/storyff/n230212a23b6vflf1cgritccl337mn1r_firsti.jpg",
        "pub_location": "福建",
        "bvid": "BV13T411Q78j",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 395348654,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i2.hdslb.com/bfs/archive/bd3592bcbba15514e45afe586b218ecfc4783618.jpg",
        "title": "国内最美的四趟列车",
        "pubdate": 1677628644,
        "ctime": 1677628645,
        "desc": "国内最美的四趟列车",
        "state": 0,
        "duration": 63,
        "mission_id": 1333042,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 2026019569,
          "name": "修行让心归于平静",
          "face": "https://i1.hdslb.com/bfs/face/2eff41ccfbc742f9baf730acbe22cb8fae1cdb34.jpg"
        },
        "stat": {
          "aid": 395348654,
          "view": 1301,
          "danmaku": 0,
          "reply": 0,
          "favorite": 32,
          "coin": 2,
          "share": 2,
          "now_rank": 0,
          "his_rank": 0,
          "like": 22,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "国内最美的四趟列车",
        "cid": 1032378037,
        "dimension": {
          "width": 1080,
          "height": 1920,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1Go4y1r7AT",
        "short_link_v2": "https://b23.tv/BV1Go4y1r7AT",
        "up_from_v2": 19,
        "first_frame": "http://i2.hdslb.com/bfs/storyff/n230301qn3eil6czq5wd0fhr2an74bfo_firsti.jpg",
        "pub_location": "河北",
        "bvid": "BV1Go4y1r7AT",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 566970534,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i1.hdslb.com/bfs/archive/ad9f7cfea38ca3b3ab2878199c6965124c423420.jpg",
        "title": "漫步广州城中村，街头看到的一幕",
        "pubdate": 1676561473,
        "ctime": 1676561473,
        "desc": "漫步广州城中村，街头看到的一幕",
        "state": 0,
        "duration": 160,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 0,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 3493121249774318,
          "name": "校园加油站",
          "face": "https://i2.hdslb.com/bfs/face/116cf5ffbf210a3fa0e1b8e39742bb0616f75462.jpg"
        },
        "stat": {
          "aid": 566970534,
          "view": 196372,
          "danmaku": 577,
          "reply": 997,
          "favorite": 1035,
          "coin": 59,
          "share": 1267,
          "now_rank": 0,
          "his_rank": 0,
          "like": 7109,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "漫步广州城中村，街头看到的一幕",
        "cid": 1011164086,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "season_id": 1050845,
        "short_link": "https://b23.tv/BV1ev4y1x7sc",
        "short_link_v2": "https://b23.tv/BV1ev4y1x7sc",
        "first_frame": "http://i1.hdslb.com/bfs/storyff/n230216a2vx9044h63f722ug0793ks5s_firsti.jpg",
        "pub_location": "广东",
        "bvid": "BV1ev4y1x7sc",
        "season_type": 1,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 907870611,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i1.hdslb.com/bfs/archive/9ccc63861c47d7c3d20097f0ac67d979b5546155.jpg",
        "title": "尽量别排在女生后面",
        "pubdate": 1677668051,
        "ctime": 1677668051,
        "desc": "我滴孩，别人下山滑了四分钟我滑了八分钟，视频还是加速过的，也不是针对她们，建议想体验速度的朋友可以稍微等一等。（还是怕女拳，原视频抱怨了几句）",
        "state": 0,
        "duration": 238,
        "mission_id": 1333042,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 63853555,
          "name": "李蚊香i",
          "face": "https://i1.hdslb.com/bfs/face/c4355de29387b0eb4fc3d75daa6b4d4f0a2a0fa8.jpg"
        },
        "stat": {
          "aid": 907870611,
          "view": 1756,
          "danmaku": 1,
          "reply": 1,
          "favorite": 1,
          "coin": 0,
          "share": 0,
          "now_rank": 0,
          "his_rank": 0,
          "like": 29,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1033358135,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1yM4y1R7ug",
        "short_link_v2": "https://b23.tv/BV1yM4y1R7ug",
        "up_from_v2": 8,
        "first_frame": "http://i2.hdslb.com/bfs/storyff/n230301ws1i9wqm69l599w3rk3cpnx9m_firsti.jpg",
        "pub_location": "安徽",
        "bvid": "BV1yM4y1R7ug",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 479173383,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i0.hdslb.com/bfs/archive/d51c9188b09a0014c1e65fb58c668ddfc1a8576d.jpg",
        "title": "住深圳最贵的酒店是什么体验？一晚上8000元",
        "pubdate": 1676115600,
        "ctime": 1676109223,
        "desc": "",
        "state": 0,
        "duration": 964,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 0,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 4249401,
          "name": "20岁了还没去过星巴克",
          "face": "https://i0.hdslb.com/bfs/face/96bf3f019f882fdf5290350bb902676bf61727dc.jpg"
        },
        "stat": {
          "aid": 479173383,
          "view": 616848,
          "danmaku": 4572,
          "reply": 1841,
          "favorite": 2304,
          "coin": 6304,
          "share": 4648,
          "now_rank": 0,
          "his_rank": 0,
          "like": 18519,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1003247124,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1yT411R7EP",
        "short_link_v2": "https://b23.tv/BV1yT411R7EP",
        "first_frame": "http://i0.hdslb.com/bfs/storyff/n230211a22gpchz4oja9ft2x54m7zy5u_firsti.jpg",
        "pub_location": "江苏",
        "bvid": "BV1yT411R7EP",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 609615181,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i2.hdslb.com/bfs/archive/a10b967df152c4ec64a0ca91a5024a887f1c8ba3.jpg",
        "title": "当藏族姑娘来到重庆......",
        "pubdate": 1676691128,
        "ctime": 1676691128,
        "desc": "和姐姐来重庆，差点因为苕皮打起来，真的太好吃了！",
        "state": 0,
        "duration": 22,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 1085299926,
          "name": "那曲拉姆",
          "face": "https://i0.hdslb.com/bfs/face/002dc3ccb7e9a75a5063fbc498bb09840c39e0d6.jpg"
        },
        "stat": {
          "aid": 609615181,
          "view": 257497,
          "danmaku": 87,
          "reply": 324,
          "favorite": 1573,
          "coin": 704,
          "share": 306,
          "now_rank": 0,
          "his_rank": 0,
          "like": 27963,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1013377613,
        "dimension": {
          "width": 1080,
          "height": 1920,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1X84y1n71v",
        "short_link_v2": "https://b23.tv/BV1X84y1n71v",
        "up_from_v2": 35,
        "first_frame": "http://i1.hdslb.com/bfs/storyff/n230218qn1l0unbnwgwx8h1gk3h56rp5_firsti.jpg",
        "pub_location": "重庆",
        "bvid": "BV1X84y1n71v",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 609375088,
        "videos": 1,
        "tid": 176,
        "tname": "汽车生活",
        "copyright": 1,
        "pic": "http://i2.hdslb.com/bfs/archive/c00630c8cb5984daa0255c348fc577d243fe6f11.jpg",
        "title": "广普大比拼！笑到你lo地！～",
        "pubdate": 1676504665,
        "ctime": 1676504665,
        "desc": "-",
        "state": 0,
        "duration": 69,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 0,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 1742441029,
          "name": "DJ初仔小朋友",
          "face": "https://i1.hdslb.com/bfs/face/ea530a95334cbd8eddcbc70b992bd75b9d7690fe.jpg"
        },
        "stat": {
          "aid": 609375088,
          "view": 592164,
          "danmaku": 250,
          "reply": 281,
          "favorite": 1982,
          "coin": 368,
          "share": 2034,
          "now_rank": 0,
          "his_rank": 0,
          "like": 29223,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1009930517,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1p84y1p7P3",
        "short_link_v2": "https://b23.tv/BV1p84y1p7P3",
        "up_from_v2": 19,
        "first_frame": "http://i2.hdslb.com/bfs/storyff/n230216a2ktf0s1k92f7a50cr5xqlup3_firsti.jpg",
        "pub_location": "未知",
        "bvid": "BV1p84y1p7P3",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 266878980,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i1.hdslb.com/bfs/archive/7aae8e8e16ee4d252a7c084e0cdfe881bc266a9f.jpg",
        "title": "女朋友喜欢跟我骑单车去西藏，现已抵达四川乐山，晚上在桥洞过夜",
        "pubdate": 1676541633,
        "ctime": 1676530784,
        "desc": "女朋友喜欢跟我骑单车去西藏，现已抵达四川乐山，晚上在桥洞过夜",
        "state": 0,
        "duration": 1468,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 1644752276,
          "name": "周和婷的旅行",
          "face": "https://i2.hdslb.com/bfs/face/a2c58c54cace57fa1f233c15187316d4553cda62.jpg"
        },
        "stat": {
          "aid": 266878980,
          "view": 64201,
          "danmaku": 745,
          "reply": 217,
          "favorite": 196,
          "coin": 1260,
          "share": 117,
          "now_rank": 0,
          "his_rank": 0,
          "like": 2364,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1010397511,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "season_id": 1007955,
        "short_link": "https://b23.tv/BV1nY411e79a",
        "short_link_v2": "https://b23.tv/BV1nY411e79a",
        "up_from_v2": 35,
        "first_frame": "http://i0.hdslb.com/bfs/storyff/n230216ws2892dbzft0xhe3o3kwcg7tl_firsti.jpg",
        "pub_location": "四川",
        "bvid": "BV1nY411e79a",
        "season_type": 1,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 863666376,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i1.hdslb.com/bfs/archive/a2e52b1bb127f1904990103a88955da68e570ee0.jpg",
        "title": "【中式怪核】老城区",
        "pubdate": 1675250842,
        "ctime": 1675250843,
        "desc": "-",
        "state": 0,
        "duration": 38,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 0,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 1675566881,
          "name": "季江市民",
          "face": "https://i2.hdslb.com/bfs/face/a85f945ddc9c68f3f5d317f1a61cd6b3be933654.jpg"
        },
        "stat": {
          "aid": 863666376,
          "view": 32836,
          "danmaku": 18,
          "reply": 89,
          "favorite": 801,
          "coin": 70,
          "share": 43,
          "now_rank": 0,
          "his_rank": 0,
          "like": 1491,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 988598018,
        "dimension": {
          "width": 1080,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV17G4y1D7ST",
        "short_link_v2": "https://b23.tv/BV17G4y1D7ST",
        "up_from_v2": 19,
        "first_frame": "http://i0.hdslb.com/bfs/storyff/n230201a22w9fmarud4q223lbqd5aq34_firsti.jpg",
        "pub_location": "江苏",
        "bvid": "BV17G4y1D7ST",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 567509427,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i2.hdslb.com/bfs/archive/09c5d2bbeade1291ae0e0eb5c508003eea431dbc.jpg",
        "title": "以后就是农村二人行了，两小伙决定完成以前的计划，出发巴基斯坦",
        "pubdate": 1677402000,
        "ctime": 1677390686,
        "desc": "以后就是农村二人行了，两小伙决定完成以前的计划，出发巴基斯坦",
        "state": 0,
        "duration": 186,
        "mission_id": 1333042,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 0,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 1101057244,
          "name": "农村三人行",
          "face": "https://i1.hdslb.com/bfs/face/21aeba16e31e0659bd651475254bb6aaa91cc10e.jpg"
        },
        "stat": {
          "aid": 567509427,
          "view": 440393,
          "danmaku": 563,
          "reply": 529,
          "favorite": 1127,
          "coin": 460,
          "share": 254,
          "now_rank": 0,
          "his_rank": 0,
          "like": 5703,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1027076667,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV19v4y1e7Lg",
        "short_link_v2": "https://b23.tv/BV19v4y1e7Lg",
        "first_frame": "http://i0.hdslb.com/bfs/storyff/n230226qn2giu9p4k94yhvnr5sbapbqy_firsti.jpg",
        "pub_location": "河南",
        "bvid": "BV19v4y1e7Lg",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 907839722,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i0.hdslb.com/bfs/archive/ce7012b4a5486c31dfe4ac8a94c90bb47b9861fa.jpg",
        "title": "久违的闲暇时光｜福州随拍小记",
        "pubdate": 1677689946,
        "ctime": 1677689946,
        "desc": "因工作，第一次来到福州，工作之余扫街随拍。\n设备：FX3+腾龙28-75二代",
        "state": 0,
        "duration": 63,
        "mission_id": 1333042,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 0,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 401754460,
          "name": "弗弗的Young",
          "face": "https://i1.hdslb.com/bfs/face/a06643e48c42890b1941d0b2e26795688cc5eb86.jpg"
        },
        "stat": {
          "aid": 907839722,
          "view": 1084,
          "danmaku": 1,
          "reply": 17,
          "favorite": 9,
          "coin": 18,
          "share": 3,
          "now_rank": 0,
          "his_rank": 0,
          "like": 48,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1033900869,
        "dimension": {
          "width": 2880,
          "height": 2160,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1YM4y1R7CN",
        "short_link_v2": "https://b23.tv/BV1YM4y1R7CN",
        "first_frame": "http://i0.hdslb.com/bfs/storyff/n230302a22uld2u0vh150s2i7w7q6eqa_firsti.jpg",
        "pub_location": "湖北",
        "bvid": "BV1YM4y1R7CN",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 652721584,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i0.hdslb.com/bfs/archive/e5fbfdf213a043b3fe5051fabf306de71cf5561e.jpg",
        "title": "广东韶关竟然有一颗 天下第一奇石，阳元石，据说他已经存在30万年的历史，就坐落在世界地质公园内！#大自然的鬼斧神工 #天下奇石 #自然奇观 #雄伟壮观 #丹霞山",
        "pubdate": 1677547415,
        "ctime": 1677547415,
        "desc": "-",
        "state": 0,
        "duration": 35,
        "mission_id": 1333042,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 0,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 1861332991,
          "name": "威利哥去旅行",
          "face": "https://i1.hdslb.com/bfs/face/aea0332ba8eb23ae7b8a17f6854407e22b57c89d.jpg"
        },
        "stat": {
          "aid": 652721584,
          "view": 311307,
          "danmaku": 713,
          "reply": 907,
          "favorite": 2627,
          "coin": 200,
          "share": 4428,
          "now_rank": 0,
          "his_rank": 0,
          "like": 13990,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1030515938,
        "dimension": {
          "width": 1080,
          "height": 1920,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1bY4y1m76H",
        "short_link_v2": "https://b23.tv/BV1bY4y1m76H",
        "up_from_v2": 36,
        "first_frame": "http://i0.hdslb.com/bfs/storyff/n230228qn2p96cswxqazjw93y0jibi49_firsti.jpg",
        "pub_location": "广东",
        "bvid": "BV1bY4y1m76H",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 693701089,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i1.hdslb.com/bfs/archive/ae093c1da6ea6ed3aba2dc1afb8d773b509d889a.jpg",
        "title": "你会如何形容这个场景呢",
        "pubdate": 1675340181,
        "ctime": 1675340181,
        "desc": "你会如何形容这个场景呢？（是觉得带着一点淡淡的忧伤，可能是因为我拍的时候情绪也比较低落吧，但看见这个列车，我知道末班车的列车可能永远也不会相遇了）",
        "state": 0,
        "duration": 16,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 0,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 353755731,
          "name": "摄影师云晓",
          "face": "https://i0.hdslb.com/bfs/face/1329d8295083d25ea741675892002fa3232429b4.jpg"
        },
        "stat": {
          "aid": 693701089,
          "view": 594151,
          "danmaku": 611,
          "reply": 1469,
          "favorite": 17059,
          "coin": 2753,
          "share": 2343,
          "now_rank": 0,
          "his_rank": 0,
          "like": 48793,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 990142657,
        "dimension": {
          "width": 3840,
          "height": 2160,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1L24y1B7rp",
        "short_link_v2": "https://b23.tv/BV1L24y1B7rp",
        "up_from_v2": 35,
        "first_frame": "http://i1.hdslb.com/bfs/storyff/n230202qn3mibfg852tb1h3h8xerwcrn_firsti.jpg",
        "pub_location": "重庆",
        "bvid": "BV1L24y1B7rp",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 822700803,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i0.hdslb.com/bfs/archive/1d55ab7df7b82f01afa47150a9fc2bc21a101c51.jpg",
        "title": "探索涉黑被查封的夜总会，发现公主休息室有大量高跟鞋和“校服”",
        "pubdate": 1677594661,
        "ctime": 1677589504,
        "desc": "第一次去夜总会很紧张",
        "state": 0,
        "duration": 216,
        "mission_id": 1333042,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 1971931622,
          "name": "伊苼青",
          "face": "https://i2.hdslb.com/bfs/face/9f2bbfa2fadc2b1d70a261042dee18e2b0a06e94.jpg"
        },
        "stat": {
          "aid": 822700803,
          "view": 7513,
          "danmaku": 5,
          "reply": 34,
          "favorite": 46,
          "coin": 0,
          "share": 5,
          "now_rank": 0,
          "his_rank": 0,
          "like": 63,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1031722294,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1Bg4y1J7UK",
        "short_link_v2": "https://b23.tv/BV1Bg4y1J7UK",
        "up_from_v2": 11,
        "first_frame": "http://i2.hdslb.com/bfs/storyff/n230228a22s4f0la2dj7u0pti5zcqb1o_firsti.jpg",
        "pub_location": "广东",
        "bvid": "BV1Bg4y1J7UK",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 779260866,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i2.hdslb.com/bfs/archive/ae5a5396421ae2197b177060af59a85801512c93.jpg",
        "title": "重庆是5A景区最多的城市，来看看你去过几个？",
        "pubdate": 1676380854,
        "ctime": 1676380854,
        "desc": "-",
        "state": 0,
        "duration": 202,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 0,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 3493135697054136,
          "name": "重庆旅游自驾全国",
          "face": "https://i0.hdslb.com/bfs/face/8d2c37d585f9d3fb4728e713ce8d7eaeb24158cd.jpg"
        },
        "stat": {
          "aid": 779260866,
          "view": 6033,
          "danmaku": 33,
          "reply": 54,
          "favorite": 122,
          "coin": 4,
          "share": 49,
          "now_rank": 0,
          "his_rank": 0,
          "like": 105,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1006967071,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1114y1c7w2",
        "short_link_v2": "https://b23.tv/BV1114y1c7w2",
        "up_from_v2": 9,
        "first_frame": "http://i2.hdslb.com/bfs/storyff/n230214a21y4iww8ufzfuw270nddcxy3_firsti.jpg",
        "pub_location": "重庆",
        "bvid": "BV1114y1c7w2",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 822155013,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i1.hdslb.com/bfs/archive/8854398215c9c002d6687fece44c8edea660e984.jpg",
        "title": "VLOG103. 在揭阳一边感受民俗一边说些可笑话！",
        "pubdate": 1676811484,
        "ctime": 1676811484,
        "desc": "",
        "state": 0,
        "duration": 370,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 0,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 91236407,
          "name": "jyhachi",
          "face": "http://i2.hdslb.com/bfs/face/e73fe153bd177c13ab357bdd4f3ccd60d2e8ec04.jpg"
        },
        "stat": {
          "aid": 822155013,
          "view": 105386,
          "danmaku": 1434,
          "reply": 437,
          "favorite": 1757,
          "coin": 5660,
          "share": 1734,
          "now_rank": 0,
          "his_rank": 0,
          "like": 9132,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1015791774,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1Wg4y1p7qg",
        "short_link_v2": "https://b23.tv/BV1Wg4y1p7qg",
        "first_frame": "http://i0.hdslb.com/bfs/storyff/n230219qn1e45grwa1ggdwaehegz3lrm_firsti.jpg",
        "pub_location": "北京",
        "bvid": "BV1Wg4y1p7qg",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 309193148,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i0.hdslb.com/bfs/archive/d0e74e3b186974462830bc9e1ca23acf8ed87c29.jpg",
        "title": "骑行北京长安街，中南海新华门前黑衣人守卫森严，让人肃然起敬！",
        "pubdate": 1676186978,
        "ctime": 1676186978,
        "desc": "",
        "state": 0,
        "duration": 251,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 690701873,
          "name": "北京旅游等着瞧",
          "face": "https://i2.hdslb.com/bfs/face/cb7867b89be883731ae25b5731bc753ebd6da5ba.jpg"
        },
        "stat": {
          "aid": 309193148,
          "view": 477194,
          "danmaku": 236,
          "reply": 945,
          "favorite": 968,
          "coin": 158,
          "share": 435,
          "now_rank": 0,
          "his_rank": 0,
          "like": 5770,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1004564441,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1mA411B7PL",
        "short_link_v2": "https://b23.tv/BV1mA411B7PL",
        "first_frame": "http://i2.hdslb.com/bfs/storyff/n230212a221o8tphdnbnhz3ro0tyqsgn_firsti.jpg",
        "pub_location": "北京",
        "bvid": "BV1mA411B7PL",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 822046802,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i2.hdslb.com/bfs/archive/f7c53a9bafd61cb5e8e5378144775e0b40ee6d97.jpg",
        "title": "花最少的钱看最美的景！值得收藏的五个穷游宝藏城市！",
        "pubdate": 1676726435,
        "ctime": 1676726435,
        "desc": "-",
        "state": 0,
        "duration": 83,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 0,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 510880741,
          "name": "罗飞飞带您云旅游",
          "face": "https://i1.hdslb.com/bfs/face/5253786b12ec7178f5a251921cc869dcf1b9817b.jpg"
        },
        "stat": {
          "aid": 822046802,
          "view": 41502,
          "danmaku": 91,
          "reply": 116,
          "favorite": 1677,
          "coin": 98,
          "share": 182,
          "now_rank": 0,
          "his_rank": 0,
          "like": 2538,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1014236030,
        "dimension": {
          "width": 1080,
          "height": 1920,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1KG4y1N7Ui",
        "short_link_v2": "https://b23.tv/BV1KG4y1N7Ui",
        "up_from_v2": 36,
        "first_frame": "http://i1.hdslb.com/bfs/storyff/n230218qncbqoxmb2jkwjwc5ij13urv1_firsti.jpg",
        "pub_location": "四川",
        "bvid": "BV1KG4y1N7Ui",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 310284536,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i1.hdslb.com/bfs/archive/48b95d9da6d39c1587d4e50033764ca064b5993c.jpg",
        "title": "广州旅游vlog｜各种小插曲的一天｜孔雀开屏｜完美融入广场舞",
        "pubdate": 1677683666,
        "ctime": 1677683666,
        "desc": "-",
        "state": 0,
        "duration": 601,
        "mission_id": 1333042,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 79400733,
          "name": "萌饭饭m",
          "face": "https://i0.hdslb.com/bfs/face/a5c8ca4d963bbaa6801124012e793fccf9494480.jpg"
        },
        "stat": {
          "aid": 310284536,
          "view": 740,
          "danmaku": 2,
          "reply": 11,
          "favorite": 9,
          "coin": 25,
          "share": 2,
          "now_rank": 0,
          "his_rank": 0,
          "like": 39,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "之前咕咕咕了好久，有很大一部分原因是觉得没什么好东西分享，大家不爱看，怕发出来数据太差\n\n现在的我：不管啦！都是我的美好生活！一秒都不剪！发疯中…",
        "cid": 1033760887,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1eA411y7s6",
        "short_link_v2": "https://b23.tv/BV1eA411y7s6",
        "up_from_v2": 9,
        "first_frame": "http://i2.hdslb.com/bfs/storyff/n230301a22qu86me0iswkf1qzn6453b7_firsti.jpg",
        "pub_location": "广东",
        "bvid": "BV1eA411y7s6",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 694438333,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i1.hdslb.com/bfs/archive/5e927a1e66e07d7c61ff884bf11ef1f15e17d8fb.jpg",
        "title": "我买了全世界最经典的步枪！是什么体验？销量全球第一！",
        "pubdate": 1676624700,
        "ctime": 1676531705,
        "desc": "点赞过10W！我就带你们玩黄金AK47！这期视频成本花了950美金！求求各位！三连！三连！三连！回回血！",
        "state": 0,
        "duration": 478,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 0,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 6336952,
          "name": "老李船长",
          "face": "https://i1.hdslb.com/bfs/face/ded6f91c6937d0935412e362a1157264760ad3b4.jpg"
        },
        "stat": {
          "aid": 694438333,
          "view": 2308302,
          "danmaku": 5420,
          "reply": 2490,
          "favorite": 14806,
          "coin": 34621,
          "share": 4190,
          "now_rank": 0,
          "his_rank": 0,
          "like": 242162,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "我买了全世界最经典的步枪！是什么体验？",
        "cid": 1010337167,
        "dimension": {
          "width": 3840,
          "height": 2160,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1P24y1p7u1",
        "short_link_v2": "https://b23.tv/BV1P24y1p7u1",
        "first_frame": "http://i2.hdslb.com/bfs/storyff/n230216qn13174ejqtfr6r1fj9o3q7ac_firsti.jpg",
        "pub_location": "美国",
        "bvid": "BV1P24y1p7u1",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 524470294,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i1.hdslb.com/bfs/archive/71fbade14220d7e2c8a1787d24d2df067e9ba594.jpg",
        "title": "本人很喜欢的厦门旅游路线",
        "pubdate": 1676391080,
        "ctime": 1676391080,
        "desc": "-",
        "state": 0,
        "duration": 171,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 174040793,
          "name": "是红贝贝",
          "face": "https://i2.hdslb.com/bfs/face/f08244c2e2ead77816cf976d91cba0a54f6c29eb.jpg"
        },
        "stat": {
          "aid": 524470294,
          "view": 163076,
          "danmaku": 66,
          "reply": 195,
          "favorite": 9352,
          "coin": 804,
          "share": 2269,
          "now_rank": 0,
          "his_rank": 0,
          "like": 10271,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1008185929,
        "dimension": {
          "width": 1080,
          "height": 1920,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1SM411n7K7",
        "short_link_v2": "https://b23.tv/BV1SM411n7K7",
        "up_from_v2": 36,
        "first_frame": "http://i1.hdslb.com/bfs/storyff/n230215a213kb1bld1pd1839tdez1vfg_firsti.jpg",
        "pub_location": "福建",
        "bvid": "BV1SM411n7K7",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 907702077,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i1.hdslb.com/bfs/archive/e0ac0a422d4e415daee04445c276194b6219766c.jpg",
        "title": "旅居深圳是什么体验？来了都是深圳人？——深圳受难记01",
        "pubdate": 1677581992,
        "ctime": 1677581992,
        "desc": "补充一下老家的寒冷：由于没有地暖、中央供暖，空调制暖是坏的，修不好，层高3.3m，最低温度-8度的情况下每天必须保持泡脚才可以保证不生病；日常头晕；伴随左肩胛骨附近酸痛和胸肌下束远端肌腱刺痛；都是在到深圳之后一天全都好了",
        "state": 0,
        "duration": 149,
        "mission_id": 1333042,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 16419172,
          "name": "灵魂健身杨老师",
          "face": "https://i1.hdslb.com/bfs/face/2b153f572bf55a4786b4f8e7395c55f8c3547eab.jpg"
        },
        "stat": {
          "aid": 907702077,
          "view": 40547,
          "danmaku": 114,
          "reply": 342,
          "favorite": 244,
          "coin": 309,
          "share": 109,
          "now_rank": 0,
          "his_rank": 0,
          "like": 3753,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1031442015,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1HM4y1o7sg",
        "short_link_v2": "https://b23.tv/BV1HM4y1o7sg",
        "first_frame": "http://i2.hdslb.com/bfs/storyff/n230228qn3eyf7xpot2gp515c7s3xm8u_firsti.jpg",
        "pub_location": "广东",
        "bvid": "BV1HM4y1o7sg",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 479243204,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i0.hdslb.com/bfs/archive/eae4ecf2664639975e70b1e2c55e0d46102c79fb.jpg",
        "title": "关于我从杭州划船去北京第一天就被抓了的道歉视频（下）",
        "pubdate": 1676111846,
        "ctime": 1676111846,
        "desc": "",
        "state": 0,
        "duration": 405,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 431768394,
          "name": "沙雕队长大明",
          "face": "https://i0.hdslb.com/bfs/face/1e5cc88beb16d0d912a1731a56cfb91338796d75.jpg"
        },
        "stat": {
          "aid": 479243204,
          "view": 1005385,
          "danmaku": 2913,
          "reply": 2144,
          "favorite": 1703,
          "coin": 2035,
          "share": 3215,
          "now_rank": 0,
          "his_rank": 0,
          "like": 30565,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1003344032,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1uM411P78k",
        "short_link_v2": "https://b23.tv/BV1uM411P78k",
        "first_frame": "http://i1.hdslb.com/bfs/storyff/n230211qn1uadyj7ooez2a2iw9tap3r4_firsti.jpg",
        "pub_location": "浙江",
        "bvid": "BV1uM411P78k",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 780186082,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i2.hdslb.com/bfs/archive/3059dee42a937bbd46d0fe925ea7d3a4e056c3cd.jpg",
        "title": "那些说5个，7个的，都是瞎扯",
        "pubdate": 1677495799,
        "ctime": 1677495800,
        "desc": "是的，是真的",
        "state": 0,
        "duration": 494,
        "mission_id": 1333042,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 0,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 570095551,
          "name": "开元心旅行",
          "face": "https://i1.hdslb.com/bfs/face/109ef5f8ac9ed07e7090b62367ead1c52aa3bef1.jpg"
        },
        "stat": {
          "aid": 780186082,
          "view": 27788,
          "danmaku": 81,
          "reply": 223,
          "favorite": 180,
          "coin": 197,
          "share": 59,
          "now_rank": 0,
          "his_rank": 0,
          "like": 972,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1029450855,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1f24y1G7aa",
        "short_link_v2": "https://b23.tv/BV1f24y1G7aa",
        "up_from_v2": 19,
        "first_frame": "http://i2.hdslb.com/bfs/storyff/n230227qn3et74epl0akfe35k3fur58i_firsti.jpg",
        "pub_location": "江苏",
        "bvid": "BV1f24y1G7aa",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 395339458,
        "videos": 2,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i1.hdslb.com/bfs/archive/82ffd588297655a9ae48bb840b68d75c4abc9959.jpg",
        "title": "【4K HDR】顶级穿越机画质 御剑遨游老君山",
        "pubdate": 1677688022,
        "ctime": 1677688022,
        "desc": "请打开HDR模式进行观看，终端不支持HDR播放的小伙伴请选择分集里面的SDR版本，以获得最好的视觉体验。\r\n        这次创作使用FPV+航拍的形式来展现老君山风景，其中穿越机是X8搭载电影机拍摄。得益于电影机的画质，制作了首个HDR版本的穿越机视频。通过这部作品，希望能向大家展示老君山的壮美景色，感受到高质量FPV画质带来的震撼体验，一起来御剑遨游老君山吧~",
        "state": 0,
        "duration": 220,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 0,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 362481165,
          "name": "LiangFPV",
          "face": "https://i0.hdslb.com/bfs/face/fd54c3714274d51008626477461032728bc4731a.jpg"
        },
        "stat": {
          "aid": 395339458,
          "view": 680,
          "danmaku": 0,
          "reply": 4,
          "favorite": 19,
          "coin": 18,
          "share": 8,
          "now_rank": 0,
          "his_rank": 0,
          "like": 42,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1033807908,
        "dimension": {
          "width": 3840,
          "height": 2160,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1Fo4y1r7Mf",
        "short_link_v2": "https://b23.tv/BV1Fo4y1r7Mf",
        "up_from_v2": 2,
        "first_frame": "http://i0.hdslb.com/bfs/storyff/n23030106172ptpa78nas11x0eq92h8h_firsti.jpg",
        "pub_location": "上海",
        "bvid": "BV1Fo4y1r7Mf",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 906745828,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i2.hdslb.com/bfs/archive/f4ec2e689f3529c5a0593a84d6bbd9c5d4486e9c.jpg",
        "title": "自从全面通关后，兰桂坊也变成了夜猫子游客们的网红打卡地，许多潮男靓女汇聚集与此，如果你来香港旅游想来喝上一杯吗？##香港与内地全面恢复通关 #香港兰桂坊 #香港",
        "pubdate": 1676129190,
        "ctime": 1676129190,
        "desc": "自从全面通关后，兰桂坊也变成了夜猫子游客们的网红打卡地，许多潮男靓女汇聚集与此，如果你来香港旅游想来喝上一杯吗？##香港与内地全面恢复通关 #香港兰桂坊 #香港兰桂坊街头",
        "state": 0,
        "duration": 12,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 1740831353,
          "name": "东北大鹅在香港",
          "face": "https://i2.hdslb.com/bfs/face/44a7ba7d1a28e365d8faa06a2ed751070c95a0b9.jpg"
        },
        "stat": {
          "aid": 906745828,
          "view": 736386,
          "danmaku": 58,
          "reply": 408,
          "favorite": 1239,
          "coin": 72,
          "share": 347,
          "now_rank": 0,
          "his_rank": 0,
          "like": 7334,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1003753045,
        "dimension": {
          "width": 2160,
          "height": 3840,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1bM4y1Q7Lf",
        "short_link_v2": "https://b23.tv/BV1bM4y1Q7Lf",
        "first_frame": "http://i2.hdslb.com/bfs/storyff/n230211qnl2wz9eoqloea18yggdwgi0d_firsti.jpg",
        "pub_location": "广东",
        "bvid": "BV1bM4y1Q7Lf",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 267749663,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i0.hdslb.com/bfs/archive/5ab8f7a6cf262925f39c062d9170f50323a20920.jpg",
        "title": "现实中的赛博世界？看北京CBD亮灯",
        "pubdate": 1677480841,
        "ctime": 1677480841,
        "desc": "一段小小的延时摄影",
        "state": 0,
        "duration": 19,
        "mission_id": 1333042,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 0,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 12915021,
          "name": "面包猫会拍照",
          "face": "https://i0.hdslb.com/bfs/face/f1121c1ac45660d6e76631cd1117d70a3cb97951.jpg"
        },
        "stat": {
          "aid": 267749663,
          "view": 6921,
          "danmaku": 13,
          "reply": 64,
          "favorite": 138,
          "coin": 35,
          "share": 27,
          "now_rank": 0,
          "his_rank": 0,
          "like": 192,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1029077386,
        "dimension": {
          "width": 4094,
          "height": 2160,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1zY411r7Ng",
        "short_link_v2": "https://b23.tv/BV1zY411r7Ng",
        "first_frame": "http://i2.hdslb.com/bfs/storyff/n230227a230303sxvxwhq018zv0y51vh_firsti.jpg",
        "pub_location": "浙江",
        "bvid": "BV1zY411r7Ng",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 907686430,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i0.hdslb.com/bfs/archive/94bbe7877290fcdbf6070b9941794c328fe1df53.jpg",
        "title": "新加坡VlogI 三天竟然花了5000多",
        "pubdate": 1677578400,
        "ctime": 1677560835,
        "desc": "-",
        "state": 0,
        "duration": 1333,
        "mission_id": 1333042,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 0,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 35174726,
          "name": "Eli与Toy",
          "face": "https://i2.hdslb.com/bfs/face/1052a59b450f52f97d72d0a7aabf53d4b62cca8f.jpg"
        },
        "stat": {
          "aid": 907686430,
          "view": 1313,
          "danmaku": 3,
          "reply": 15,
          "favorite": 18,
          "coin": 15,
          "share": 1,
          "now_rank": 0,
          "his_rank": 0,
          "like": 55,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1030174442,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1bM4y1o7JL",
        "short_link_v2": "https://b23.tv/BV1bM4y1o7JL",
        "first_frame": "http://i1.hdslb.com/bfs/storyff/n230228qnfn7fbfdm3mvg2wp9uq20v4o_firsti.jpg",
        "pub_location": "贵州",
        "bvid": "BV1bM4y1o7JL",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 266846543,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i0.hdslb.com/bfs/archive/0c3d3d12a87a65c28220314781d17d4dce0c72e1.jpg",
        "title": "我们的目标！把广东吃空！！",
        "pubdate": 1676262665,
        "ctime": 1676261745,
        "desc": "自驾游第一期！过年和爸妈一起去了广东！真的好幸福啊啊啊！小时候不懂事每次出去玩，总要和爸妈吵几架，现在已经究极好关系了！！没有什么事不是相互笑一笑过不去的！好爱现在的生活，爸妈身体健康，我有了可以带他们到处玩的能力，要更努力更努力！！！",
        "state": 0,
        "duration": 652,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 0,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 1072317049,
          "name": "宝剑嫂的小世界",
          "face": "https://i1.hdslb.com/bfs/face/365d1aeb88253c5efdf855c36068d45ecadcbf74.jpg"
        },
        "stat": {
          "aid": 266846543,
          "view": 488782,
          "danmaku": 2787,
          "reply": 1343,
          "favorite": 3762,
          "coin": 11912,
          "share": 2014,
          "now_rank": 0,
          "his_rank": 0,
          "like": 73943,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "旅游七天胖了五斤…广东真的太好吃了！",
        "cid": 1005700987,
        "dimension": {
          "width": 1080,
          "height": 1920,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1XY411i7PM",
        "short_link_v2": "https://b23.tv/BV1XY411i7PM",
        "first_frame": "http://i2.hdslb.com/bfs/storyff/n230213a27hkbspfv6i8lxtycaj3gp4n_firsti.jpg",
        "pub_location": "上海",
        "bvid": "BV1XY411i7PM",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 694258692,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i1.hdslb.com/bfs/archive/f9b3bb19e0638683d5421d8a254f1357df55c587.jpg",
        "title": "有一天，我们在雪山下奔跑。",
        "pubdate": 1676368654,
        "ctime": 1676368654,
        "desc": "这次，因为想拍一张以大山作为背景的结婚照，我们来到了日本鸟取县。然而，一场突如其来的大雪，把我们要去的目的地，全部埋在了白雪之中，拍摄计划全部被打乱。但这样的意外，才是我们的家常便饭...\n我们还坐了鸟取市的环游的士，司机大叔滔滔不绝，为我们一路讲了很多鸟取的人文和历史，对这座城市了解得更深刻了。\nP.S.查了一下，国内出发的话吉祥航空可以从上海直飞到鸟取米子市\n2023，让我们相遇在旅行的路上🖐",
        "state": 0,
        "duration": 266,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 1680997579,
          "name": "Masa和加三",
          "face": "https://i1.hdslb.com/bfs/face/90390c26e5066b8937999cab7e8d59faf228ea15.jpg"
        },
        "stat": {
          "aid": 694258692,
          "view": 20588,
          "danmaku": 129,
          "reply": 69,
          "favorite": 575,
          "coin": 715,
          "share": 269,
          "now_rank": 0,
          "his_rank": 0,
          "like": 1786,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "你，什么时候来找我们玩？",
        "cid": 1007616207,
        "dimension": {
          "width": 3840,
          "height": 2160,
          "rotate": 0
        },
        "season_id": 180933,
        "short_link": "https://b23.tv/BV1f24y1W7SX",
        "short_link_v2": "https://b23.tv/BV1f24y1W7SX",
        "first_frame": "http://i0.hdslb.com/bfs/storyff/n230214qn3o275rrc4yezr2uw2udnu2p_firsti.jpg",
        "pub_location": "日本",
        "bvid": "BV1f24y1W7SX",
        "season_type": 1,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 267802170,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i1.hdslb.com/bfs/archive/27301fa4549fd03558a79818369eceb75736e04c.jpg",
        "title": "【霹雳爷们儿】演员来到大理旅游后竟发出如此感叹！！！",
        "pubdate": 1677686880,
        "ctime": 1677686880,
        "desc": "霹雳爷们儿虎牙直播间：274874\n霹雳爷们儿B站账号：霹雳爷们儿668\n更多直播录像请关注：霹雳爷们儿录像小屋",
        "state": 0,
        "duration": 229,
        "mission_id": 1333042,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 13136390,
          "name": "暴躁刘师傅",
          "face": "https://i2.hdslb.com/bfs/face/326e3c5581946208c1c3e0c4f7040d3adb3244df.jpg"
        },
        "stat": {
          "aid": 267802170,
          "view": 745,
          "danmaku": 2,
          "reply": 12,
          "favorite": 5,
          "coin": 32,
          "share": 2,
          "now_rank": 0,
          "his_rank": 0,
          "like": 37,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1033843603,
        "dimension": {
          "width": 1920,
          "height": 1080,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV11Y411r7YD",
        "short_link_v2": "https://b23.tv/BV11Y411r7YD",
        "first_frame": "http://i1.hdslb.com/bfs/storyff/n230301qnuc4pn59jyk7t217epgruvcw_firsti.jpg",
        "pub_location": "辽宁",
        "bvid": "BV11Y411r7YD",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 482779457,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i0.hdslb.com/bfs/archive/34ed5c539ba4e9400bb71279b42f16dee549ca16.jpg",
        "title": "广州cpsp，扮成国漫天花板逛漫展是什么体验？",
        "pubdate": 1677665027,
        "ctime": 1677665027,
        "desc": "流水账，眷思量cos\n奉眠@微渺miroky_",
        "state": 0,
        "duration": 39,
        "mission_id": 1333042,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 0,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 7437481,
          "name": "爱拍照的玉老师",
          "face": "https://i1.hdslb.com/bfs/face/0153d10b009f7889550817ae3d60d3228c102d59.jpg"
        },
        "stat": {
          "aid": 482779457,
          "view": 2891,
          "danmaku": 2,
          "reply": 18,
          "favorite": 30,
          "coin": 16,
          "share": 4,
          "now_rank": 0,
          "his_rank": 0,
          "like": 422,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "",
        "cid": 1033297119,
        "dimension": {
          "width": 2160,
          "height": 3840,
          "rotate": 0
        },
        "short_link": "https://b23.tv/BV1qT411v78Z",
        "short_link_v2": "https://b23.tv/BV1qT411v78Z",
        "up_from_v2": 36,
        "first_frame": "http://i1.hdslb.com/bfs/storyff/n230301qn2syflczhtyvup27hbf0a4g9_firsti.jpg",
        "pub_location": "浙江",
        "bvid": "BV1qT411v78Z",
        "season_type": 0,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      },
      {
        "aid": 351555180,
        "videos": 1,
        "tid": 250,
        "tname": "出行",
        "copyright": 1,
        "pic": "http://i1.hdslb.com/bfs/archive/4c9516be8edb88bc50e6a1b2209011a4646a5123.jpg",
        "title": "卧槽！这是地铁站？老外对中国地铁站感到惊讶！说可以一天都呆在这里",
        "pubdate": 1675994682,
        "ctime": 1675984220,
        "desc": "记得点赞，关注，评论收藏噢！ins：https://www.instagram.com/rafaavedra/ YouTube ：https://youtube.com/rafagoesaround",
        "state": 0,
        "duration": 584,
        "mission_id": 1153647,
        "rights": {
          "bp": 0,
          "elec": 0,
          "download": 0,
          "movie": 0,
          "pay": 0,
          "hd5": 1,
          "no_reprint": 1,
          "autoplay": 1,
          "ugc_pay": 0,
          "is_cooperation": 0,
          "ugc_pay_preview": 0,
          "no_background": 0,
          "arc_pay": 0,
          "pay_free_watch": 0
        },
        "owner": {
          "mid": 651005588,
          "name": "Rafa的环游记",
          "face": "https://i2.hdslb.com/bfs/face/76ea276d397299cdb0b845ddda5d97290ba8d573.jpg"
        },
        "stat": {
          "aid": 351555180,
          "view": 736687,
          "danmaku": 2623,
          "reply": 1515,
          "favorite": 3297,
          "coin": 9220,
          "share": 1413,
          "now_rank": 0,
          "his_rank": 0,
          "like": 35095,
          "dislike": 0,
          "vt": 0,
          "vv": 0
        },
        "dynamic": "地铁区Up主来啦",
        "cid": 1000853532,
        "dimension": {
          "width": 3840,
          "height": 2160,
          "rotate": 0
        },
        "season_id": 1071225,
        "short_link": "https://b23.tv/BV1HR4y1q7kk",
        "short_link_v2": "https://b23.tv/BV1HR4y1q7kk",
        "first_frame": "http://i2.hdslb.com/bfs/storyff/n230209a2bphvrimev9es2hucdklkfht_firsti.jpg",
        "pub_location": "广东",
        "bvid": "BV1HR4y1q7kk",
        "season_type": 1,
        "is_ogv": false,
        "ogv_info": null,
        "rcmd_reason": ""
      }
    ],
    "Spec": null,
    "hot_share": {
      "show": false,
      "list": []
    },
    "elec": null,
    "recommend": null,
    "view_addit": {
      "63": false,
      "64": false,
      "69": false,
      "71": false,
      "72": false
    },
    "guide": null,
    "query_tags": null
  }
}
    """


def get_videoinfo(session: Session, cookies: RequestsCookieJar, bvid: str) -> Response:
    """获取视频信息

    Args:
        session (Session, optional): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取
        bvid (str): 视频ID

    Returns:
        Response: 返回结果
            成功 {
                "code": 0,
                "message": "0",
                "ttl": 1,
                "data": {
                    "bvid": "BV16v4y147EP",
                    "aid": 566624511,
                    "videos": 1,
                    "tid": 250,
                    "tname": "出行",
                    "copyright": 1,
                    "pic": "http://i2.hdslb.com/bfs/archive/af4081081cce65740a219dcb68b1e1783e4704f9.jpg",
                    "title": "深圳世界之窗春节烟花",
                    "pubdate": 1675781219,
                    "ctime": 1675781220,
                    "desc": "深圳世界之窗春节烟花",
                    "desc_v2": [
                    {
                        "raw_text": "深圳世界之窗春节烟花",
                        "type": 1,
                        "biz_id": 0
                    }
                    ],
                    "state": 0,
                    "duration": 55,
                    "mission_id": 1153647,
                    "rights": {
                        "bp": 0,
                        "elec": 0,
                        "download": 1,
                        "movie": 0,
                        "pay": 0,
                        "hd5": 0,
                        "no_reprint": 1,
                        "autoplay": 1,
                        "ugc_pay": 0,
                        "is_cooperation": 0,
                        "ugc_pay_preview": 0,
                        "no_background": 0,
                        "clean_mode": 0,
                        "is_stein_gate": 0,
                        "is_360": 0,
                        "no_share": 0,
                        "arc_pay": 0,
                        "free_watch": 0
                    },
                    "owner": {
                        "mid": 1614308159,
                        "name": "澎湖湾狠人",
                        "face": "https://i2.hdslb.com/bfs/face/4eb307be5329cf4e7fbe944946f3f894207a5ddc.jpg"
                    },
                    "stat": {
                        "aid": 566624511,
                        "view": 29,
                        "danmaku": 0,
                        "reply": 0,
                        "favorite": 0,
                        "coin": 0,
                        "share": 0,
                        "now_rank": 0,
                        "his_rank": 0,
                        "like": 1,
                        "dislike": 0,
                        "evaluation": "",
                        "argue_msg": ""
                    },
                    "dynamic": "",
                    "cid": 997878516,
                    "dimension": {
                        "width": 1920,
                        "height": 1080,
                        "rotate": 1
                    },
                    "premiere": null,
                    "teenage_mode": 0,
                    "is_chargeable_season": false,
                    "is_story": true,
                    "no_cache": false,
                    "pages": [
                    {
                        "cid": 997878516,
                        "page": 1,
                        "from": "vupload",
                        "part": "深圳世界之窗春节烟花",
                        "duration": 55,
                        "vid": "",
                        "weblink": "",
                        "dimension": {
                        "width": 1920,
                        "height": 1080,
                        "rotate": 1
                        },
                        "first_frame": "http://i0.hdslb.com/bfs/storyff/n230207qn29v8tglefsgkv36x53mr7b2_firsti.jpg"
                    }
                    ],
                    "subtitle": {
                        "allow_submit": false,
                        "list": []
                    },
                    "is_season_display": false,
                    "user_garb": {
                        "url_image_ani_cut": ""
                    },
                    "honor_reply": {},
                    "like_icon": "",
                    "need_jump_bv": false
                }
            }
    """


def get_spaceinfo(session: Session, cookies: RequestsCookieJar) -> Response:
    """获取空间信息
        该接口会检查头部，调用时记得带头部
            {
                "origin": "https://www.bilibili.com",
                "referer": "https://www.bilibili.com/video",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            }

    Args:
        session (Session, optional): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取

    Returns:
        Response: 返回结果
            成功 {
                "code": 0,
                "message": "0",
                "ttl": 1,
                "data": {
                    "mid": 1614308159,
                    "name": "澎湖湾狠人",
                    "sex": "保密",
                    "face": "https://i2.hdslb.com/bfs/face/4eb307be5329cf4e7fbe944946f3f894207a5ddc.jpg",
                    "face_nft": 0,
                    "face_nft_type": 0,
                    "sign": "",
                    "rank": 10000,
                    "level": 3,
                    "jointime": 0,
                    "moral": 0,
                    "silence": 0,
                    "coins": 168,
                    "fans_badge": false,
                    "fans_medal": {
                    "show": true,
                    "wear": false,
                    "medal": null
                    },
                    "official": {
                    "role": 0,
                    "title": "",
                    "desc": "",
                    "type": -1
                    },
                    "vip": {
                    "type": 0,
                    "status": 0,
                    "due_date": 0,
                    "vip_pay_type": 0,
                    "theme_type": 0,
                    "label": {
                        "path": "",
                        "text": "",
                        "label_theme": "",
                        "text_color": "",
                        "bg_style": 0,
                        "bg_color": "",
                        "border_color": "",
                        "use_img_label": true,
                        "img_label_uri_hans": "",
                        "img_label_uri_hant": "",
                        "img_label_uri_hans_static": "https://i0.hdslb.com/bfs/vip/d7b702ef65a976b20ed854cbd04cb9e27341bb79.png",
                        "img_label_uri_hant_static": "https://i0.hdslb.com/bfs/activity-plat/static/20220614/e369244d0b14644f5e1a06431e22a4d5/KJunwh19T5.png"
                    },
                    "avatar_subscript": 0,
                    "nickname_color": "",
                    "role": 0,
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
                    "nid": 0,
                    "name": "",
                    "image": "",
                    "image_small": "",
                    "level": "",
                    "condition": ""
                    },
                    "user_honour_info": {
                    "mid": 0,
                    "colour": null,
                    "tags": []
                    },
                    "is_followed": false,
                    "top_photo": "http://i2.hdslb.com/bfs/space/cb1c3ef50e22b6096fde67febe863494caefebad.png",
                    "theme": {},
                    "sys_notice": {},
                    "live_room": {
                    "roomStatus": 1,
                    "liveStatus": 0,
                    "url": "https://live.bilibili.com/25835033?broadcast_type=0&is_room_feed=1",
                    "title": "命运女郎",
                    "cover": "http://i0.hdslb.com/bfs/live/user_cover/7b5a72746d2ed4d02a88a55ab60ffa0918d3ef36.jpg",
                    "roomid": 25835033,
                    "roundStatus": 0,
                    "broadcast_type": 0,
                    "watched_show": {
                        "switch": true,
                        "num": 2,
                        "text_small": "2",
                        "text_large": "2人看过",
                        "icon": "https://i0.hdslb.com/bfs/live/a725a9e61242ef44d764ac911691a7ce07f36c1d.png",
                        "icon_location": "",
                        "icon_web": "https://i0.hdslb.com/bfs/live/8d9d0f33ef8bf6f308742752d13dd0df731df19c.png"
                    }
                    },
                    "birthday": "01-05",
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
                        "show": false,
                        "state": -1,
                        "title": "",
                        "icon": "",
                        "jump_url": ""
                    }
                    },
                    "contract": {
                    "is_display": false,
                    "is_follow_display": false
                    }
                }
            }
    """


def search_videos(session: Session, cookies: RequestsCookieJar, keyword: str, page: int, page_size: int, tid: int, order: str, duration_type: int) -> Response:
    """查询视频

    Args:
        session (Session, optional): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取
        keyword (str): 关键词
        page (int): 页数
        page_size (int): 每天数量
        tid (int): 分区ID
            搞笑、舞蹈、纪录片、生活、综艺、知识等等
        order (str): 排序
            click: 最多点击   pubdate: 最近发布   dm: 最多弹幕  stow: 最多收藏
        duration_type (int): 时长
            1: 10分钟以下  2: 10-30分钟  3: 30-60分钟  4: 60分钟以上

    Returns:
        Response: 返回结果
            成功 {
                "code": 0,
                "message": "0",
                "ttl": 1,
                "data": {
                    "seid": "8811846583901040474",
                    "page": 1,
                    "pagesize": 1,
                    "numResults": 245,
                    "numPages": 245,
                    "suggest_keyword": "",
                    "rqt_type": "search",
                    "cost_time": {
                        "params_check": "0.000971",
                        "is_risk_query": "0.000223",
                        "illegal_handler": "0.000085",
                        "as_response_format": "0.000683",
                        "as_request": "0.048738",
                        "save_cache": "0.000007",
                        "deserialize_response": "0.000186",
                        "as_request_format": "0.000467",
                        "total": "0.058831",
                        "main_handler": "0.050939"
                    },
                    "exp_list": {
                        "6601": true,
                        "9901": true,
                        "5514": true,
                        "7701": true
                    },
                    "egg_hit": 0,
                    "result": [
                    {
                        "type": "video",
                        "id": 378206168,
                        "author": "饿梦美食印度",
                        "mid": 1149587932,
                        "typeid": "76",
                        "typename": "美食制作",
                        "arcurl": "http://www.bilibili.com/video/av378206168",
                        "aid": 378206168,
                        "bvid": "BV12f4y1w7Qt",
                        "title": "在印度有一种头开的水果，千万不要尝试",
                        "description": "-",
                        "arcrank": "0",
                        "pic": "//i2.hdslb.com/bfs/archive/320a7beb900088876cc3db4ec664e0286dec034e.jpg",
                        "play": 7971875,
                        "video_review": 29,
                        "favorites": 2152,
                        "tag": "人类沙雕行为,印度美食",
                        "review": 47,
                        "pubdate": 1632731251,
                        "senddate": 1632731251,
                        "duration": "1:2",
                        "badgepay": false,
                        "hit_columns": [
                        "tag"
                        ],
                        "view_type": "",
                        "is_pay": 0,
                        "is_union_video": 0,
                        "rec_tags": null,
                        "new_rec_tags": [],
                        "rank_score": 7971875,
                        "like": 4214,
                        "upic": "https://i1.hdslb.com/bfs/face/090e75a3df0bc73e30f60f84a3d5652a243635b9.jpg",
                        "corner": "",
                        "cover": "",
                        "desc": "",
                        "url": "",
                        "rec_reason": "",
                        "danmaku": 29,
                        "biz_data": null
                    }
                    ],
                    "show_column": 0,
                    "in_black_key": 0,
                    "in_white_key": 0
                }
            }
    """


def search_users(session: Session, cookies: RequestsCookieJar, keyword: str, page: int, page_size: int) -> Response:
    """查询用户

    Args:
        session (Session, optional): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取
        keyword (str): 关键词
        page (int): 页数
        page_size (int): 每天数量

    Returns:
        Response: 返回结果
            成功 {
                "code": 0,
                "message": "0",
                "ttl": 1,
                "data": {
                    "seid": "588401944436269683",
                    "page": 1,
                    "pagesize": 1,
                    "numResults": 1000,
                    "numPages": 1000,
                    "suggest_keyword": "",
                    "rqt_type": "search",
                    "cost_time": {
                    "params_check": "0.000659",
                    "get upuser live status": "0.000003",
                    "is_risk_query": "0.000184",
                    "illegal_handler": "0.000067",
                    "as_response_format": "0.000675",
                    "as_request": "0.107137",
                    "save_cache": "0.000004",
                    "deserialize_response": "0.000195",
                    "as_request_format": "0.000316",
                    "total": "0.149040",
                    "main_handler": "0.108583"
                    },
                    "exp_list": {
                    "6601": true,
                    "9901": true,
                    "5514": true,
                    "7701": true
                    },
                    "egg_hit": 0,
                    "result": [
                    {
                        "type": "bili_user",
                        "mid": 16391550,
                        "uname": "人类",
                        "usign": "要早睡早起\n                                     －鲁迅",
                        "fans": 66,
                        "videos": 5,
                        "upic": "//i2.hdslb.com/bfs/face/785c2c5eda4449c392b503612fcd6fbee4e641b2.jpg",
                        "face_nft": 0,
                        "face_nft_type": 0,
                        "verify_info": "",
                        "level": 6,
                        "gender": 1,
                        "is_upuser": 1,
                        "is_live": 0,
                        "room_id": 0,
                        "res": [
                        {
                            "aid": 676042130,
                            "bvid": "BV1yU4y1w783",
                            "title": "犹豫到最后一天还是抽了，不想后悔好几个版本，瞧这条鱼多好看呀。",
                            "pubdate": 1634145015,
                            "arcurl": "http://www.bilibili.com/video/av676042130",
                            "pic": "//i1.hdslb.com/bfs/archive/4bc72eb0014b1aa51f584e22557e213d0a675824.jpg",
                            "play": "9276",
                            "dm": 2,
                            "coin": 5,
                            "fav": 0,
                            "desc": "因为是大保底之前一直没打算抽，也没有准备突破材料，圣遗物也是芭芭拉身上的。",
                            "duration": "2:0",
                            "is_pay": 0,
                            "is_union_video": 0
                        },
                        {
                            "aid": 505806643,
                            "bvid": "BV1du411f7Zr",
                            "title": "原神一周年记录",
                            "pubdate": 1632845815,
                            "arcurl": "http://www.bilibili.com/video/av505806643",
                            "pic": "//i1.hdslb.com/bfs/archive/c3197bb6deb66c565737e630b5d684c6f33496ea.jpg",
                            "play": "45",
                            "dm": 0,
                            "coin": 0,
                            "fav": 1,
                            "desc": "",
                            "duration": "7:10",
                            "is_pay": 0,
                            "is_union_video": 0
                        },
                        {
                            "aid": 933168193,
                            "bvid": "BV1sM4y137TG",
                            "title": "杨过开箱",
                            "pubdate": 1632469249,
                            "arcurl": "http://www.bilibili.com/video/av933168193",
                            "pic": "//i0.hdslb.com/bfs/archive/72ac00f997314d5fc913126fb0246cb1b237ba73.jpg",
                            "play": "218",
                            "dm": 0,
                            "coin": 0,
                            "fav": 1,
                            "desc": "-",
                            "duration": "1:8",
                            "is_pay": 0,
                            "is_union_video": 0
                        }
                        ],
                        "official_verify": {
                        "type": 127,
                        "desc": ""
                        },
                        "hit_columns": [
                        "uname"
                        ],
                        "is_senior_member": 1
                    }
                    ],
                    "show_column": 0,
                    "in_black_key": 0,
                    "in_white_key": 0
                }
            }
    """


def top_reply(session: Session, cookies: RequestsCookieJar, aid: int, rpid: int) -> Response:
    """评论置顶

    Args:
        session (Session, optional): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取
        aid (int): 视频ID
        rpid (int): 评论ID

    Returns:
        Response: 返回结果
            成功  {
                "code": 0,
                "message": "0",
                "ttl": 1
            }
    """


def add_reply(session: Session, cookies: RequestsCookieJar, aid: int, message: str) -> Response:
    """发表评论

    Args:
        session (Session, optional): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取
        aid (int): 视频ID
        message (str): 评论内容

    Returns:
        Response: 返回结果
            成功 {
                "code": 0,
                "message": "0",
                "ttl": 1,
                "data": {
                    "need_captcha": false,
                    "url": "",
                    "success_action": 0,
                    "success_toast": "发送成功",
                    "success_animation": "",
                    "rpid": 153683115376,
                    "rpid_str": "153683115376",
                    "dialog": 0,
                    "dialog_str": "0",
                    "root": 0,
                    "root_str": "0",
                    "parent": 0,
                    "parent_str": "0",
                    "reply": {
                    "rpid": 153683115376,
                    "oid": 814098534,
                    "type": 1,
                    "mid": 1614308159,
                    "root": 0,
                    "parent": 0,
                    "dialog": 0,
                    "count": 0,
                    "rcount": 0,
                    "state": 0,
                    "fansgrade": 0,
                    "attr": 0,
                    "ctime": 1677222818,
                    "rpid_str": "153683115376",
                    "root_str": "0",
                    "parent_str": "0",
                    "like": 0,
                    "action": 0,
                    "member": {
                        "mid": "1614308159",
                        "uname": "澎湖湾狠人",
                        "sex": "保密",
                        "sign": "",
                        "avatar": "https://i2.hdslb.com/bfs/face/4eb307be5329cf4e7fbe944946f3f894207a5ddc.jpg",
                        "rank": "10000",
                        "face_nft_new": 0,
                        "is_senior_member": 0,
                        "level_info": {
                        "current_level": 3,
                        "current_min": 0,
                        "current_exp": 0,
                        "next_exp": 0
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
                        "nid": 0,
                        "name": "",
                        "image": "",
                        "image_small": "",
                        "level": "",
                        "condition": ""
                        },
                        "official_verify": {
                        "type": -1,
                        "desc": ""
                        },
                        "vip": {
                        "vipType": 0,
                        "vipDueDate": 0,
                        "dueRemark": "",
                        "accessStatus": 0,
                        "vipStatus": 0,
                        "vipStatusWarn": "",
                        "themeType": 0,
                        "label": {
                            "path": "",
                            "text": "",
                            "label_theme": "",
                            "text_color": "",
                            "bg_style": 0,
                            "bg_color": "",
                            "border_color": "",
                            "use_img_label": true,
                            "img_label_uri_hans": "",
                            "img_label_uri_hant": "",
                            "img_label_uri_hans_static": "https://i0.hdslb.com/bfs/vip/d7b702ef65a976b20ed854cbd04cb9e27341bb79.png",
                            "img_label_uri_hant_static": "https://i0.hdslb.com/bfs/activity-plat/static/20220614/e369244d0b14644f5e1a06431e22a4d5/KJunwh19T5.png"
                        },
                        "avatar_subscript": 0,
                        "nickname_color": ""
                        },
                        "fans_detail": null,
                        "user_sailing": {
                        "pendant": null,
                        "cardbg": null,
                        "cardbg_with_focus": null
                        },
                        "is_contractor": false,
                        "contract_desc": "",
                        "nft_interaction": null,
                        "avatar_item": {
                        "container_size": {
                            "width": 1.8,
                            "height": 1.8
                        },
                        "fallback_layers": {
                            "layers": [
                            {
                                "visible": true,
                                "general_spec": {
                                "pos_spec": {
                                    "coordinate_pos": 2,
                                    "axis_x": 0.9,
                                    "axis_y": 0.9
                                },
                                "size_spec": {
                                    "width": 1,
                                    "height": 1
                                },
                                "render_spec": {
                                    "opacity": 1
                                }
                                },
                                "layer_config": {
                                "tags": {
                                    "AVATAR_LAYER": {}
                                },
                                "is_critical": true,
                                "layer_mask": {
                                    "general_spec": {
                                    "pos_spec": {
                                        "coordinate_pos": 2,
                                        "axis_x": 0.9,
                                        "axis_y": 0.9
                                    },
                                    "size_spec": {
                                        "width": 1,
                                        "height": 1
                                    },
                                    "render_spec": {
                                        "opacity": 1
                                    }
                                    },
                                    "mask_src": {
                                    "src_type": 3,
                                    "draw": {
                                        "draw_type": 1,
                                        "fill_mode": 1,
                                        "color_config": {
                                        "day": {
                                            "argb": "#FF000000"
                                        }
                                        }
                                    }
                                    }
                                }
                                },
                                "resource": {
                                "res_type": 3,
                                "res_image": {
                                    "image_src": {
                                    "src_type": 1,
                                    "placeholder": 6,
                                    "remote": {
                                        "url": "https://i2.hdslb.com/bfs/face/4eb307be5329cf4e7fbe944946f3f894207a5ddc.jpg",
                                        "bfs_style": "widget-layer-avatar"
                                    }
                                    }
                                }
                                }
                            }
                            ],
                            "is_critical_group": true
                        },
                        "mid": "1614308159"
                        }
                    },
                    "content": {
                        "message": "哈哈哈",
                        "members": [],
                        "jump_url": {},
                        "max_line": 6
                    },
                    "replies": null,
                    "assist": 0,
                    "up_action": {
                        "like": false,
                        "reply": false
                    },
                    "invisible": false,
                    "reply_control": {
                        "max_line": 6,
                        "time_desc": "1秒前发布",
                        "location": "IP属地：广东"
                    },
                    "folder": {
                        "has_folded": false,
                        "is_folded": false,
                        "rule": ""
                    },
                    "dynamic_id_str": "0"
                    },
                    "OptSubject": {
                    "oid": 814098534,
                    "type": 1,
                    "mid": 1614308159,
                    "count": 3,
                    "rcount": 3,
                    "acount": 2,
                    "state": 0,
                    "attr": 0,
                    "meta": "{\"tcmid\":387783803}",
                    "ctime": 1659334490,
                    "mtime": 1668745960
                    }
                }
            }
    """


def get_playurl2(session: Session, cookies: RequestsCookieJar, bvid: str, cid: int) -> Response:
    """解析播放地址(.m4s视频和音频)
        该接口可得到高清晰度 1080P 的视频，但需要自行合并音频

        bvid + cid 才能唯一确定视频文件地址, 因为一个合集作品可能有多个视频

    Args:
        session (Session, optional): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取
        bvid (str): 作品ID
        cid (int): 集数ID 

    Returns:
        Response: 返回结果
            成功 {
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "from": "local",
    "result": "suee",
    "message": "",
    "quality": 32,
    "format": "flv480",
    "timelength": 54911,
    "accept_format": "hdflv2,flv,flv720,flv480,mp4",
    "accept_description": [
      "高清 1080P+",
      "高清 1080P",
      "高清 720P",
      "清晰 480P",
      "流畅 360P"
    ],
    "accept_quality": [
      112,
      80,
      64,
      32,
      16
    ],
    "video_codecid": 7,
    "seek_param": "start",
    "seek_type": "offset",
    "dash": {
      "duration": 55,
      "minBufferTime": 1.5,
      "min_buffer_time": 1.5,
      "video": [
        {
          "id": 32,
          "baseUrl": "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30032.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=830e0afd372cc1b55162a511075d40a5&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=104618&logo=80000000",
          "base_url": "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30032.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=830e0afd372cc1b55162a511075d40a5&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=104618&logo=80000000",
          "backupUrl": [
            "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30032.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=830e0afd372cc1b55162a511075d40a5&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=1,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=104618&logo=40000000",
            "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30032.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=830e0afd372cc1b55162a511075d40a5&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=2,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=104618&logo=40000000"
          ],
          "backup_url": [
            "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30032.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=830e0afd372cc1b55162a511075d40a5&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=1,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=104618&logo=40000000",
            "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30032.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=830e0afd372cc1b55162a511075d40a5&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=2,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=104618&logo=40000000"
          ],
          "bandwidth": 823425,
          "mimeType": "video/mp4",
          "mime_type": "video/mp4",
          "codecs": "avc1.64001F",
          "width": 480,
          "height": 852,
          "frameRate": "29.412",
          "frame_rate": "29.412",
          "sar": "639:640",
          "startWithSap": 1,
          "start_with_sap": 1,
          "SegmentBase": {
            "Initialization": "0-1010",
            "indexRange": "1011-1174"
          },
          "segment_base": {
            "initialization": "0-1010",
            "index_range": "1011-1174"
          },
          "codecid": 7
        },
        {
          "id": 16,
          "baseUrl": "https://upos-sz-estgoss.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30016.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=upos&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=3990aaf89a58f78985662858597070ff&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=45335&logo=80000000",
          "base_url": "https://upos-sz-estgoss.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30016.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=upos&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=3990aaf89a58f78985662858597070ff&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=45335&logo=80000000",
          "backupUrl": [
            "https://upos-sz-mirrorali.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30016.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=alibv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=94f578338d69cb61f798d1f458c859ea&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=1,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=45335&logo=40000000",
            "https://upos-sz-mirroralib.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30016.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=alibbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=7eb51c1846b79bcc4bb47cc928088dd8&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=2,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=45335&logo=40000000"
          ],
          "backup_url": [
            "https://upos-sz-mirrorali.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30016.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=alibv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=94f578338d69cb61f798d1f458c859ea&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=1,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=45335&logo=40000000",
            "https://upos-sz-mirroralib.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30016.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=alibbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=7eb51c1846b79bcc4bb47cc928088dd8&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=2,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=45335&logo=40000000"
          ],
          "bandwidth": 356824,
          "mimeType": "video/mp4",
          "mime_type": "video/mp4",
          "codecs": "avc1.64001E",
          "width": 360,
          "height": 640,
          "frameRate": "29.412",
          "frame_rate": "29.412",
          "sar": "1:1",
          "startWithSap": 1,
          "start_with_sap": 1,
          "SegmentBase": {
            "Initialization": "0-1014",
            "indexRange": "1015-1178"
          },
          "segment_base": {
            "initialization": "0-1014",
            "index_range": "1015-1178"
          },
          "codecid": 7
        }
      ],
      "audio": [
        {
          "id": 30280,
          "baseUrl": "https://upos-sz-estgoss.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=upos&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=f38485bc8ca5c14937ebddcd3b1d65fd&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=25007&logo=80000000",
          "base_url": "https://upos-sz-estgoss.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=upos&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=f38485bc8ca5c14937ebddcd3b1d65fd&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=25007&logo=80000000",
          "backupUrl": [
            "https://upos-sz-mirrorali.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=alibv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=9e5291309e79b1190df604f165baa071&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=1,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=25007&logo=40000000",
            "https://upos-sz-mirroralib.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=alibbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=e68ee94df6e521e7afe694d8ab8a6d86&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=2,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=25007&logo=40000000"
          ],
          "backup_url": [
            "https://upos-sz-mirrorali.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=alibv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=9e5291309e79b1190df604f165baa071&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=1,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=25007&logo=40000000",
            "https://upos-sz-mirroralib.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=alibbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=e68ee94df6e521e7afe694d8ab8a6d86&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=2,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=25007&logo=40000000"
          ],
          "bandwidth": 196970,
          "mimeType": "audio/mp4",
          "mime_type": "audio/mp4",
          "codecs": "mp4a.40.2",
          "width": 0,
          "height": 0,
          "frameRate": "",
          "frame_rate": "",
          "sar": "",
          "startWithSap": 0,
          "start_with_sap": 0,
          "SegmentBase": {
            "Initialization": "0-933",
            "indexRange": "934-1097"
          },
          "segment_base": {
            "initialization": "0-933",
            "index_range": "934-1097"
          },
          "codecid": 0
        },
        {
          "id": 30216,
          "baseUrl": "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30216.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=acf681d341972c8a3a6288125bdf567e&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=6271&logo=80000000",
          "base_url": "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30216.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=acf681d341972c8a3a6288125bdf567e&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=6271&logo=80000000",
          "backupUrl": [
            "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30216.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=acf681d341972c8a3a6288125bdf567e&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=1,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=6271&logo=40000000",
            "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30216.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=acf681d341972c8a3a6288125bdf567e&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=2,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=6271&logo=40000000"
          ],
          "backup_url": [
            "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30216.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=acf681d341972c8a3a6288125bdf567e&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=1,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=6271&logo=40000000",
            "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30216.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=acf681d341972c8a3a6288125bdf567e&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=2,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=6271&logo=40000000"
          ],
          "bandwidth": 49335,
          "mimeType": "audio/mp4",
          "mime_type": "audio/mp4",
          "codecs": "mp4a.40.5",
          "width": 0,
          "height": 0,
          "frameRate": "",
          "frame_rate": "",
          "sar": "",
          "startWithSap": 0,
          "start_with_sap": 0,
          "SegmentBase": {
            "Initialization": "0-943",
            "indexRange": "944-1107"
          },
          "segment_base": {
            "initialization": "0-943",
            "index_range": "944-1107"
          },
          "codecid": 0
        },
        {
          "id": 30232,
          "baseUrl": "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30232.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=0eb52019e051c065fb0eaf891b2407e3&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=14400&logo=80000000",
          "base_url": "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30232.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=0eb52019e051c065fb0eaf891b2407e3&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=14400&logo=80000000",
          "backupUrl": [
            "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30232.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=0eb52019e051c065fb0eaf891b2407e3&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=1,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=14400&logo=40000000",
            "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30232.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=0eb52019e051c065fb0eaf891b2407e3&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=2,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=14400&logo=40000000"
          ],
          "backup_url": [
            "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30232.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=0eb52019e051c065fb0eaf891b2407e3&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=1,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=14400&logo=40000000",
            "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-30232.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1677739473&gen=playurlv2&os=08ctbv&oi=1901535305&trid=09145d76369b4c338000da790d3c8f57u&mid=0&platform=pc&upsig=0eb52019e051c065fb0eaf891b2407e3&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=2,3&buvid=5E9801C7-9A82-BC34-F286-70BF1249F50655182infoc&build=0&agrr=1&bw=14400&logo=40000000"
          ],
          "bandwidth": 113422,
          "mimeType": "audio/mp4",
          "mime_type": "audio/mp4",
          "codecs": "mp4a.40.2",
          "width": 0,
          "height": 0,
          "frameRate": "",
          "frame_rate": "",
          "sar": "",
          "startWithSap": 0,
          "start_with_sap": 0,
          "SegmentBase": {
            "Initialization": "0-933",
            "indexRange": "934-1097"
          },
          "segment_base": {
            "initialization": "0-933",
            "index_range": "934-1097"
          },
          "codecid": 0
        }
      ],
      "dolby": {
        "type": 0,
        "audio": null
      },
      "flac": null
    },
    "support_formats": [
      {
        "quality": 112,
        "format": "hdflv2",
        "new_description": "1080P 高码率",
        "display_desc": "1080P",
        "superscript": "高码率",
        "codecs": [
          "avc1.640028"
        ]
      },
      {
        "quality": 80,
        "format": "flv",
        "new_description": "1080P 高清",
        "display_desc": "1080P",
        "superscript": "",
        "codecs": [
          "avc1.640028"
        ]
      },
      {
        "quality": 64,
        "format": "flv720",
        "new_description": "720P 高清",
        "display_desc": "720P",
        "superscript": "",
        "codecs": [
          "avc1.64001F"
        ]
      },
      {
        "quality": 32,
        "format": "flv480",
        "new_description": "480P 清晰",
        "display_desc": "480P",
        "superscript": "",
        "codecs": [
          "avc1.64001F"
        ]
      },
      {
        "quality": 16,
        "format": "mp4",
        "new_description": "360P 流畅",
        "display_desc": "360P",
        "superscript": "",
        "codecs": [
          "avc1.64001E"
        ]
      }
    ],
    "high_format": null,
    "last_play_time": 0,
    "last_play_cid": 0
  }
}
    """


def get_playurl(session: Session, cookies: RequestsCookieJar, bvid: str, cid: int) -> Response:
    """解析播放地址(.mp4视频)
        注意该接口返回的视频清晰度可能只有 360p

        bvid + cid 才能唯一确定视频文件地址, 因为一个合集作品可能有多个视频

    Args:
        session (Session, optional): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取
        bvid (str): 作品ID
        cid (int): 集数ID 

    Returns:
        Response: 返回结果
            成功 {
                "code": 0,
                "message": "0",
                "ttl": 1,
                "data": {
                    "from": "local",
                    "result": "suee",
                    "message": "",
                    "quality": 16,
                    "format": "mp4",
                    "timelength": 54912,
                    "accept_format": "mp4",
                    "accept_description": [
                        "流畅 360P"
                    ],
                    "accept_quality": [
                        16
                    ],
                    "video_codecid": 7,
                    "seek_param": "start",
                    "seek_type": "second",
                    "durl": [
                    {
                        "order": 1,
                        "length": 54912,
                        "size": 2802786,
                        "ahead": "",
                        "vhead": "",
                        "url": "https://upos-sz-mirror08ct.bilivideo.com/upgcxcode/16/85/997878516/997878516-1-16.mp4?e=ig8euxZM2rNcNbRVhwdVhwdlhWdVhwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&uipk=5&nbs=1&deadline=1677233313&gen=playurlv2&os=08ctbv&oi=1032677146&trid=fc8bc899565140e1bf29f5359f70a140h&mid=0&platform=html5&upsig=4f8b18c8c0e2b7a2a5df4cb4cc746002&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&bw=51903&logo=80000000",
                        "backup_url": null
                    }
                    ],
                    "support_formats": [
                    {
                        "quality": 16,
                        "format": "mp4",
                        "new_description": "360P 流畅",
                        "display_desc": "360P",
                        "superscript": "",
                        "codecs": null
                    }
                    ],
                    "high_format": null,
                    "last_play_time": 0,
                    "last_play_cid": 0
                }
            }
    """


def get_myinfo(session: Session, cookies: RequestsCookieJar) -> Response:
    """获取个人信息

    Args:
        session (Session, optional): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取

    Returns:
        Response: 返回结果
            成功 {
                "code": 0,
                "message": "0",
                "ttl": 1,
                "data": {
                    "mid": 1614308159,
                    "name": "澎湖湾狠人",
                    "sex": "保密",
                    "face": "https://i2.hdslb.com/bfs/face/4eb307be5329cf4e7fbe944946f3f894207a5ddc.jpg",
                    "sign": "",
                    "rank": 10000,
                    "level": 3,
                    "jointime": 0,
                    "moral": 70,
                    "silence": 0,
                    "email_status": 0,
                    "tel_status": 1,
                    "identification": 1,
                    "vip": {
                    "type": 0,
                    "status": 0,
                    "due_date": 0,
                    "vip_pay_type": 0,
                    "theme_type": 0,
                    "label": {
                        "path": "",
                        "text": "",
                        "label_theme": "",
                        "text_color": "",
                        "bg_style": 0,
                        "bg_color": "",
                        "border_color": "",
                        "use_img_label": true,
                        "img_label_uri_hans": "",
                        "img_label_uri_hant": "",
                        "img_label_uri_hans_static": "https://i0.hdslb.com/bfs/vip/d7b702ef65a976b20ed854cbd04cb9e27341bb79.png",
                        "img_label_uri_hant_static": "https://i0.hdslb.com/bfs/activity-plat/static/20220614/e369244d0b14644f5e1a06431e22a4d5/KJunwh19T5.png"
                    },
                    "avatar_subscript": 0,
                    "nickname_color": "",
                    "role": 0,
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
                        "nid": 0,
                        "name": "",
                        "image": "",
                        "image_small": "",
                        "level": "",
                        "condition": ""
                    },
                    "official": {
                        "role": 0,
                        "title": "",
                        "desc": "",
                        "type": -1
                    },
                    "birthday": 978624000,
                    "is_tourist": 0,
                    "is_fake_account": 0,
                    "pin_prompting": 1,
                    "is_deleted": 0,
                    "in_reg_audit": 0,
                    "is_rip_user": false,
                    "profession": {
                        "id": 0,
                        "name": "",
                        "show_name": "",
                        "is_show": 0,
                        "category_one": "",
                        "realname": "",
                        "title": "",
                        "department": ""
                    },
                    "face_nft": 0,
                    "face_nft_new": 0,
                    "is_senior_member": 0,
                    "honours": {
                        "mid": 1614308159,
                        "colour": {
                            "dark": "#CE8620",
                            "normal": "#F0900B"
                        },
                        "tags": null
                    },
                    "digital_id": "",
                    "digital_type": -2,
                    "level_exp": {
                        "current_level": 3,
                        "current_min": 1500,
                        "current_exp": 2300,
                        "next_exp": 4500,
                        "level_up": 1668616181
                    },
                    "coins": 168,
                    "following": 2,
                    "follower": 2
                }
            }
    """


def get_followers(session: Session, cookies: RequestsCookieJar) -> Response:
    """获取粉丝列表

    Args:
        session (Session, optional): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取

    Returns:
        Response: 返回结果
            成功 {
            "code": 0,
            "message": "0",
            "ttl": 1,
            "data": {
                "list": [
                {
                    "mid": 1045472466,
                    "attribute": 6,
                    "mtime": 1661914305,
                    "tag": null,
                    "special": 0,
                    "contract_info": {},
                    "uname": "F菌一天3次",
                    "face": "https://i0.hdslb.com/bfs/face/3e3c7593c0411b0afa95ab09360ff7881ec6c333.jpg",
                    "sign": "",
                    "face_nft": 0,
                    "official_verify": {
                    "type": -1,
                    "desc": ""
                    },
                    "vip": {
                    "vipType": 0,
                    "vipDueDate": 0,
                    "dueRemark": "",
                    "accessStatus": 0,
                    "vipStatus": 0,
                    "vipStatusWarn": "",
                    "themeType": 0,
                    "label": {
                        "path": "",
                        "text": "",
                        "label_theme": "",
                        "text_color": "",
                        "bg_style": 0,
                        "bg_color": "",
                        "border_color": ""
                    },
                    "avatar_subscript": 0,
                    "nickname_color": "",
                    "avatar_subscript_url": ""
                    },
                    "nft_icon": "",
                    "rec_reason": "",
                    "track_id": ""
                }
                ],
                "re_version": 0,
                "total": 1
            }
        }
    """

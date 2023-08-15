from requests import Session, Response
from requests.cookies import RequestsCookieJar


def join_activity(session: Session, cookies: RequestsCookieJar, act_id: int) -> Response:
    """参加活动

    Args:
        session (Session): 可能需要代理
        cookies (RequestsCookieJar): 抓包获取
        act_id (int): 活动ID

    Returns:
        Response: 返回请求
            成功
{
    "code": 0,
    "message": "0",
    "ttl": 1
}
    """


def list_activity(session: Session, cookies: RequestsCookieJar) -> Response:
    """获取活动列表

    Args:
        session (Session): 可能需要代理
        cookies (RequestsCookieJar): 抓包获取

    Returns:
        Response: 返回请求
            成功
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "list": [
            {
                "act_id": 547,
                "title": "必剪3月创作打卡（第二期）",
                "act_img": "http://i0.hdslb.com/bfs/archive/fdef521aab3d3e6390ce8833f168698a9718ab90.png",
                "rtime": 1678636800,
                "stime": 1678636800,
                "etime": 1679846399,
                "icon_state": 1,
                "act_tags": [
                    "10万",
                    "必剪"
                ],
                "act_brief": "报名打卡后，使用必剪投稿",
                "process": 0,
                "process_type": 0,
                "business": 1,
                "topic": null,
                "tags": "",
                "rank": 20,
                "call_type": 3,
                "material": null
            },
            {
                "act_id": 477,
                "title": "粉丝音乐安利打卡挑战",
                "act_img": "http://i0.hdslb.com/bfs/archive/14c83f292c2adeb2c5f16ee0783d9300bcc257e4.jpg",
                "rtime": 1675958400,
                "stime": 1675958400,
                "etime": 1680278399,
                "icon_state": 1,
                "act_tags": [
                    "粉丝二创",
                    "安利"
                ],
                "act_brief": "投稿音乐安利相关视频参与打卡",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1006596,
                    "name": "粉丝音乐安利大赛"
                },
                "tags": "",
                "rank": 14,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 549,
                "title": "用照片记录春天",
                "act_img": "http://i0.hdslb.com/bfs/archive/6207cd7515379dd2aafd09f0dc8e9b061608d1f6.jpg",
                "rtime": 1678636800,
                "stime": 1678636800,
                "etime": 1679846399,
                "icon_state": 1,
                "act_tags": [
                    "图片转视频",
                    "限时有奖活动"
                ],
                "act_brief": "使用图片转视频记录生活，赢打卡大奖",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1017312,
                    "name": "记录春天日常"
                },
                "tags": "",
                "rank": 13,
                "call_type": 2,
                "material": {
                    "material_type": -72,
                    "material_id": 0
                }
            },
            {
                "act_id": 530,
                "title": "游戏玩家的日常",
                "act_img": "http://i0.hdslb.com/bfs/archive/2379034aa2a80d7622a31b19d97c0234bf163a19.jpg",
                "rtime": 1678032000,
                "stime": 1678032000,
                "etime": 1680451199,
                "icon_state": 1,
                "act_tags": [
                    "周周有奖",
                    "游戏区"
                ],
                "act_brief": "在游戏区投稿",
                "process": 0,
                "process_type": 0,
                "business": 6,
                "topic": null,
                "tags": "",
                "rank": 13,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 561,
                "title": "每日职场唠嗑",
                "act_img": "http://i0.hdslb.com/bfs/archive/04dfcf3cd97ea597f07a52f68c3b8ad53047601b.jpg",
                "rtime": 1679241600,
                "stime": 1679241600,
                "etime": 1680451199,
                "icon_state": 0,
                "act_tags": [
                    "文字视频",
                    "职场",
                    "唠嗑",
                    "周周有奖"
                ],
                "act_brief": "每周使用文字视频分享职场见闻，赢打卡奖金",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1007132,
                    "name": "每日职场唠嗑"
                },
                "tags": "",
                "rank": 13,
                "call_type": 2,
                "material": {
                    "material_type": 44,
                    "material_id": 3855323
                }
            },
            {
                "act_id": 559,
                "title": "我的心情日记",
                "act_img": "http://i0.hdslb.com/bfs/archive/78e94ae99402293792eed829be634a157a7d87e4.jpg",
                "rtime": 1679241600,
                "stime": 1679241600,
                "etime": 1680451199,
                "icon_state": 0,
                "act_tags": [
                    "文字视频",
                    "日常",
                    "日记",
                    "周周有奖"
                ],
                "act_brief": "每周使用文字视频记录心情，赢打卡奖金",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": null,
                "tags": "",
                "rank": 13,
                "call_type": 2,
                "material": {
                    "material_type": 44,
                    "material_id": 2014087
                }
            },
            {
                "act_id": 537,
                "title": "动物圈喊你瓜分现金啦",
                "act_img": "http://i0.hdslb.com/bfs/archive/0d035d1f701e3e1dcfb1154aec5afcb9e3dbc50d.png",
                "rtime": 1678032000,
                "stime": 1678032000,
                "etime": 1680451199,
                "icon_state": 1,
                "act_tags": [
                    "动物圈"
                ],
                "act_brief": "投稿动物圈分区，带#动物观察局#话题",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 3442,
                    "name": "动物观察局"
                },
                "tags": "",
                "rank": 13,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 555,
                "title": "每天唠一唠",
                "act_img": "http://i0.hdslb.com/bfs/archive/40e8f5e6ad846c0fba7e259317fcfe1c80e5cd1d.png",
                "rtime": 1678809600,
                "stime": 1678809600,
                "etime": 1680019199,
                "icon_state": 1,
                "act_tags": [
                    "拍摄特效",
                    "首投必得",
                    "唠嗑",
                    "聊天"
                ],
                "act_brief": "特效唠嗑赢奖金；特效首投前50名必得3元",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1014991,
                    "name": "唠嗑区新人来报道"
                },
                "tags": "",
                "rank": 13,
                "call_type": 2,
                "material": {
                    "material_type": 64,
                    "material_id": 4029567
                }
            },
            {
                "act_id": 540,
                "title": "影视整活大赏",
                "act_img": "http://i0.hdslb.com/bfs/archive/757c0dfbeede3b3387435cb45661f758dce27907.jpg",
                "rtime": 1678377600,
                "stime": 1678377600,
                "etime": 1683734399,
                "icon_state": 1,
                "act_tags": [
                    "整活",
                    "名场面"
                ],
                "act_brief": "带#整活#标签，投稿影视区",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 8939,
                    "name": "影视整活大赏"
                },
                "tags": "",
                "rank": 13,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 541,
                "title": "小剧场打卡挑战",
                "act_img": "http://i0.hdslb.com/bfs/archive/90aa932d035330b02cc31b7e185cb8de016bb4f7.jpg",
                "rtime": 1678636800,
                "stime": 1678636800,
                "etime": 1682870399,
                "icon_state": 1,
                "act_tags": [
                    "剧情",
                    "小剧场"
                ],
                "act_brief": "影视·小剧场分区指定话题下投稿",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1016630,
                    "name": "科普小剧场开课啦"
                },
                "tags": "",
                "rank": 13,
                "call_type": 1,
                "material": {
                    "material_type": 46,
                    "material_id": 4178502
                }
            },
            {
                "act_id": 560,
                "title": "每日学习打卡",
                "act_img": "http://i0.hdslb.com/bfs/archive/13cd83b1de3869043256f17bd518d6ab06e44b8b.jpg",
                "rtime": 1679241600,
                "stime": 1679241600,
                "etime": 1680451199,
                "icon_state": 0,
                "act_tags": [
                    "文字视频",
                    "学习"
                ],
                "act_brief": "使用文字视频分享学习打卡，赢打卡奖金",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": null,
                "tags": "",
                "rank": 13,
                "call_type": 2,
                "material": {
                    "material_type": 44,
                    "material_id": 3171420
                }
            },
            {
                "act_id": 564,
                "title": "转角遇到春天",
                "act_img": "http://i0.hdslb.com/bfs/archive/483293bbaaae43cf0da28b9d6af4dbe5dc630607.jpg",
                "rtime": 1679068800,
                "stime": 1679068800,
                "etime": 1682870399,
                "icon_state": 0,
                "act_tags": [
                    "记录春日",
                    "生活日常"
                ],
                "act_brief": "指定话题下投稿",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 11203,
                    "name": "转角遇到春天"
                },
                "tags": "",
                "rank": 13,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 519,
                "title": "每天安利我的爱豆",
                "act_img": "http://i0.hdslb.com/bfs/archive/c050bd194150a7d42d1d12ac65892c80806cab97.png",
                "rtime": 1677427200,
                "stime": 1677427200,
                "etime": 1682265599,
                "icon_state": 1,
                "act_tags": [
                    "爱豆安利",
                    "粉丝二创",
                    "追星现场"
                ],
                "act_brief": "投稿明星安利视频，瓜分万元奖金池！",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 173422,
                    "name": "春日娱人大联欢"
                },
                "tags": "",
                "rank": 12,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 550,
                "title": "普通人的美食日常打卡",
                "act_img": "http://i0.hdslb.com/bfs/archive/f96ba9ddb044c4627498b7f2c23f4a74e6a77d0b.jpg",
                "rtime": 1678636800,
                "stime": 1678636800,
                "etime": 1681055999,
                "icon_state": 1,
                "act_tags": [
                    "美食日常",
                    "普通人美食"
                ],
                "act_brief": "投稿美食内容必得奖金",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1011553,
                    "name": "普通人的美食日常"
                },
                "tags": "",
                "rank": 12,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 543,
                "title": "周末带孩去野打卡挑战",
                "act_img": "http://i0.hdslb.com/bfs/archive/071eb9bae8702727f6a24a646787281830ab7170.jpg",
                "rtime": 1678636800,
                "stime": 1678636800,
                "etime": 1681660799,
                "icon_state": 1,
                "act_tags": [
                    "春日出游",
                    "周周有奖"
                ],
                "act_brief": "生活-亲子分区指定话题下投稿",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1016826,
                    "name": "带孩子去野"
                },
                "tags": "",
                "rank": 12,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 542,
                "title": "每周亲子露营打卡挑战",
                "act_img": "http://i0.hdslb.com/bfs/archive/071eb9bae8702727f6a24a646787281830ab7170.jpg",
                "rtime": 1678636800,
                "stime": 1678636800,
                "etime": 1681660799,
                "icon_state": 1,
                "act_tags": [
                    "图转视频",
                    "周周有奖"
                ],
                "act_brief": "使用图转视频功能，在亲子区投稿话题",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1016826,
                    "name": "带孩子去野"
                },
                "tags": "",
                "rank": 12,
                "call_type": 2,
                "material": {
                    "material_type": -72,
                    "material_id": 0
                }
            },
            {
                "act_id": 552,
                "title": "一起来画画吧！2.0",
                "act_img": "http://i0.hdslb.com/bfs/archive/f160145b426d149a82448005eede6b5dbf35e639.jpg",
                "rtime": 1678636800,
                "stime": 1678636800,
                "etime": 1682265599,
                "icon_state": 1,
                "act_tags": [
                    "绘画",
                    "周周有奖"
                ],
                "act_brief": "每周投稿2天，可参与瓜分500元",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1004553,
                    "name": "一起来画画吧！"
                },
                "tags": "",
                "rank": 12,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 554,
                "title": "全民街舞打卡挑战3.0",
                "act_img": "http://i0.hdslb.com/bfs/archive/21a03c0eb0275f05c86ecc6e6aefabdfc6176991.jpg",
                "rtime": 1678636800,
                "stime": 1678636800,
                "etime": 1682265599,
                "icon_state": 1,
                "act_tags": [
                    "街舞",
                    "投稿必得奖"
                ],
                "act_brief": "投稿街舞相关内容必得奖金",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1015136,
                    "name": "全民街舞计划第三期"
                },
                "tags": "",
                "rank": 12,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 497,
                "title": "KPOP人招募计划打卡挑战",
                "act_img": "http://i0.hdslb.com/bfs/archive/092e3ab6b6630fc74d9beaeac414a620d24ed28c.jpg",
                "rtime": 1676390400,
                "stime": 1676390400,
                "etime": 1680883199,
                "icon_state": 1,
                "act_tags": [
                    "明星舞蹈",
                    "KPOP"
                ],
                "act_brief": "投稿KPOP相关内容必得奖金",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1007093,
                    "name": "KPOP人的随跳随拍"
                },
                "tags": "",
                "rank": 12,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 562,
                "title": "校园健身打卡",
                "act_img": "http://i0.hdslb.com/bfs/archive/aaf4cc13b0dec2c0d816169af1a222e304e73f57.jpg",
                "rtime": 1679241600,
                "stime": 1679241600,
                "etime": 1681660799,
                "icon_state": 0,
                "act_tags": [
                    "健身"
                ],
                "act_brief": "投稿健身内容必得奖金",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 64413,
                    "name": "学生党的自律时刻"
                },
                "tags": "",
                "rank": 12,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 535,
                "title": "一起打卡做手工",
                "act_img": "http://i0.hdslb.com/bfs/archive/0b05f5dddab19d5127239bfa3ca7201d3948ebd8.jpg",
                "rtime": 1678032000,
                "stime": 1678032000,
                "etime": 1680451199,
                "icon_state": 1,
                "act_tags": [
                    "手作分享",
                    "周周有奖"
                ],
                "act_brief": "生活-手工分区指定话题下投稿",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 3887,
                    "name": "一起做手工吧！"
                },
                "tags": "",
                "rank": 12,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 513,
                "title": "MV创作打卡挑战",
                "act_img": "http://i0.hdslb.com/bfs/archive/da98fc10b5a381049044994741ab2b4ebcf2765b.png",
                "rtime": 1677146400,
                "stime": 1677146400,
                "etime": 1680278399,
                "icon_state": 1,
                "act_tags": [
                    "MV",
                    "自制MV"
                ],
                "act_brief": "投稿音乐视频参与打卡",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 28739,
                    "name": "我的MV我做主"
                },
                "tags": "",
                "rank": 12,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 518,
                "title": "每日种草好剧好片",
                "act_img": "http://i0.hdslb.com/bfs/archive/53a9a84c33d33568e49ff1824a8c175b0eb94692.png",
                "rtime": 1677427200,
                "stime": 1677427200,
                "etime": 1682265599,
                "icon_state": 1,
                "act_tags": [
                    "好剧安利",
                    "影视剪辑",
                    "CP混剪"
                ],
                "act_brief": "每日安利好剧好片，瓜分万元奖金池！",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 173423,
                    "name": "春日迷影电影院"
                },
                "tags": "",
                "rank": 12,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 532,
                "title": "随心唠嗑，轻松拿奖！",
                "act_img": "http://i0.hdslb.com/bfs/archive/8ace072dc3f206152b37dc5e559210eb71f87185.jpg",
                "rtime": 1677772800,
                "stime": 1677772800,
                "etime": 1681660799,
                "icon_state": 1,
                "act_tags": [
                    "唠嗑",
                    "聊天"
                ],
                "act_brief": "点击打卡按钮，投递原创视频，即可参与",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1014941,
                    "name": "唠嗑区UP主集结令3"
                },
                "tags": "",
                "rank": 12,
                "call_type": 1,
                "material": {
                    "material_type": 64,
                    "material_id": 1830868
                }
            },
            {
                "act_id": 563,
                "title": "打卡记录春日碎片",
                "act_img": "http://i0.hdslb.com/bfs/archive/04fd292667848416a8d3968e7ca2b877060e4c02.png",
                "rtime": 1679241600,
                "stime": 1679241600,
                "etime": 1682870399,
                "icon_state": 0,
                "act_tags": [
                    "日常记录",
                    "奖池过万"
                ],
                "act_brief": "生活-日常分区指定话题下投稿",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1016572,
                    "name": "随手记录春日碎片"
                },
                "tags": "",
                "rank": 12,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 529,
                "title": "高能快闪动画团",
                "act_img": "http://i0.hdslb.com/bfs/archive/55686eced89f72b9061d9a2f9b37f72fd8c38fd6.jpg",
                "rtime": 1677772800,
                "stime": 1678032000,
                "etime": 1681055999,
                "icon_state": 1,
                "act_tags": [
                    "动画",
                    "竖屏",
                    "周周有奖"
                ],
                "act_brief": "投稿时长10~90s竖屏视频至动画区",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 298042,
                    "name": "高能快闪动画团"
                },
                "tags": "",
                "rank": 12,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 527,
                "title": "每日韩剧韩综安利",
                "act_img": "http://i0.hdslb.com/bfs/archive/ed7c1265f127a721c0c81088bb3f01945deee1a9.jpg",
                "rtime": 1677427200,
                "stime": 1677427200,
                "etime": 1683475199,
                "icon_state": 1,
                "act_tags": [
                    "好剧安利",
                    "影视剪辑",
                    "CP混剪"
                ],
                "act_brief": "每日韩剧韩综安利，万元奖金等你瓜分！",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1012381,
                    "name": "好看韩剧推荐"
                },
                "tags": "",
                "rank": 12,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 526,
                "title": "每日安利KPOP爱豆",
                "act_img": "http://i0.hdslb.com/bfs/archive/ed7c1265f127a721c0c81088bb3f01945deee1a9.jpg",
                "rtime": 1677427200,
                "stime": 1677427200,
                "etime": 1683475199,
                "icon_state": 1,
                "act_tags": [
                    "爱豆安利",
                    "粉丝二创",
                    "追星现场"
                ],
                "act_brief": "分享KPOP心动时刻，万元奖金等你瓜分！",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 53585,
                    "name": "万物皆可KPOP"
                },
                "tags": "",
                "rank": 12,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 548,
                "title": "每日追星唠嗑",
                "act_img": "http://i0.hdslb.com/bfs/archive/b27a68f7ee3cbc6fc90dbc739b851778451e9d01.jpg",
                "rtime": 1678636800,
                "stime": 1678636800,
                "etime": 1679846399,
                "icon_state": 1,
                "act_tags": [
                    "文字视频",
                    "追星",
                    "娱乐"
                ],
                "act_brief": "使用文字视频分享追星心情，打卡赢现金",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": null,
                "tags": "",
                "rank": 12,
                "call_type": 2,
                "material": {
                    "material_type": 44,
                    "material_id": 1205284
                }
            },
            {
                "act_id": 536,
                "title": "打卡春日农村生活",
                "act_img": "http://i0.hdslb.com/bfs/archive/3d86143f5467056228d9ae30bafc3b27a8726ac7.png",
                "rtime": 1678032000,
                "stime": 1678032000,
                "etime": 1681055999,
                "icon_state": 1,
                "act_tags": [
                    "三农",
                    "春日"
                ],
                "act_brief": "原创自制稿件带以下话题，投稿生活三农分区",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 43542,
                    "name": "三农繁星计划"
                },
                "tags": "",
                "rank": 12,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 521,
                "title": "这个春天吃什么",
                "act_img": "http://i0.hdslb.com/bfs/archive/85fc4b736ebaf3194893b14d2814054c69d96edf.png",
                "rtime": 1677427200,
                "stime": 1677427200,
                "etime": 1679846399,
                "icon_state": 1,
                "act_tags": [
                    "美食"
                ],
                "act_brief": "投稿美食内容必得奖金",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1009384,
                    "name": "阳春三月·美食烟火气"
                },
                "tags": "",
                "rank": 11,
                "call_type": 1,
                "material": {
                    "material_type": 46,
                    "material_id": 4022096
                }
            },
            {
                "act_id": 520,
                "title": "这个春天动起来\t",
                "act_img": "http://i0.hdslb.com/bfs/archive/4beaead9d325984e71a99b031e360c4097af813f.jpg",
                "rtime": 1677427200,
                "stime": 1677427200,
                "etime": 1679846399,
                "icon_state": 1,
                "act_tags": [
                    "运动健身",
                    "燃脂"
                ],
                "act_brief": "投稿健身内容必得奖金",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1011132,
                    "name": "春日·复苏燃脂季"
                },
                "tags": "",
                "rank": 11,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 524,
                "title": "2023UP！新学期！\t",
                "act_img": "http://i0.hdslb.com/bfs/archive/b81d97c5d03213cbea72a09cd5c2602c0a24dc58.jpg",
                "rtime": 1677427200,
                "stime": 1677427200,
                "etime": 1679846399,
                "icon_state": 1,
                "act_tags": [
                    "开学季",
                    "新学期"
                ],
                "act_brief": "视频参与打卡，使用指定话题投稿",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1011577,
                    "name": "浅浅唠下我的新学期生活"
                },
                "tags": "",
                "rank": 11,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 514,
                "title": "一分钟扬名B站",
                "act_img": "http://i0.hdslb.com/bfs/archive/903d7ddcd271bc61813f78ee93d6317d09d2be26.jpg",
                "rtime": 1677168000,
                "stime": 1677427200,
                "etime": 1682870399,
                "icon_state": 1,
                "act_tags": [
                    "周周有奖"
                ],
                "act_brief": "选择指定话题投稿",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 65056,
                    "name": "玩一种很新的东西"
                },
                "tags": "",
                "rank": 11,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 534,
                "title": "分享我的专业知识",
                "act_img": "http://i0.hdslb.com/bfs/archive/5cb7233458fc47767c776cf5be4bd517dd411a9e.jpg",
                "rtime": 1678032000,
                "stime": 1678032000,
                "etime": 1680451199,
                "icon_state": 1,
                "act_tags": [
                    "科学科普",
                    "周周有奖"
                ],
                "act_brief": "知识区-科学科普分区指定话题下投稿",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1013618,
                    "name": "分享我的专业知识"
                },
                "tags": "",
                "rank": 11,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 498,
                "title": "一起来聊聊",
                "act_img": "http://i0.hdslb.com/bfs/archive/073e7e54dd2e4b58b11332a8e450a5e7249fb32e.jpg",
                "rtime": 1676563200,
                "stime": 1676563200,
                "etime": 1680278399,
                "icon_state": 1,
                "act_tags": [
                    "限时有奖活动"
                ],
                "act_brief": "打卡投递原创视频，丰厚奖励等你拿",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1007415,
                    "name": "聊聊我向往的爱情"
                },
                "tags": "",
                "rank": 11,
                "call_type": 1,
                "material": {
                    "material_type": 64,
                    "material_id": 1830868
                }
            },
            {
                "act_id": 515,
                "title": "美好校园随手拍",
                "act_img": "http://i0.hdslb.com/bfs/archive/2cc6b1ed9fcaa800a7b6541ced638689b548dc52.png",
                "rtime": 1677168000,
                "stime": 1677168000,
                "etime": 1680278399,
                "icon_state": 1,
                "act_tags": [
                    "美好瞬间",
                    "校园",
                    "到梦空间",
                    "证书"
                ],
                "act_brief": "投稿指定话题#美好校园随手拍#参与投稿",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1011838,
                    "name": "美好校园随手拍"
                },
                "tags": "",
                "rank": 10,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 533,
                "title": "每周设计打卡",
                "act_img": "http://i0.hdslb.com/bfs/archive/2e498d0f870fafe99f6219786c3cde4f6bae184c.jpg",
                "rtime": 1678032000,
                "stime": 1678032000,
                "etime": 1681055999,
                "icon_state": 1,
                "act_tags": [
                    "设计分享",
                    "周周有奖"
                ],
                "act_brief": "知识区-设计·创意分区指定话题下投稿",
                "process": 0,
                "process_type": 0,
                "business": 3,
                "topic": {
                    "id": 1004060,
                    "name": "设计研习会"
                },
                "tags": "",
                "rank": 10,
                "call_type": 1,
                "material": null
            },
            {
                "act_id": 557,
                "title": "3月创作打卡",
                "act_img": "http://i0.hdslb.com/bfs/archive/433730b92935ee14f0b744c5bb9067591ee6dc27.png",
                "rtime": 1679241600,
                "stime": 1679241600,
                "etime": 1679846399,
                "icon_state": 0,
                "act_tags": [
                    ""
                ],
                "act_brief": "投稿瓜分万元奖池",
                "process": 0,
                "process_type": 0,
                "business": 4,
                "topic": null,
                "tags": "",
                "rank": 9,
                "call_type": 1,
                "material": null
            }
        ]
    }
}
    """


def search_channel(session: Session, cookies: RequestsCookieJar, keywords: str, filename: str) -> Response:
    """搜索推荐分区

    Args:
        session (Session): 可能需要代理
        cookies (RequestsCookieJar): 抓包获取
        keywords (str): 关键词
        filename (str): 服务器文件地址

    Returns:
        Response: 返回请求
            成功
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": [
        {
            "id": 183,
            "parent": 181,
            "parent_name": "影视",
            "name": "影视剪辑",
            "description": "对影视素材进行剪辑再创作的视频",
            "desc": "对影视素材进行剪辑再创作的视频",
            "intro_original": "建议在简介中添加正确的影视剧名、BGM等信息，以便在分区和搜索中得到更好的展示。CUT不属于自制内容，请选转载。",
            "intro_copy": "建议在简介中添加正确的影视剧名等信息。搬运转载内容必须添加原作者、原链接地址信息。",
            "notice": "【剪辑类型】+主要标题",
            "copy_right": 0,
            "show": true,
            "rank": 5,
            "max_video_count": 50,
            "request_id": ""
        },
        {
            "id": 21,
            "parent": 160,
            "parent_name": "生活",
            "name": "日常",
            "description": "一般日常向的生活类视频",
            "desc": "一般日常向的生活类视频",
            "intro_original": "能够选择自制的必须是up主个人或工作室自己制作剪辑的视频，除此之外的搬运视频字幕制作，对于视频进行加速、慢放等简易二次创作，在视频中添加前后贴片或者打水印等行为均不被认作自制",
            "intro_copy": "转载需写明请注明转载作品详细信息原作者、原标题及出处（需为该视频最原始出处，如所标注明显为非原始出处的话会被打回）",
            "notice": "",
            "copy_right": 0,
            "show": true,
            "rank": 4,
            "max_video_count": 50,
            "request_id": ""
        },
        {
            "id": 241,
            "parent": 5,
            "parent_name": "娱乐",
            "name": "娱乐杂谈",
            "description": "娱乐人物解读、娱乐热点点评、娱乐行业分析",
            "desc": "娱乐人物解读、娱乐热点点评、娱乐行业分析",
            "intro_original": "",
            "intro_copy": "",
            "notice": "清晰明了表明内容亮点的标题会更受观众欢迎哟",
            "copy_right": 0,
            "show": true,
            "rank": 9,
            "max_video_count": 50,
            "request_id": ""
        },
        {
            "id": 182,
            "parent": 181,
            "parent_name": "影视",
            "name": "影视杂谈",
            "description": "影视评论、解说、吐槽、科普、配音等",
            "desc": "影视评论、解说、吐槽、科普、配音等",
            "intro_original": "建议在简介和TAG中添加正确的影视剧名等信息，以便在分区和搜索中得到更好的展示。",
            "intro_copy": "建议在简介和TAG中添加正确的影视剧名等信息。\n搬运转载内容必须添加原作者、原链接地址信息。",
            "notice": "【UP主/节目名】+《影视剧名》（选填）+主要标题",
            "copy_right": 0,
            "show": true,
            "rank": 10,
            "max_video_count": 50,
            "request_id": ""
        },
        {
            "id": 138,
            "parent": 160,
            "parent_name": "生活",
            "name": "搞笑",
            "description": "搞笑挑战、剪辑、表演、配音以及各类日常沙雕视频",
            "desc": "搞笑挑战、剪辑、表演、配音以及各类日常沙雕视频",
            "intro_original": "能够选择自制的必须是up主个人或工作室自己制作剪辑的视频，除此之外的搬运视频字幕制作，对于视频进行加速、慢放等简易二次创作，在视频中添加前后贴片或者打水印等行为均不被认作自制",
            "intro_copy": "转载需写明请注明转载作品详细信息原作者、原标题及出处（需为该视频最原始出处，如所标注明显为非原始出处的话会被打回）",
            "notice": "",
            "copy_right": 0,
            "show": true,
            "rank": 30,
            "max_video_count": 50,
            "request_id": ""
        }
    ]
}
    """


def search_topic(session: Session, cookies: RequestsCookieJar, keywords: str, size: int = 20) -> Response:
    """搜索活动

    Args:
        session (Session): 可能需要代理
        cookies (RequestsCookieJar): 抓包获取
        keywords (str): 关键词
        size (int): 话题数量

    Returns:
        Response: 返回请求
            成功 
{
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "result": {
      "topics": [
        {
          "id": 1019782,
          "name": "我来红山看动物",
          "uname": "",
          "state": 0,
          "description": "邀请去过红山的朋友们来分享自己的见闻啦~好多小伙伴在等你的分享哦",
          "mission_id": 1358917,
          "activity_sign": "有奖活动",
          "act_protocol": "万元奖金火热招募动物观察员！"
        }
      ],
      "page_info": {
        "page_num": 0,
        "offset": 1,
        "has_more": true
      },
      "is_new_topic": true,
      "has_create_jurisdiction": false,
      "tips": "该话题是UP主活动相关话题，您在话题下的稿件信息可能会被提供给发起话题的UP主，并可能被UP主用于二次创作"
    }
  }
}
    """


def upload_cover(session: Session, cookies: RequestsCookieJar, cover_base64: bytes) -> Response:
    """上传封面

    Args:
        session (Session, optional): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取
        cover_base64 (bytes): base64格式的二进制流

    Returns:
        Response: 返回结果
            成功 {
                'code': 0, 
                'message': '0', 
                'ttl': 1, 
                'data': {
                    'url': 'https://archive.biliimg.com/bfs/archive/d0a0af83425ce3bf7d0e831c637b2733623120a7.jpg'
                }
            }
    """


def preupload_video(session: Session, cookies: RequestsCookieJar, name: str, size: int) -> Response:
    """预上传
        投稿视频的第 1 步

    Args:
        session (Session, optional): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取
        name (str): 文件名，可随意
        size (int): 文件大小

    Returns:
        Response: 返回结果
            成功 {
                "OK": 1,
                "auth": "ak=1494471752&cdn=%2F%2Fupos-cs-upcdnqn.bilivideo.com&os=upos&sign=0f117936cc26d371ef2b3faa20f3ff96&timestamp=1677145385.078&uid=1614308159&uip=113.87.32.73&uport=57104&use_dqp=0",
                "biz_id": 0,
                "chunk_retry": 10,
                "chunk_retry_delay": 3,
                "chunk_size": 10485760,
                "endpoint": "//upos-cs-upcdnqn.bilivideo.com",
                "endpoints": [
                    "//upos-cs-upcdnqn.bilivideo.com",
                    "//upos-cs-upcdnbda2.bilivideo.com"
                ],
                "expose_params": null,
                "put_query": "os=upos&profile=svf%2Fbup",
                "threads": 5,
                "timeout": 1200,
                "uip": "113.87.32.73",
                "upos_uri": "upos://svfboss/n230223qn3f298l71j5qgmhwaiq26e5z.zip"
            }
    """


def add_video(session: Session, cookies: RequestsCookieJar, filename: str, title: str, tid: int, tag: str, subtitle: int = 0, recreate: int = 0,
              up_close_danmu: bool = False, up_close_reply: bool = False, up_selection_reply: bool = False,
              lang: str = "zh-CN", desc: str = "", dynamic: str = "", open_elec: int = 1, cover: str = "",
              copyright: int = 1, source: str = "", no_reprint: int = 0, interactive: int = 0, topic_id: int = None) -> Response:
    """提交作品信息
        投稿视频的最后 1 步

    Args:
        session (Session, optional): Session实例对象
            可能存在一些需要代理的场景
        cookies (RequestsCookieJar): 从已登录的有效账号的 cookies 中获取
        filename (str): 视频网络地址
            注意不是本地地址,是已上传到哔哩哔哩服务器的网络地址,不包含前缀 upos://
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
        cover (str, optional): 封面名
            注意是上传到哔哩哔哩服务器的图片后返回的文件名,可以为空,b站会从视频里取一帧作为封面
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
        Response: 返回结果
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

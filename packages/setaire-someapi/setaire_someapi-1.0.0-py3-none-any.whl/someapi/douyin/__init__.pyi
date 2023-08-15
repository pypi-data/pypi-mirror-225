from requests import Session, Response
from requests.cookies import RequestsCookieJar


def get_user_info(session: Session, cookies: RequestsCookieJar, sec_user_id: str) -> Response:
    """获取用户基本信息

    Args:
        session (Session): 可能需要代理
        cookies (RequestsCookieJar): 抓包获取
        sec_user_id (str): 用户加密ID, 例如 MS4wLjABAAAAfbWhm2kBkPIi9XeDDGWtBO7Ns939XRTRvwCaEwNcda0
              https://www.douyin.com/user/MS4wLjABAAAAfbWhm2kBkPIi9XeDDGWtBO7Ns939XRTRvwCaEwNcda0?vid=7206519665021996303

    Returns:
        str: 返回请求
          成功
  {
    "extra": {
      "fatal_item_ids": [],
      "logid": "20230318211048117AB1532E03F78734D0",
      "now": 1679145048000
    },
    "log_pb": {
      "impr_id": "20230318211048117AB1532E03F78734D0"
    },
    "status_code": 0,
    "status_msg": null,
    "user": {
      "apple_account": 0,
      "avatar_168x168": {
        "height": 720,
        "uri": "aweme-avatar/tos-cn-i-0813_608ae285285f415fb4f3ac5b49a8ba1b",
        "url_list": [
          "https://p3-pc.douyinpic.com/img/aweme-avatar/tos-cn-i-0813_608ae285285f415fb4f3ac5b49a8ba1b~c5_168x168.jpeg?from=2956013662"
        ],
        "width": 720
      },
      "avatar_300x300": {
        "height": 720,
        "uri": "aweme-avatar/tos-cn-i-0813_608ae285285f415fb4f3ac5b49a8ba1b",
        "url_list": [
          "https://p3-pc.douyinpic.com/img/aweme-avatar/tos-cn-i-0813_608ae285285f415fb4f3ac5b49a8ba1b~c5_300x300.jpeg?from=2956013662"
        ],
        "width": 720
      },
      "avatar_larger": {
        "height": 720,
        "uri": "aweme-avatar/tos-cn-i-0813_608ae285285f415fb4f3ac5b49a8ba1b",
        "url_list": [
          "https://p3-pc.douyinpic.com/aweme/1080x1080/aweme-avatar/tos-cn-i-0813_608ae285285f415fb4f3ac5b49a8ba1b.jpeg?from=2956013662"
        ],
        "width": 720
      },
      "avatar_medium": {
        "height": 720,
        "uri": "aweme-avatar/tos-cn-i-0813_608ae285285f415fb4f3ac5b49a8ba1b",
        "url_list": [
          "https://p3-pc.douyinpic.com/aweme/720x720/aweme-avatar/tos-cn-i-0813_608ae285285f415fb4f3ac5b49a8ba1b.jpeg?from=2956013662"
        ],
        "width": 720
      },
      "avatar_thumb": {
        "height": 720,
        "uri": "aweme-avatar/tos-cn-i-0813_608ae285285f415fb4f3ac5b49a8ba1b",
        "url_list": [
          "https://p3-pc.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-i-0813_608ae285285f415fb4f3ac5b49a8ba1b.jpeg?from=2956013662"
        ],
        "width": 720
      },
      "aweme_count": 735,
      "aweme_count_correction_threshold": -1,
      "birthday_hide_level": 0,
      "can_set_item_cover": false,
      "can_show_group_card": 1,
      "card_entries": [
        {
          "goto_url": "aweme://im/FansGroup/GuestState",
          "icon_dark": {
            "uri": "https://p3.douyinpic.com/obj/im-resource/old_fans_group_manage_dark.png",
            "url_list": [
              "https://p3.douyinpic.com/obj/im-resource/old_fans_group_manage_dark.png",
              "https://p6.douyinpic.com/obj/im-resource/old_fans_group_manage_dark.png",
              "https://p9.douyinpic.com/obj/im-resource/old_fans_group_manage_dark.png"
            ]
          },
          "icon_light": {
            "uri": "https://p3.douyinpic.com/obj/im-resource/old_fans_group_manage_light.png",
            "url_list": [
              "https://p3.douyinpic.com/obj/im-resource/old_fans_group_manage_light.png",
              "https://p6.douyinpic.com/obj/im-resource/old_fans_group_manage_light.png",
              "https://p9.douyinpic.com/obj/im-resource/old_fans_group_manage_light.png"
            ]
          },
          "sub_title": "2个群聊",
          "title": "粉丝群",
          "type": 2
        }
      ],
      "city": "保山",
      "close_friend_type": 0,
      "commerce_info": {
        "challenge_list": null,
        "head_image_list": null,
        "offline_info_list": [],
        "smart_phone_list": null,
        "task_list": null
      },
      "commerce_user_info": {
        "ad_revenue_rits": null,
        "has_ads_entry": true,
        "show_star_atlas_cooperation": true,
        "star_atlas": 1
      },
      "commerce_user_level": 0,
      "country": "中国",
      "cover_and_head_image_info": {
        "cover_list": null,
        "profile_cover_list": [
          {
            "cover_url": {
              "uri": "tos-cn-i-0813/d9e4db169758414bb4659933f0295db7",
              "url_list": [
                "https://p6-pc-sign.douyinpic.com/obj/tos-cn-i-0813/d9e4db169758414bb4659933f0295db7?x-expires=1679317200&x-signature=r6EOZCguvRroKglstRQQd1DmFOY%3D&from=2480802190",
                "https://p3-pc-sign.douyinpic.com/obj/tos-cn-i-0813/d9e4db169758414bb4659933f0295db7?x-expires=1679317200&x-signature=k5s6GpTdl2sumwZNm6A1H5uvrvo%3D&from=2480802190",
                "https://p9-pc-sign.douyinpic.com/obj/tos-cn-i-0813/d9e4db169758414bb4659933f0295db7?x-expires=1679317200&x-signature=UCRXI4DbhwRX1u4Fk1Zl6ylQV4g%3D&from=2480802190"
              ]
            },
            "dark_cover_color": "#FF484f57",
            "light_cover_color": "#FF484f57"
          }
        ]
      },
      "cover_colour": "#03373EE5",
      "cover_url": [
        {
          "uri": "tos-cn-i-0813/d9e4db169758414bb4659933f0295db7",
          "url_list": [
            "https://p6-pc-sign.douyinpic.com/obj/tos-cn-i-0813/d9e4db169758414bb4659933f0295db7?x-expires=1679317200&x-signature=r6EOZCguvRroKglstRQQd1DmFOY%3D&from=2480802190",
            "https://p3-pc-sign.douyinpic.com/obj/tos-cn-i-0813/d9e4db169758414bb4659933f0295db7?x-expires=1679317200&x-signature=k5s6GpTdl2sumwZNm6A1H5uvrvo%3D&from=2480802190",
            "https://p9-pc-sign.douyinpic.com/obj/tos-cn-i-0813/d9e4db169758414bb4659933f0295db7?x-expires=1679317200&x-signature=UCRXI4DbhwRX1u4Fk1Zl6ylQV4g%3D&from=2480802190"
          ]
        },
        {
          "uri": "c8510002be9a3a61aad2",
          "url_list": [
            "https://p3-pc-sign.douyinpic.com/obj/c8510002be9a3a61aad2?x-expires=1679317200&x-signature=oC6NbgZhYJ8uta0T%2BGQzo68uo1c%3D&from=2480802190",
            "https://p9-pc-sign.douyinpic.com/obj/c8510002be9a3a61aad2?x-expires=1679317200&x-signature=et1dQgKTEnvhpidkGGFVSQ58eLM%3D&from=2480802190",
            "https://p6-pc-sign.douyinpic.com/obj/c8510002be9a3a61aad2?x-expires=1679317200&x-signature=HspXblF6yEnhtWQmBsddYCkEsgo%3D&from=2480802190"
          ]
        }
      ],
      "custom_verify": "",
      "district": null,
      "dongtai_count": 0,
      "dynamic_cover": {},
      "enable_wish": false,
      "enterprise_user_info": "{\"commerce_info\":{\"offline_info_list\":[],\"challenge_list\":null,\"task_list\":null,\"head_image_list\":null,\"smart_phone_list\":null},\"homepage_bottom_toast\":null,\"tab_ceiling_toast\":null,\"limiters\":null,\"attic_info\":null,\"profile_edit_button\":null,\"elite_center\":null,\"enterprise_card_visibility\":false,\"blue_label_edit_jump_url\":\"aweme://webview/?url=https%3A%2F%2Fapi.amemv.com%2Finsights%2Flite%2FcontactSetting%3Fhide_nav_bar%3D1%26title%3D%25E8%2581%2594%25E7%25B3%25BB%25E6%2596%25B9%25E5%25BC%258F%26enter_from%3Dcustomized_tab&hide_nav_bar=1&title=%E8%81%94%E7%B3%BB%E6%96%B9%E5%BC%8F&rn_schema=aweme%3A%2F%2Freactnative%2F%3Fchannel_name%3Drn_patch%26bundle_name%3Dbusiness%26module_name%3Dpage_e_lite_contactSetting%26force_h5%3D1%26hide_nav_bar%3D1%26bundle_url%3D%26title%3D%25E8%2581%2594%25E7%25B3%25BB%25E6%2596%25B9%25E5%25BC%258F%26enter_from%3Dcustomized_tab\"}",
      "enterprise_verify_reason": "",
      "favorite_permission": 1,
      "favoriting_count": 0,
      "follow_guide": true,
      "follow_status": 0,
      "follower_count": 324722,
      "follower_request_status": 0,
      "follower_status": 0,
      "following_count": 24,
      "forward_count": 0,
      "gender": 2,
      "has_e_account_role": false,
      "has_subscription": false,
      "im_primary_role_id": 8,
      "im_role_ids": [
        8,
        19,
        9
      ],
      "image_send_exempt": false,
      "ins_id": "",
      "ip_location": "IP属地：云南",
      "is_activity_user": false,
      "is_ban": false,
      "is_block": false,
      "is_blocked": false,
      "is_effect_artist": false,
      "is_gov_media_vip": false,
      "is_mix_user": false,
      "is_not_show": false,
      "is_series_user": false,
      "is_sharing_profile_user": 0,
      "is_star": false,
      "iso_country_code": "CN",
      "life_story_block": {
        "life_story_block": false
      },
      "live_commerce": false,
      "live_status": 0,
      "max_follower_count": 324722,
      "message_chat_entry": true,
      "mix_count": 0,
      "mplatform_followers_count": 324722,
      "new_friend_type": 0,
      "nickname": "𝒔𝒄𝒆𝒏𝒆𝒓𝒚",
      "original_musician": {
        "digg_count": 0,
        "music_count": 0,
        "music_used_count": 0
      },
      "pigeon_daren_status": "",
      "pigeon_daren_warn_tag": "",
      "profile_tab_type": 0,
      "province": "云南",
      "publish_landing_tab": 3,
      "r_fans_group_info": {},
      "recommend_reason_relation": "",
      "recommend_user_reason_source": 0,
      "risk_notice_text": "",
      "room_id": 0,
      "school_name": "",
      "sec_uid": "MS4wLjABAAAAP9IeZhDHS5xRBl20L8d-rDjNFokqnZTBVOw72A1GxzIIezcDJu6QzDCkNa3FsbY2",
      "secret": 0,
      "series_count": 0,
      "share_info": {
        "bool_persist": 1,
        "share_desc": "长按复制此条消息，打开抖音搜索，查看TA的更多作品。",
        "share_image_url": {
          "uri": "tos-cn-p-0015/ca890e4053734843aef7f4edc21bad3a_1679121846",
          "url_list": [
            "https://p3-pc-sign.douyinpic.com/obj/tos-cn-p-0015/ca890e4053734843aef7f4edc21bad3a_1679121846?x-expires=1679317200&x-signature=4%2FqzMLTlHfPkkQJDc9AqFgFbpIw%3D&from=2480802190",
            "https://p6-pc-sign.douyinpic.com/obj/tos-cn-p-0015/ca890e4053734843aef7f4edc21bad3a_1679121846?x-expires=1679317200&x-signature=DvQSaCSmSKmJohcabXEPT5119%2Bc%3D&from=2480802190",
            "https://p9-pc-sign.douyinpic.com/obj/tos-cn-p-0015/ca890e4053734843aef7f4edc21bad3a_1679121846?x-expires=1679317200&x-signature=GneOUq0sdu3WWjw0xXiJpsW9MoI%3D&from=2480802190"
          ]
        },
        "share_qrcode_url": {
          "uri": "31b040012fd8708ffa3b8",
          "url_list": [
            "https://p11.douyinpic.com/obj/31b040012fd8708ffa3b8",
            "https://p26.douyinpic.com/obj/31b040012fd8708ffa3b8",
            "https://p3.douyinpic.com/obj/31b040012fd8708ffa3b8"
          ]
        },
        "share_title": "快来加入抖音，让你发现最有趣的我！",
        "share_url": "www.iesdouyin.com/share/user/MS4wLjABAAAAP9IeZhDHS5xRBl20L8d-rDjNFokqnZTBVOw72A1GxzIIezcDJu6QzDCkNa3FsbY2?did=MS4wLjABAAAAUNvaBVZEBfBjOoFxFxYB0k34e1mqofJhzu6esByOrelbwsCdIScOIS-EDYvaLAMA&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ&with_sec_did=1&sec_uid=MS4wLjABAAAAP9IeZhDHS5xRBl20L8d-rDjNFokqnZTBVOw72A1GxzIIezcDJu6QzDCkNa3FsbY2&from_ssr=1&u_code=33j71mhi576g",
        "share_weibo_desc": "长按复制此条消息，打开抖音搜索，查看TA的更多作品。"
      },
      "short_id": "0",
      "show_favorite_list": false,
      "show_subscription": false,
      "signature": "小动物让生活更温馨-治愈",
      "signature_display_lines": 0,
      "signature_language": "un",
      "special_follow_status": 0,
      "sync_to_toutiao": 0,
      "tab_settings": {
        "private_tab": {
          "private_tab_style": 1,
          "show_private_tab": false
        }
      },
      "total_favorited": 14051911,
      "total_favorited_correction_threshold": -1,
      "twitter_id": "",
      "twitter_name": "",
      "uid": "4495236625081352",
      "unique_id": "Ane08",
      "urge_detail": {
        "user_urged": 0
      },
      "user_age": 20,
      "user_not_see": 0,
      "user_not_show": 1,
      "verification_type": 0,
      "video_cover": {},
      "video_icon": {
        "height": 720,
        "uri": "",
        "url_list": [],
        "width": 720
      },
      "watch_status": false,
      "white_cover_url": [
        {
          "uri": "tos-cn-i-0813/d9e4db169758414bb4659933f0295db7",
          "url_list": [
            "https://p6-pc-sign.douyinpic.com/obj/tos-cn-i-0813/d9e4db169758414bb4659933f0295db7?x-expires=1679317200&x-signature=r6EOZCguvRroKglstRQQd1DmFOY%3D&from=2480802190",
            "https://p3-pc-sign.douyinpic.com/obj/tos-cn-i-0813/d9e4db169758414bb4659933f0295db7?x-expires=1679317200&x-signature=k5s6GpTdl2sumwZNm6A1H5uvrvo%3D&from=2480802190",
            "https://p9-pc-sign.douyinpic.com/obj/tos-cn-i-0813/d9e4db169758414bb4659933f0295db7?x-expires=1679317200&x-signature=UCRXI4DbhwRX1u4Fk1Zl6ylQV4g%3D&from=2480802190"
          ]
        },
        {
          "uri": "318f1000413827e122102",
          "url_list": [
            "https://p3-pc-sign.douyinpic.com/obj/318f1000413827e122102?x-expires=1679317200&x-signature=P%2Fw26JBpRveMxzR%2B3wOaTdlnctk%3D&from=2480802190",
            "https://p9-pc-sign.douyinpic.com/obj/318f1000413827e122102?x-expires=1679317200&x-signature=vkRrttT6AUKbd6mGTTZHh4XuePU%3D&from=2480802190",
            "https://p6-pc-sign.douyinpic.com/obj/318f1000413827e122102?x-expires=1679317200&x-signature=91hRuut8KqxzG5Q%2B2xynW3vrA%2BE%3D&from=2480802190"
          ]
        }
      ],
      "with_commerce_enterprise_tab_entry": false,
      "with_commerce_entry": false,
      "with_fusion_shop_entry": false,
      "with_new_goods": false,
      "youtube_channel_id": "",
      "youtube_channel_title": ""
    }
  }
    """


def get_video_playurl(session: Session, cookies: RequestsCookieJar, aweme_id: str) -> str:
    """获取无水印视频地址

    Args:
        session (Session): 可能需要代理
        cookies (RequestsCookieJar): 抓包获取
        aweme_id (str): 视频ID, 例如 7188795449468259623

              ```https://www.douyin.com/video/7188795449468259623```

    Raise:
        InvalidCookiesError: 当解析地址失败时抛出该异常
        
    Returns:
        str: 视频地址
            ```https://v26-web.douyinvod.com/cb4056d8c8402a175d23ce3d9891ddec/64153ed0/video/tos/cn/tos-cn-ve-15/osIDUQAEe0b4Apzx4fjntnrGJ2LAkhDgDhdYB2/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1944&bt=1944&cs=0&ds=4&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLfr2MZU_4qu.beJNv7T&mime_type=video_mp4&qs=0&rc=NDs5ZmQzZjU7aDY5Ozc8Z0BpajpoNGU6Zmx1aTMzNGkzM0A1YzYvLzVjNTAxMS8tNC41YSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=2023031811320366684E9BB4FC594E1BFD&btag=8000```
    """


def get_user_videos(session: Session, cookies: RequestsCookieJar, sec_user_id: str, size: int = 10) -> Response:
    """获取用户视频

    Args:
        session (Session): 可能需要代理
        cookies (RequestsCookieJar): 抓包获取
        sec_user_id (str): 用户加密ID, 例如 MS4wLjABAAAAfbWhm2kBkPIi9XeDDGWtBO7Ns939XRTRvwCaEwNcda0
            https://www.douyin.com/user/MS4wLjABAAAAfbWhm2kBkPIi9XeDDGWtBO7Ns939XRTRvwCaEwNcda0?vid=7206519665021996303
        size (int, optional): 视频数量, 需要注意如果该用户置顶了3个视频, 返回的实际数量是 size + 3 个

    Returns:
        Response: 返回请求
        成功 
{
  "aweme_list": [
    {
      "anchors": null,
      "authentication_token": "MS4wLjAAAAAAvNBVdz0DbvuaNLlGL4opV0jeKDDrGNdRzkPWNmpYVrTd2PEQGV-6cA8yNG8CW6L7NsJLlz1pRVqC7KvyFjKcbQpuA8HrEHZqlx0YEQ0XONlL41QjN_TYsu-dHGiPXLkCQAbYlRZULljvU8VZ6WOQBHjDTE3pD4R-uIP-zG5i2RpczO-Op_ATuGA4r9vKL8q60RCeah6LAU71Xn7AzhPh_zdeuautKZltH3aK_qFFo8A",
      "author": {
        "accept_private_policy": false,
        "account_region": "",
        "apple_account": 0,
        "avatar_thumb": {
          "height": 720,
          "uri": "100x100/aweme-avatar/tos-cn-i-0813_596fa8b236e949b7a185134ebd0312bb",
          "url_list": [
            "https://p3-pc.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-i-0813_596fa8b236e949b7a185134ebd0312bb.jpeg?from=116350172"
          ],
          "width": 720
        },
        "avatar_uri": "aweme-avatar/tos-cn-i-0813_596fa8b236e949b7a185134ebd0312bb",
        "aweme_control": {
          "can_comment": true,
          "can_forward": true,
          "can_share": true,
          "can_show_comment": true
        },
        "aweme_count": 85,
        "aweme_hotsoon_auth": 1,
        "aweme_hotsoon_auth_relation": 1,
        "ban_user_functions": [],
        "bind_phone": "",
        "can_set_geofencing": null,
        "card_entries": null,
        "card_entries_not_display": null,
        "card_sort_priority": null,
        "cf_list": null,
        "cha_list": null,
        "close_friend_type": 0,
        "constellation": 10,
        "contacts_status": 2,
        "contrail_list": null,
        "cover_url": [
          {
            "height": 720,
            "uri": "c8510002be9a3a61aad2",
            "url_list": [
              "https://p6-pc-sign.douyinpic.com/obj/c8510002be9a3a61aad2?x-expires=1680192000&x-signature=tVjPwcMavp1i%2FnIF18zk2LgXuK4%3D&from=116350172",
              "https://p9-pc-sign.douyinpic.com/obj/c8510002be9a3a61aad2?x-expires=1680192000&x-signature=bA9aTYTRYV7%2FNkbSXOQqzpG77lw%3D&from=116350172",
              "https://p3-pc-sign.douyinpic.com/obj/c8510002be9a3a61aad2?x-expires=1680192000&x-signature=5gs4K3OYHDtp1qgC9gjnh7b2gzI%3D&from=116350172"
            ],
            "width": 720
          }
        ],
        "create_time": 0,
        "custom_verify": "",
        "cv_level": "",
        "data_label_list": null,
        "display_info": null,
        "download_prompt_ts": 0,
        "enable_nearby_visible": false,
        "endorsement_info_list": null,
        "enterprise_verify_reason": "",
        "favoriting_count": 622,
        "fb_expire_time": 0,
        "follow_status": 1,
        "follower_count": 39576,
        "follower_list_secondary_information_struct": null,
        "follower_request_status": 0,
        "follower_status": 0,
        "following_count": 11,
        "geofencing": [],
        "google_account": "",
        "has_email": false,
        "has_facebook_token": false,
        "has_insights": false,
        "has_orders": false,
        "has_twitter_token": false,
        "has_youtube_token": false,
        "hide_search": true,
        "homepage_bottom_toast": null,
        "im_role_ids": null,
        "ins_id": "",
        "interest_tags": null,
        "is_binded_weibo": false,
        "is_blocked_v2": false,
        "is_blocking_v2": false,
        "is_cf": 0,
        "is_not_show": false,
        "is_phone_binded": false,
        "item_list": null,
        "ky_only_predict": 0,
        "link_item_list": null,
        "live_agreement": 0,
        "live_agreement_time": 0,
        "live_commerce": false,
        "live_verify": 0,
        "max_follower_count": 0,
        "need_points": null,
        "need_recommend": 0,
        "neiguang_shield": 0,
        "new_story_cover": null,
        "nickname": "𝐻𝑒𝑎𝑙𝑒𝑟★",
        "not_seen_item_id_list": null,
        "not_seen_item_id_list_v2": null,
        "offline_info_list": null,
        "personal_tag_list": null,
        "platform_sync_info": null,
        "prevent_download": false,
        "react_setting": 0,
        "reflow_page_gid": 0,
        "reflow_page_uid": 0,
        "risk_notice_text": "",
        "school_category": 1,
        "school_id": "6601125882050398212",
        "search_impr": {
          "entity_id": "3734384759022542"
        },
        "sec_uid": "MS4wLjABAAAAXXV_8qOG_ruJxLIoqDrpiVF32brHfaCEKxl06poCsxKjzCJt7O7XCDmFqTmC0UWq",
        "secret": 0,
        "share_info": {
          "share_desc": "",
          "share_desc_info": "",
          "share_qrcode_url": {
            "height": 720,
            "uri": "319580021a41c02b569fe",
            "url_list": [
              "https://p9-pc-sign.douyinpic.com/obj/319580021a41c02b569fe?x-expires=1679004000&x-signature=2NkG6KIAFaM2z60GRQq5koDgbU8%3D&from=116350172",
              "https://p6-pc-sign.douyinpic.com/obj/319580021a41c02b569fe?x-expires=1679004000&x-signature=3sAWLjm%2FvFRzWgP97CTexKejWOE%3D&from=116350172",
              "https://p3-pc-sign.douyinpic.com/obj/319580021a41c02b569fe?x-expires=1679004000&x-signature=QiwIb02LXOfkopATefTok9IF4Cg%3D&from=116350172"
            ],
            "width": 720
          },
          "share_title": "",
          "share_title_myself": "",
          "share_title_other": "",
          "share_url": "",
          "share_weibo_desc": ""
        },
        "share_qrcode_uri": "319580021a41c02b569fe",
        "shield_comment_notice": 0,
        "shield_digg_notice": 0,
        "shield_follow_notice": 0,
        "short_id": "38442767301",
        "show_image_bubble": false,
        "show_nearby_active": false,
        "signature": "好看的皮囊千篇一律  有趣的灵魂万里挑一\n日常更新搞怪治愈萌宠  谢谢您的关注🙈\n学习/合作:Sun10151120",
        "signature_display_lines": 0,
        "signature_extra": null,
        "special_follow_status": 0,
        "special_lock": 1,
        "special_people_labels": null,
        "status": 1,
        "story_open": false,
        "text_extra": null,
        "total_favorited": 2700738,
        "tw_expire_time": 0,
        "twitter_id": "",
        "twitter_name": "",
        "type_label": null,
        "uid": "3734384759022542",
        "unique_id": "ztxmc",
        "unique_id_modify_time": 1678982440,
        "user_age": -1,
        "user_canceled": false,
        "user_mode": 0,
        "user_not_see": 0,
        "user_not_show": 1,
        "user_period": 0,
        "user_permissions": null,
        "user_rate": 1,
        "user_tags": null,
        "verification_type": 1,
        "weibo_name": "",
        "weibo_schema": "",
        "weibo_url": "",
        "weibo_verify": "",
        "white_cover_url": null,
        "with_dou_entry": false,
        "with_fusion_shop_entry": false,
        "with_shop_entry": false,
        "youtube_channel_id": "",
        "youtube_channel_title": "",
        "youtube_expire_time": 0
      },
      "author_mask_tag": 0,
      "author_user_id": 3734384759022542,
      "aweme_control": {
        "can_comment": true,
        "can_forward": true,
        "can_share": true,
        "can_show_comment": true
      },
      "aweme_id": "7188795449468259623",
      "aweme_type": 0,
      "book_bar": {},
      "challenge_position": null,
      "chapter_list": null,
      "collect_stat": 0,
      "collection_corner_mark": 0,
      "comment_gid": 7188795449468259623,
      "comment_list": null,
      "comment_permission_info": {
        "can_comment": true,
        "comment_permission_status": 0,
        "item_detail_entry": false,
        "press_entry": false,
        "toast_guide": false
      },
      "commerce_config_data": null,
      "common_bar_info": "[]",
      "component_info_v2": "{\"desc_lines_limit\":0,\"hide_marquee\":false}",
      "cover_labels": null,
      "create_time": 1673771886,
      "desc": "艾特身边最像它的人来看",
      "digg_lottie": {
        "can_bomb": 0,
        "lottie_id": ""
      },
      "disable_relation_bar": 0,
      "dislike_dimension_list": null,
      "duet_aggregate_in_music_tab": false,
      "duration": 13095,
      "geofencing": [],
      "geofencing_regions": null,
      "group_id": "7186887960493591865",
      "guide_btn_type": 0,
      "hybrid_label": null,
      "image_album_music_info": {
        "begin_time": 0,
        "end_time": 12933,
        "volume": 158
      },
      "image_comment": {},
      "image_infos": null,
      "image_list": null,
      "images": null,
      "img_bitrate": null,
      "impression_data": {
        "group_id_list_a": [
          7188067834398887229
        ],
        "group_id_list_b": [
          7188067834398887229
        ],
        "group_id_list_c": null,
        "similar_id_list_a": null,
        "similar_id_list_b": [
          7188795449468259623
        ]
      },
      "interaction_stickers": null,
      "is_collects_selected": 0,
      "is_duet_sing": false,
      "is_image_beat": false,
      "is_life_item": false,
      "is_share_post": false,
      "is_story": 0,
      "is_top": 0,
      "item_warn_notification": {
        "content": "",
        "show": false,
        "type": 0
      },
      "label_top_text": null,
      "long_video": null,
      "music": {
        "album": "",
        "artist_user_infos": null,
        "artists": [],
        "audition_duration": 28,
        "author": "静萱🧚",
        "author_deleted": false,
        "author_position": null,
        "author_status": 1,
        "avatar_large": {
          "height": 720,
          "uri": "1080x1080/aweme-avatar/tos-cn-avt-0015_5ded6f72f88ed7d27314a6b4b5d09f44",
          "url_list": [
            "https://p3-pc.douyinpic.com/aweme/1080x1080/aweme-avatar/tos-cn-avt-0015_5ded6f72f88ed7d27314a6b4b5d09f44.jpeg?from=116350172"
          ],
          "width": 720
        },
        "avatar_medium": {
          "height": 720,
          "uri": "720x720/aweme-avatar/tos-cn-avt-0015_5ded6f72f88ed7d27314a6b4b5d09f44",
          "url_list": [
            "https://p3-pc.douyinpic.com/aweme/720x720/aweme-avatar/tos-cn-avt-0015_5ded6f72f88ed7d27314a6b4b5d09f44.jpeg?from=116350172"
          ],
          "width": 720
        },
        "avatar_thumb": {
          "height": 720,
          "uri": "100x100/aweme-avatar/tos-cn-avt-0015_5ded6f72f88ed7d27314a6b4b5d09f44",
          "url_list": [
            "https://p3-pc.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-avt-0015_5ded6f72f88ed7d27314a6b4b5d09f44.jpeg?from=116350172"
          ],
          "width": 720
        },
        "binded_challenge_id": 0,
        "can_background_play": true,
        "collect_stat": 0,
        "cover_hd": {
          "height": 720,
          "uri": "1080x1080/aweme-avatar/tos-cn-avt-0015_5ded6f72f88ed7d27314a6b4b5d09f44",
          "url_list": [
            "https://p3-pc.douyinpic.com/aweme/1080x1080/aweme-avatar/tos-cn-avt-0015_5ded6f72f88ed7d27314a6b4b5d09f44.jpeg?from=116350172"
          ],
          "width": 720
        },
        "cover_large": {
          "height": 720,
          "uri": "1080x1080/aweme-avatar/tos-cn-avt-0015_5ded6f72f88ed7d27314a6b4b5d09f44",
          "url_list": [
            "https://p3-pc.douyinpic.com/aweme/1080x1080/aweme-avatar/tos-cn-avt-0015_5ded6f72f88ed7d27314a6b4b5d09f44.jpeg?from=116350172"
          ],
          "width": 720
        },
        "cover_medium": {
          "height": 720,
          "uri": "720x720/aweme-avatar/tos-cn-avt-0015_5ded6f72f88ed7d27314a6b4b5d09f44",
          "url_list": [
            "https://p3-pc.douyinpic.com/aweme/720x720/aweme-avatar/tos-cn-avt-0015_5ded6f72f88ed7d27314a6b4b5d09f44.jpeg?from=116350172"
          ],
          "width": 720
        },
        "cover_thumb": {
          "height": 720,
          "uri": "100x100/aweme-avatar/tos-cn-avt-0015_5ded6f72f88ed7d27314a6b4b5d09f44",
          "url_list": [
            "https://p3-pc.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-avt-0015_5ded6f72f88ed7d27314a6b4b5d09f44.jpeg?from=116350172"
          ],
          "width": 720
        },
        "dmv_auto_show": false,
        "dsp_status": 10,
        "duration": 28,
        "end_time": 0,
        "external_song_info": [],
        "extra": "{\"is_aed_music\":1,\"with_aed_model\":1,\"dsp_switch\":0,\"has_edited\":0,\"douyin_beats_info\":{},\"cover_colors\":null,\"extract_item_id\":6828761341872934148,\"beats\":{\"audio_effect_onset\":\"https://sf6-cdn-tos.douyinstatic.com/obj/ies-music/strong_beat/v3/1667220971260935\",\"beats_tracker\":\"https://sf3-cdn-tos.douyinstatic.com/obj/ies-music/strong_beat/v3/1667220976317447\",\"energy_trace\":\"https://sf86-cdn-tos.douyinstatic.com/obj/ies-music/strong_beat/v3/1667220971233294\",\"merged_beats\":\"https://sf6-cdn-tos.douyinstatic.com/obj/ies-music/strong_beat/v3/1667220976356365\"},\"is_subsidy_exp\":false,\"is_red\":0,\"music_label_id\":null,\"reviewed\":0,\"review_unshelve_reason\":0,\"schedule_search_time\":0,\"hotsoon_review_time\":-1,\"music_tagging\":{\"Languages\":[\"non_vocal\"],\"Moods\":[\"Dynamic\"],\"Genres\":[\"DJ\",\"Others\"],\"Themes\":[\"Low\",\"Danceable\"],\"AEDs\":[\"Vocal\"],\"SingingVersions\":null,\"Instruments\":null},\"aggregate_exempt_conf\":[]}",
        "id": 6828761557481065230,
        "id_str": "6828761557481065230",
        "is_audio_url_with_cookie": false,
        "is_commerce_music": false,
        "is_del_video": false,
        "is_matched_metadata": false,
        "is_original": false,
        "is_original_sound": true,
        "is_pgc": false,
        "is_restricted": false,
        "is_video_self_see": false,
        "luna_info": {
          "has_copyright": false,
          "is_luna_user": false
        },
        "lyric_short_position": null,
        "matched_pgc_sound": {
          "author": "黑猫警长Giao哥&拼音师",
          "cover_medium": {
            "height": 720,
            "uri": "tos-cn-v-2774c002/6f11b3c363ea436f838cb72abc031e8f",
            "url_list": [
              "https://p6.douyinpic.com/aweme/200x200/tos-cn-v-2774c002/6f11b3c363ea436f838cb72abc031e8f.jpeg",
              "https://p26.douyinpic.com/aweme/200x200/tos-cn-v-2774c002/6f11b3c363ea436f838cb72abc031e8f.jpeg",
              "https://p11.douyinpic.com/aweme/200x200/tos-cn-v-2774c002/6f11b3c363ea436f838cb72abc031e8f.jpeg"
            ],
            "width": 720
          },
          "mixed_author": "",
          "mixed_title": "",
          "title": "一起giao"
        },
        "mid": "6828761557481065230",
        "music_chart_ranks": null,
        "music_collect_count": 0,
        "music_cover_atmosphere_color_value": "",
        "music_status": 1,
        "musician_user_infos": null,
        "mute_share": false,
        "offline_desc": "",
        "owner_handle": "159880167",
        "owner_id": "80833885391",
        "owner_nickname": "静萱🧚",
        "pgc_music_type": 2,
        "play_url": {
          "height": 720,
          "uri": "https://sf86-cdn-tos.douyinstatic.com/obj/ies-music/217f28b3b542c259a23ab23e3f8e1948.mp3",
          "url_key": "6828761557481065230",
          "url_list": [
            "https://sf86-cdn-tos.douyinstatic.com/obj/ies-music/217f28b3b542c259a23ab23e3f8e1948.mp3",
            "https://sf3-cdn-tos.douyinstatic.com/obj/ies-music/217f28b3b542c259a23ab23e3f8e1948.mp3"
          ],
          "width": 720
        },
        "position": null,
        "prevent_download": false,
        "prevent_item_download_status": 0,
        "preview_end_time": 0,
        "preview_start_time": 0,
        "reason_type": 0,
        "redirect": false,
        "schema_url": "",
        "search_impr": {
          "entity_id": "6828761557481065230"
        },
        "sec_uid": "MS4wLjABAAAAusoqPVGicitwbtOCHzBZodLencBBxDDjRxd2bW-ZhXw",
        "shoot_duration": 28,
        "song": {
          "artists": null,
          "chorus_v3_infos": null,
          "id": 7171455299630172192,
          "id_str": "7171455299630172192"
        },
        "source_platform": 23,
        "start_time": 0,
        "status": 1,
        "strong_beat_url": {
          "height": 720,
          "uri": "https://sf6-cdn-tos.douyinstatic.com/obj/ies-music/pattern/a5747cf953238427171e02e8262fd1d6.json",
          "url_list": [
            "https://sf6-cdn-tos.douyinstatic.com/obj/ies-music/pattern/a5747cf953238427171e02e8262fd1d6.json",
            "https://sf86-cdn-tos.douyinstatic.com/obj/ies-music/pattern/a5747cf953238427171e02e8262fd1d6.json"
          ],
          "width": 720
        },
        "tag_list": null,
        "title": "@静萱🧚创作的原声",
        "unshelve_countries": null,
        "user_count": 0,
        "video_duration": 28
      },
      "nickname_position": null,
      "origin_comment_ids": null,
      "origin_text_extra": [],
      "original_images": null,
      "packed_clips": null,
      "photo_search_entrance": {
        "ecom_type": 0
      },
      "position": null,
      "prevent_download": false,
      "preview_title": "艾特身边最像它的人来看",
      "preview_video_status": 1,
      "promotions": [],
      "ref_tts_id_list": null,
      "ref_voice_modify_id_list": null,
      "region": "CN",
      "relation_labels": null,
      "report_action": false,
      "search_impr": {
        "entity_id": "7188795449468259623",
        "entity_type": "GENERAL"
      },
      "seo_info": {},
      "series_paid_info": {
        "item_price": 0,
        "series_paid_status": 0
      },
      "share_info": {
        "share_link_desc": "0.20 ZzT:/ 艾特身边最像它的人来看  %s 复制此链接，打开Dou音搜索，直接观看视频！",
        "share_url": "https://www.iesdouyin.com/share/video/7188795449468259623/?region=CN&mid=6828761557481065230&u_code=33j71mhi576g&did=MS4wLjABAAAAUNvaBVZEBfBjOoFxFxYB0k34e1mqofJhzu6esByOrelbwsCdIScOIS-EDYvaLAMA&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ&with_sec_did=1&titleType=title&from_ssr=1"
      },
      "share_url": "https://www.iesdouyin.com/share/video/7188795449468259623/?region=CN&mid=6828761557481065230&u_code=33j71mhi576g&did=MS4wLjABAAAAUNvaBVZEBfBjOoFxFxYB0k34e1mqofJhzu6esByOrelbwsCdIScOIS-EDYvaLAMA&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ&with_sec_did=1&titleType=title&from_ssr=1",
      "should_open_ad_report": false,
      "show_follow_button": {},
      "social_tag_list": null,
      "standard_bar_info_list": null,
      "statistics": {
        "admire_count": 0,
        "aweme_id": "7188795449468259623",
        "collect_count": 2611,
        "comment_count": 18165,
        "digg_count": 48559,
        "play_count": 0,
        "share_count": 41916
      },
      "status": {
        "allow_share": true,
        "aweme_id": "7188795449468259623",
        "in_reviewing": false,
        "is_delete": false,
        "is_prohibited": false,
        "listen_video_status": 0,
        "part_see": 0,
        "private_status": 0,
        "review_result": {
          "review_status": 0
        }
      },
      "suggest_words": {
        "suggest_words": [
          {
            "extra_info": "{}",
            "hint_text": "气泡框词",
            "icon_url": "",
            "scene": "search_icon_rec",
            "words": [
              {
                "info": "{\"word_suffix\":\"\",\"recommend_word_type\":\"\",\"history_word_tag\":\"\",\"qrec_for_search\":\"{\\\"video_ecom\\\":\\\"0\\\",\\\"query_ecom\\\":\\\"0\\\",\\\"is_purchase\\\":\\\"0\\\"}\"}",
                "word": "海狗",
                "word_id": "6542732805305013507"
              }
            ]
          },
          {
            "extra_info": "{}",
            "hint_text": "",
            "icon_url": "",
            "scene": "detail_inbox_rex",
            "words": [
              {
                "info": "{\"word_suffix\":\"\",\"recommend_word_type\":\"\",\"history_word_tag\":\"\",\"qrec_for_search\":\"{\\\"video_ecom\\\":\\\"0\\\",\\\"query_ecom\\\":\\\"0\\\",\\\"is_purchase\\\":\\\"0\\\"}\"}",
                "word": "金毛扭腰摇尾巴",
                "word_id": "7106225246722233612"
              }
            ]
          },
          {
            "extra_info": "{}",
            "hint_text": "大家都在搜：",
            "icon_url": "",
            "scene": "comment_top_rec",
            "words": [
              {
                "info": "{\"word_suffix\":\"\",\"recommend_word_type\":\"\",\"history_word_tag\":\"\",\"qrec_for_search\":\"{\\\"video_ecom\\\":\\\"0\\\",\\\"query_ecom\\\":\\\"0\\\",\\\"is_purchase\\\":\\\"0\\\"}\"}",
                "word": "金毛扭腰摇尾巴",
                "word_id": "7106225246722233612"
              }
            ]
          }
        ]
      },
      "text_extra": [],
      "tts_id_list": null,
      "uniqid_position": null,
      "user_digged": 0,
      "user_recommend_status": 0,
      "video": {
        "animated_cover": {
          "uri": "tos-cn-p-0015/51c94ceed2e244af8c4b1f06ad3cf332_1673771890",
          "url_list": [
            "https://p6-pc-sign.douyinpic.com/obj/tos-cn-p-0015/51c94ceed2e244af8c4b1f06ad3cf332_1673771890?x-expires=1680192000&x-signature=qM5DwVjApvmfRelRWFXtXSY8m%2BM%3D&from=3213915784_large",
            "https://p9-pc-sign.douyinpic.com/obj/tos-cn-p-0015/51c94ceed2e244af8c4b1f06ad3cf332_1673771890?x-expires=1680192000&x-signature=UAizuU2CwBg%2BvmXU3nl7FP6fFUA%3D&from=3213915784_large",
            "https://p3-pc-sign.douyinpic.com/obj/tos-cn-p-0015/51c94ceed2e244af8c4b1f06ad3cf332_1673771890?x-expires=1680192000&x-signature=0b2X60%2BDC0Jy84BLPDQxGEhEV2Q%3D&from=3213915784_large"
          ]
        },
        "big_thumbs": null,
        "bit_rate": [
          {
            "FPS": 30,
            "HDR_bit": "",
            "HDR_type": "",
            "bit_rate": 2012897,
            "gear_name": "adapt_1080_0",
            "is_bytevc1": 0,
            "is_h265": 0,
            "play_addr": {
              "data_size": 3265927,
              "file_cs": "c:0-14924-075e|d:0-1632962-e8c3,1632963-3265926-40b1|a:v0300fg10000cf1rmibc77ubs1je374g",
              "file_hash": "c5403780de2d04ee827e4f0ba8a8f171",
              "height": 1440,
              "uri": "v0300fg10000cf1rmibc77ubs1je374g",
              "url_key": "v0300fg10000cf1rmibc77ubs1je374g_h264_1080p_2012897",
              "url_list": [
                "http://v26-web.douyinvod.com/22428bfcf501653e1ba980825a63593a/64134b44/video/tos/cn/tos-cn-ve-15/ooIHExhAXBdDygeGLbUAXfhA2CzPn4Qz4tJkVD/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1965&bt=1965&cs=0&ds=4&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=11&rc=Nmc7PGc1NDY4ZmZkN2hkNEBpajpoNGU6Zmx1aTMzNGkzM0AtNjYyMmIwNmMxYzVjYGBfYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "http://v3-web.douyinvod.com/d617335c5ec2b907aef53d2fadc34de4/64134b44/video/tos/cn/tos-cn-ve-15/ooIHExhAXBdDygeGLbUAXfhA2CzPn4Qz4tJkVD/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1965&bt=1965&cs=0&ds=4&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=11&rc=Nmc7PGc1NDY4ZmZkN2hkNEBpajpoNGU6Zmx1aTMzNGkzM0AtNjYyMmIwNmMxYzVjYGBfYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "https://www.douyin.com/aweme/v1/play/?video_id=v0300fg10000cf1rmibc77ubs1je374g&line=0&file_id=b1cacef48afc4cf59331e25d59989d03&sign=c5403780de2d04ee827e4f0ba8a8f171&is_play_url=1&source=PackSourceEnum_PUBLISH"
              ],
              "width": 1080
            },
            "quality_type": 4,
            "video_extra": "{\"PktOffsetMap\":\"\"}"
          },
          {
            "FPS": 30,
            "HDR_bit": "",
            "HDR_type": "",
            "bit_rate": 1991612,
            "gear_name": "normal_1080_0",
            "is_bytevc1": 0,
            "is_h265": 0,
            "play_addr": {
              "data_size": 3219940,
              "file_cs": "c:0-14919-8a6b|d:0-1609969-92a0,1609970-3219939-c228|a:v0300fg10000cf1rmibc77ubs1je374g",
              "file_hash": "3cb71c7c985a07219d3ee75e21995cea",
              "height": 1440,
              "uri": "v0300fg10000cf1rmibc77ubs1je374g",
              "url_key": "v0300fg10000cf1rmibc77ubs1je374g_h264_1080p_1991612",
              "url_list": [
                "http://v26-web.douyinvod.com/3f403c347ac78cd11b51c0e5b6e35d26/64134b44/video/tos/cn/tos-cn-ve-15/osIDUQAEe0b4Apzx4fjntnrGJ2LAkhDgDhdYB2/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1944&bt=1944&cs=0&ds=4&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=0&rc=NDs5ZmQzZjU7aDY5Ozc8Z0BpajpoNGU6Zmx1aTMzNGkzM0A1YzYvLzVjNTAxMS8tNC41YSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "http://v3-web.douyinvod.com/caa9d6d8f368238b9db8c62183e0acfc/64134b44/video/tos/cn/tos-cn-ve-15/osIDUQAEe0b4Apzx4fjntnrGJ2LAkhDgDhdYB2/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1944&bt=1944&cs=0&ds=4&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=0&rc=NDs5ZmQzZjU7aDY5Ozc8Z0BpajpoNGU6Zmx1aTMzNGkzM0A1YzYvLzVjNTAxMS8tNC41YSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "https://www.douyin.com/aweme/v1/play/?video_id=v0300fg10000cf1rmibc77ubs1je374g&line=0&file_id=8d19740826434e3882fc802a2c96f881&sign=3cb71c7c985a07219d3ee75e21995cea&is_play_url=1&source=PackSourceEnum_PUBLISH"
              ],
              "width": 1080
            },
            "quality_type": 1,
            "video_extra": "{\"PktOffsetMap\":\"\"}"
          },
          {
            "FPS": 30,
            "HDR_bit": "",
            "HDR_type": "",
            "bit_rate": 1340040,
            "gear_name": "adapt_540_0",
            "is_bytevc1": 0,
            "is_h265": 0,
            "play_addr": {
              "data_size": 2174216,
              "file_cs": "c:0-15331-53c0|d:0-1087107-5b59,1087108-2174215-0ada|a:v0300fg10000cf1rmibc77ubs1je374g",
              "file_hash": "8150b3956c65fc73ed3da6d71d1244ca",
              "height": 768,
              "uri": "v0300fg10000cf1rmibc77ubs1je374g",
              "url_key": "v0300fg10000cf1rmibc77ubs1je374g_h264_540p_1340040",
              "url_list": [
                "http://v26-web.douyinvod.com/793ba396752597e001147fd4ae10f6a1/64134b44/video/tos/cn/tos-cn-ve-15/oApzfBb4dALEnv2EIQCVhtJkDC40xUAGzAhegz/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1308&bt=1308&cs=0&ds=6&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=11&rc=N2g2O2lpZWZlOzhpNjdmOUBpajpoNGU6Zmx1aTMzNGkzM0BiYjE0MC0wNTIxLy5hMDJhYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "http://v3-web.douyinvod.com/fa8cc3ada3280f673658257e71138f5c/64134b44/video/tos/cn/tos-cn-ve-15/oApzfBb4dALEnv2EIQCVhtJkDC40xUAGzAhegz/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1308&bt=1308&cs=0&ds=6&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=11&rc=N2g2O2lpZWZlOzhpNjdmOUBpajpoNGU6Zmx1aTMzNGkzM0BiYjE0MC0wNTIxLy5hMDJhYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "https://www.douyin.com/aweme/v1/play/?video_id=v0300fg10000cf1rmibc77ubs1je374g&line=0&file_id=d65c34d31f25485b8c3b0f3f7843eee4&sign=8150b3956c65fc73ed3da6d71d1244ca&is_play_url=1&source=PackSourceEnum_PUBLISH"
              ],
              "width": 576
            },
            "quality_type": 28,
            "video_extra": "{\"PktOffsetMap\":\"\"}"
          },
          {
            "FPS": 30,
            "HDR_bit": "",
            "HDR_type": "",
            "bit_rate": 1317855,
            "gear_name": "adapt_720_0",
            "is_bytevc1": 0,
            "is_h265": 0,
            "play_addr": {
              "data_size": 2138221,
              "file_cs": "c:0-15314-6491|d:0-1069109-ab1c,1069110-2138220-8dee|a:v0300fg10000cf1rmibc77ubs1je374g",
              "file_hash": "402e341f2ffc2d345f29dffee3a52fd0",
              "height": 960,
              "uri": "v0300fg10000cf1rmibc77ubs1je374g",
              "url_key": "v0300fg10000cf1rmibc77ubs1je374g_h264_720p_1317855",
              "url_list": [
                "http://v26-web.douyinvod.com/c656ec0d67219ad0635f0ab19109b4f7/64134b44/video/tos/cn/tos-cn-ve-15/o0CCnDhUIAgxkz4tGCfDEvjhJV2bZAA4zBdeQL/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1286&bt=1286&cs=0&ds=3&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=11&rc=ODU2Omc0NWdoZTs2ZGhlNEBpajpoNGU6Zmx1aTMzNGkzM0BeMDAwMmIyXzYxNTY2YzBiYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "http://v3-web.douyinvod.com/0fa43741555dabe8e00cf0ee8b076a83/64134b44/video/tos/cn/tos-cn-ve-15/o0CCnDhUIAgxkz4tGCfDEvjhJV2bZAA4zBdeQL/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1286&bt=1286&cs=0&ds=3&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=11&rc=ODU2Omc0NWdoZTs2ZGhlNEBpajpoNGU6Zmx1aTMzNGkzM0BeMDAwMmIyXzYxNTY2YzBiYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "https://www.douyin.com/aweme/v1/play/?video_id=v0300fg10000cf1rmibc77ubs1je374g&line=0&file_id=e13bfe9a93884b9ebd52e15d373332a5&sign=402e341f2ffc2d345f29dffee3a52fd0&is_play_url=1&source=PackSourceEnum_PUBLISH"
              ],
              "width": 720
            },
            "quality_type": 18,
            "video_extra": "{\"PktOffsetMap\":\"\"}"
          },
          {
            "FPS": 30,
            "HDR_bit": "",
            "HDR_type": "",
            "bit_rate": 1267427,
            "gear_name": "normal_720_0",
            "is_bytevc1": 0,
            "is_h265": 0,
            "play_addr": {
              "data_size": 2049113,
              "file_cs": "c:0-15373-f22c|d:0-1024555-6ee0,1024556-2049112-d736|a:v0300fg10000cf1rmibc77ubs1je374g",
              "file_hash": "122459680c1c32c887b0752d2f55b2f3",
              "height": 960,
              "uri": "v0300fg10000cf1rmibc77ubs1je374g",
              "url_key": "v0300fg10000cf1rmibc77ubs1je374g_h264_720p_1267427",
              "url_list": [
                "http://v26-web.douyinvod.com/252de32862d8f1c69dd1ab8e416657ec/64134b44/video/tos/cn/tos-cn-ve-15c001-alinc2/oYtk9n3HdxGKIghlubhf4AYzBDBJ4UeD2LDAQA/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1237&bt=1237&cs=0&ds=3&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=0&rc=Z2Y4aTQzZmVkO2c0N2Q3ZkBpajpoNGU6Zmx1aTMzNGkzM0A0NTNfLjNjXzMxM2M0NmI2YSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "http://v3-web.douyinvod.com/bb86e02c3172501caba21f883fe13d1c/64134b44/video/tos/cn/tos-cn-ve-15c001-alinc2/oYtk9n3HdxGKIghlubhf4AYzBDBJ4UeD2LDAQA/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1237&bt=1237&cs=0&ds=3&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=0&rc=Z2Y4aTQzZmVkO2c0N2Q3ZkBpajpoNGU6Zmx1aTMzNGkzM0A0NTNfLjNjXzMxM2M0NmI2YSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "https://www.douyin.com/aweme/v1/play/?video_id=v0300fg10000cf1rmibc77ubs1je374g&line=0&file_id=9ce49a74f16d486abbfc6011bf658c7d&sign=122459680c1c32c887b0752d2f55b2f3&is_play_url=1&source=PackSourceEnum_PUBLISH"
              ],
              "width": 720
            },
            "quality_type": 10,
            "video_extra": "{\"PktOffsetMap\":\"\"}"
          },
          {
            "FPS": 30,
            "HDR_bit": "",
            "HDR_type": "",
            "bit_rate": 1151860,
            "gear_name": "normal_540_0",
            "is_bytevc1": 0,
            "is_h265": 0,
            "play_addr": {
              "data_size": 1862270,
              "file_cs": "c:0-15390-59a8|d:0-931134-0fba,931135-1862269-4c90|a:v0300fg10000cf1rmibc77ubs1je374g",
              "file_hash": "02420d7bd9f43852899167b8d68e51db",
              "height": 768,
              "uri": "v0300fg10000cf1rmibc77ubs1je374g",
              "url_key": "v0300fg10000cf1rmibc77ubs1je374g_h264_540p_1151860",
              "url_list": [
                "http://v26-web.douyinvod.com/71883a251339dde515e6099298825207/64134b44/video/tos/cn/tos-cn-ve-15/o0twnbXJAD4DoHeOwgjgeBMHQ097AjDSWAnD3O/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1124&bt=1124&cs=0&ds=6&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=0&rc=OGlmZTo6ZTZoMzhmNWU6O0BpajpoNGU6Zmx1aTMzNGkzM0BjMTVhYGE2NjAxNC8tX2A0YSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "http://v3-web.douyinvod.com/6fc347e0e61424e1fcad2a23ff5487b3/64134b44/video/tos/cn/tos-cn-ve-15/o0twnbXJAD4DoHeOwgjgeBMHQ097AjDSWAnD3O/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1124&bt=1124&cs=0&ds=6&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=0&rc=OGlmZTo6ZTZoMzhmNWU6O0BpajpoNGU6Zmx1aTMzNGkzM0BjMTVhYGE2NjAxNC8tX2A0YSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "https://www.douyin.com/aweme/v1/play/?video_id=v0300fg10000cf1rmibc77ubs1je374g&line=0&file_id=78c7bb022c75403e939bd7c7db8c4ff5&sign=02420d7bd9f43852899167b8d68e51db&is_play_url=1&source=PackSourceEnum_PUBLISH"
              ],
              "width": 576
            },
            "quality_type": 20,
            "video_extra": "{\"PktOffsetMap\":\"\"}"
          },
          {
            "FPS": 30,
            "HDR_bit": "",
            "HDR_type": "",
            "bit_rate": 831739,
            "gear_name": "adapt_lower_540_0",
            "is_bytevc1": 0,
            "is_h265": 0,
            "play_addr": {
              "data_size": 1361454,
              "file_cs": "c:0-11953-262c|d:0-680726-00d2,680727-1361453-324d|a:v0300fg10000cf1rmibc77ubs1je374g",
              "file_hash": "77c5f35b0db82defffa97ce7bc9b38ec",
              "height": 768,
              "uri": "v0300fg10000cf1rmibc77ubs1je374g",
              "url_key": "v0300fg10000cf1rmibc77ubs1je374g_h264_540p_831739",
              "url_list": [
                "http://v26-web.douyinvod.com/e2f99541693cb158077ac45d76b3df99/64134b44/video/tos/cn/tos-cn-ve-15/oshNbBeAIAAtVUHEQxTgGJ4hDBf2nC4zdh0kZL/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=812&bt=812&cs=0&ds=6&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=14&rc=NmQ4NjdlOzc6NzdlOzRpZEBpajpoNGU6Zmx1aTMzNGkzM0A1NDMvYDFeNmAxMmJjMy0xYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "http://v3-web.douyinvod.com/942e06f3ac5979a948168b6b9713067f/64134b44/video/tos/cn/tos-cn-ve-15/oshNbBeAIAAtVUHEQxTgGJ4hDBf2nC4zdh0kZL/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=812&bt=812&cs=0&ds=6&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=14&rc=NmQ4NjdlOzc6NzdlOzRpZEBpajpoNGU6Zmx1aTMzNGkzM0A1NDMvYDFeNmAxMmJjMy0xYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "https://www.douyin.com/aweme/v1/play/?video_id=v0300fg10000cf1rmibc77ubs1je374g&line=0&file_id=4a0f61f8eb5444c794a84bc423657a83&sign=77c5f35b0db82defffa97ce7bc9b38ec&is_play_url=1&source=PackSourceEnum_PUBLISH"
              ],
              "width": 576
            },
            "quality_type": 21,
            "video_extra": "{\"PktOffsetMap\":\"\"}"
          },
          {
            "FPS": 30,
            "HDR_bit": "",
            "HDR_type": "",
            "bit_rate": 792704,
            "gear_name": "lower_540_0",
            "is_bytevc1": 0,
            "is_h265": 0,
            "play_addr": {
              "data_size": 1281605,
              "file_cs": "c:0-12012-8645|d:0-640801-f5c9,640802-1281604-ec43|a:v0300fg10000cf1rmibc77ubs1je374g",
              "file_hash": "0cce94df123f2d148812acba2cc26b10",
              "height": 768,
              "uri": "v0300fg10000cf1rmibc77ubs1je374g",
              "url_key": "v0300fg10000cf1rmibc77ubs1je374g_h264_540p_792704",
              "url_list": [
                "http://v26-web.douyinvod.com/aba451dabc6f4694df3fe35f21fa523e/64134b44/video/tos/cn/tos-cn-ve-15/okBMQtnGzAPxfObAkDhzdJIa4BDU4JhgLOeY2A/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=774&bt=774&cs=0&ds=6&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=4&rc=ZGk7aDw6PGc8NjloOzg0Z0BpajpoNGU6Zmx1aTMzNGkzM0BgYV5eLzQxXjExNTAuYWMyYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "http://v3-web.douyinvod.com/85134e578d0115e258febe5ecfa437a6/64134b44/video/tos/cn/tos-cn-ve-15/okBMQtnGzAPxfObAkDhzdJIa4BDU4JhgLOeY2A/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=774&bt=774&cs=0&ds=6&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=4&rc=ZGk7aDw6PGc8NjloOzg0Z0BpajpoNGU6Zmx1aTMzNGkzM0BgYV5eLzQxXjExNTAuYWMyYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "https://www.douyin.com/aweme/v1/play/?video_id=v0300fg10000cf1rmibc77ubs1je374g&line=0&file_id=5df1d5183e864349ad497729aea8dfca&sign=0cce94df123f2d148812acba2cc26b10&is_play_url=1&source=PackSourceEnum_PUBLISH"
              ],
              "width": 576
            },
            "quality_type": 24,
            "video_extra": "{\"PktOffsetMap\":\"\"}"
          },
          {
            "FPS": 30,
            "HDR_bit": "",
            "HDR_type": "",
            "bit_rate": 722568,
            "gear_name": "adapt_lowest_720_1",
            "is_bytevc1": 1,
            "is_h265": 1,
            "play_addr": {
              "data_size": 1168212,
              "file_cs": "c:0-12337-3fdb|d:0-584105-38a3,584106-1168211-62fb|a:v0300fg10000cf1rmibc77ubs1je374g",
              "file_hash": "a62a4fb61f8bc4cbd602c795213a7029",
              "height": 960,
              "uri": "v0300fg10000cf1rmibc77ubs1je374g",
              "url_key": "v0300fg10000cf1rmibc77ubs1je374g_bytevc1_720p_722568",
              "url_list": [
                "http://v26-web.douyinvod.com/905cf02e9dc647b9981b57a9a8466754/64134b44/video/tos/cn/tos-cn-ve-15/oIJ70Dge3DOAwCMjASgwodQHbtAm3BADOnX9we/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=705&bt=705&cs=2&ds=3&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=15&rc=Z2Q6PDo3M2U1MzMzODs8O0BpajpoNGU6Zmx1aTMzNGkzM0AuLl5eYC1hNTAxYmAtNl9fYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "http://v3-web.douyinvod.com/cfbdbf4bdaf554b88a938bdaa744b461/64134b44/video/tos/cn/tos-cn-ve-15/oIJ70Dge3DOAwCMjASgwodQHbtAm3BADOnX9we/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=705&bt=705&cs=2&ds=3&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=15&rc=Z2Q6PDo3M2U1MzMzODs8O0BpajpoNGU6Zmx1aTMzNGkzM0AuLl5eYC1hNTAxYmAtNl9fYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "https://www.douyin.com/aweme/v1/play/?video_id=v0300fg10000cf1rmibc77ubs1je374g&line=0&file_id=b8b99805c0e040328bd004c7a9a71a1d&sign=a62a4fb61f8bc4cbd602c795213a7029&is_play_url=1&source=PackSourceEnum_PUBLISH"
              ],
              "width": 720
            },
            "quality_type": 15,
            "video_extra": "{\"PktOffsetMap\":\"\"}"
          },
          {
            "FPS": 30,
            "HDR_bit": "",
            "HDR_type": "",
            "bit_rate": 645024,
            "gear_name": "adapt_540_1",
            "is_bytevc1": 1,
            "is_h265": 1,
            "play_addr": {
              "data_size": 1042843,
              "file_cs": "c:0-12337-3ccf|d:0-521420-2291,521421-1042842-2f24|a:v0300fg10000cf1rmibc77ubs1je374g",
              "file_hash": "ae2d2f0e2ffe26e568054f244d1699f0",
              "height": 768,
              "uri": "v0300fg10000cf1rmibc77ubs1je374g",
              "url_key": "v0300fg10000cf1rmibc77ubs1je374g_bytevc1_540p_645024",
              "url_list": [
                "http://v26-web.douyinvod.com/84e2bb3d14ca423224eae76ede8d9b45/64134b44/video/tos/cn/tos-cn-ve-15/oIevuAkbALZUnP5xJdDfh2h4IBGtm6gDogzuA4/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=629&bt=629&cs=2&ds=6&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=11&rc=ZjdkOTVoN2gzaTk7ZTs0N0BpajpoNGU6Zmx1aTMzNGkzM0BfMTYvXjI0NmMxYy9gYGNhYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "http://v3-web.douyinvod.com/39c897217ceeac28de2af0ba2c30d16c/64134b44/video/tos/cn/tos-cn-ve-15/oIevuAkbALZUnP5xJdDfh2h4IBGtm6gDogzuA4/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=629&bt=629&cs=2&ds=6&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=11&rc=ZjdkOTVoN2gzaTk7ZTs0N0BpajpoNGU6Zmx1aTMzNGkzM0BfMTYvXjI0NmMxYy9gYGNhYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "https://www.douyin.com/aweme/v1/play/?video_id=v0300fg10000cf1rmibc77ubs1je374g&line=0&file_id=d4f1c8cb28f64ff09e745ea2269a44bc&sign=ae2d2f0e2ffe26e568054f244d1699f0&is_play_url=1&source=PackSourceEnum_PUBLISH"
              ],
              "width": 576
            },
            "quality_type": 28,
            "video_extra": "{\"PktOffsetMap\":\"\"}"
          },
          {
            "FPS": 30,
            "HDR_bit": "",
            "HDR_type": "",
            "bit_rate": 557916,
            "gear_name": "adapt_lower_540_1",
            "is_bytevc1": 1,
            "is_h265": 1,
            "play_addr": {
              "data_size": 902011,
              "file_cs": "c:0-12337-f6d4|d:0-451004-62bd,451005-902010-29cd|a:v0300fg10000cf1rmibc77ubs1je374g",
              "file_hash": "ddee5b21310d96a2e4920e64d729f446",
              "height": 768,
              "uri": "v0300fg10000cf1rmibc77ubs1je374g",
              "url_key": "v0300fg10000cf1rmibc77ubs1je374g_bytevc1_540p_557916",
              "url_list": [
                "http://v26-web.douyinvod.com/28b45fc88e78a78727eca6ea489d0267/64134b44/video/tos/cn/tos-cn-ve-15/ocGdDAhidDNubhUxv4ftABgunva32JI4ewzLAk/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=544&bt=544&cs=2&ds=6&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=14&rc=aTloZzQ2OjU3ODs7aDtmZUBpajpoNGU6Zmx1aTMzNGkzM0AtNDM2Ml8xXzQxYC5gYTM1YSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "http://v3-web.douyinvod.com/38740a64f1606096e9e424d5ca3b01ce/64134b44/video/tos/cn/tos-cn-ve-15/ocGdDAhidDNubhUxv4ftABgunva32JI4ewzLAk/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=544&bt=544&cs=2&ds=6&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=14&rc=aTloZzQ2OjU3ODs7aDtmZUBpajpoNGU6Zmx1aTMzNGkzM0AtNDM2Ml8xXzQxYC5gYTM1YSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
                "https://www.douyin.com/aweme/v1/play/?video_id=v0300fg10000cf1rmibc77ubs1je374g&line=0&file_id=8b6cd8ce18c84574b247b3519d6e760f&sign=ddee5b21310d96a2e4920e64d729f446&is_play_url=1&source=PackSourceEnum_PUBLISH"
              ],
              "width": 576
            },
            "quality_type": 21,
            "video_extra": "{\"PktOffsetMap\":\"\"}"
          }
        ],
        "cover": {
          "height": 720,
          "uri": "tos-cn-p-0015/oU7EAZxJhfA4z4BgIeCzDkbhdnuE2LxDsAGtB2",
          "url_list": [
            "https://p6-pc-sign.douyinpic.com/tos-cn-p-0015/oU7EAZxJhfA4z4BgIeCzDkbhdnuE2LxDsAGtB2~tplv-dy-cropcenter:323:430.jpeg?x-expires=1994342400&x-signature=0aL3PMLlwY9m0DdOk%2B0qpJzRfhw%3D&from=3213915784&s=PackSourceEnum_PUBLISH&se=true&sh=323_430&sc=cover&biz_tag=pcweb_cover&l=20230317000040E64A9BC92C5D4748215F",
            "https://p9-pc-sign.douyinpic.com/obj/tos-cn-p-0015/oU7EAZxJhfA4z4BgIeCzDkbhdnuE2LxDsAGtB2?x-expires=1994342400&x-signature=sgLtuq7SgnYMoJAo8nyCIOMuyjM%3D&from=3213915784&s=PackSourceEnum_PUBLISH&se=false&sc=cover&biz_tag=pcweb_cover&l=20230317000040E64A9BC92C5D4748215F",
            "https://p6-pc-sign.douyinpic.com/obj/tos-cn-p-0015/oU7EAZxJhfA4z4BgIeCzDkbhdnuE2LxDsAGtB2?x-expires=1994342400&x-signature=ozPTwyZUPj2pSCY9M7UfxmmN1js%3D&from=3213915784&s=PackSourceEnum_PUBLISH&se=false&sc=cover&biz_tag=pcweb_cover&l=20230317000040E64A9BC92C5D4748215F",
            "https://p3-pc-sign.douyinpic.com/obj/tos-cn-p-0015/oU7EAZxJhfA4z4BgIeCzDkbhdnuE2LxDsAGtB2?x-expires=1994342400&x-signature=szGjh9zwf6Vp1Eztm22%2BmsGzinU%3D&from=3213915784&s=PackSourceEnum_PUBLISH&se=false&sc=cover&biz_tag=pcweb_cover&l=20230317000040E64A9BC92C5D4748215F"
          ],
          "width": 720
        },
        "download_addr": {
          "data_size": 2737901,
          "height": 720,
          "uri": "v0300fg10000cf1rmibc77ubs1je374g",
          "url_list": [
            "http://v26-web.douyinvod.com/54936b94a4f52486ca9b96628892747e/64134b44/video/tos/cn/tos-cn-ve-15c001-alinc2/ooWneB3w7AXOOOtHQgFwDbSJDdwejoAMMAD9g4/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1340&bt=1340&cs=0&ds=3&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=0&rc=aWQ5Ojs8Zmc4aGg2NGZkZ0BpajpoNGU6Zmx1aTMzNGkzM0AxLzIvL2MuNWIxLzVjXy9gYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
            "http://v3-web.douyinvod.com/595695ab311c3bab0a1e79194cb4a8bb/64134b44/video/tos/cn/tos-cn-ve-15c001-alinc2/ooWneB3w7AXOOOtHQgFwDbSJDdwejoAMMAD9g4/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1340&bt=1340&cs=0&ds=3&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=0&rc=aWQ5Ojs8Zmc4aGg2NGZkZ0BpajpoNGU6Zmx1aTMzNGkzM0AxLzIvL2MuNWIxLzVjXy9gYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
            "https://www.douyin.com/aweme/v1/play/?video_id=v0300fg10000cf1rmibc77ubs1je374g&line=0&ratio=540p&watermark=1&media_type=4&vr_type=0&improve_bitrate=0&biz_sign=NRPI1lC4AlkgB1YZ_o3JxvAfESRKvePEcuHF98w5fX-8HccpC4oAms9EpeDT9VaaOzLa7CA0Ou-V1V2BgFgadN4R6UvFDGbNHaUZIZuaRMUGyO7s5wbVW7et0I2xsyVeH7OYijs=&logo_name=aweme_search_suffix&quality_type=11&source=PackSourceEnum_PUBLISH"
          ],
          "width": 720
        },
        "duration": 13095,
        "dynamic_cover": {
          "height": 720,
          "uri": "tos-cn-p-0015/1362a86514fd47c19cda3b5e7169bd81_1673771890",
          "url_list": [
            "https://p9-pc-sign.douyinpic.com/obj/tos-cn-p-0015/1362a86514fd47c19cda3b5e7169bd81_1673771890?x-expires=1680192000&x-signature=hOt%2F5BjNZbqkcrXPe2g3lI6KNzE%3D&from=3213915784_large",
            "https://p6-pc-sign.douyinpic.com/obj/tos-cn-p-0015/1362a86514fd47c19cda3b5e7169bd81_1673771890?x-expires=1680192000&x-signature=kkq9KjiazN7D9O689ltoo8B8lYc%3D&from=3213915784_large",
            "https://p3-pc-sign.douyinpic.com/obj/tos-cn-p-0015/1362a86514fd47c19cda3b5e7169bd81_1673771890?x-expires=1680192000&x-signature=Ght%2FZp7l06syo86NI7rel2AaHWQ%3D&from=3213915784_large"
          ],
          "width": 720
        },
        "height": 1440,
        "is_h265": 0,
        "is_source_HDR": 0,
        "meta": "{\"bright_ratio_mean\":\"0.0525\",\"brightness_mean\":\"142.4347\",\"diff_overexposure_ratio\":\"0.0712\",\"fullscreen_max_crop\":\"{\\\"maxcrop_left\\\": -1.0, \\\"maxcrop_right\\\": -1.0, \\\"maxcrop_top\\\": -1.0, \\\"version\\\": \\\"v1.0\\\"}\",\"loudness\":\"-4.6\",\"overexposure_ratio_mean\":\"0.0373\",\"peak\":\"1\",\"qprf\":\"1.000\",\"sr_score\":\"1.000\",\"std_brightness\":\"18.8792\",\"title_info\":\"{\\\"ratio_br_l\\\": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], \\\"ratio_edge_l\\\": [0.0, 0.03, 0.1, 0.14, 0.17, 0.18], \\\"progress_bar\\\": [0.0, 0.0, 0.0], \\\"version\\\": \\\"v1.0\\\"}\"}",
        "origin_cover": {
          "height": 720,
          "uri": "tos-cn-p-0015/5adca00ebb5642a0a13eae1875694f2c_1673771890",
          "url_list": [
            "https://p6-pc-sign.douyinpic.com/tos-cn-p-0015/5adca00ebb5642a0a13eae1875694f2c_1673771890~tplv-dy-360p.jpeg?x-expires=1680192000&x-signature=EhAyNeKBUPixluvNCxb1ulTIpK0%3D&from=3213915784&se=false&biz_tag=pcweb_cover&l=20230317000040E64A9BC92C5D4748215F",
            "https://p9-pc-sign.douyinpic.com/tos-cn-p-0015/5adca00ebb5642a0a13eae1875694f2c_1673771890~tplv-dy-360p.jpeg?x-expires=1680192000&x-signature=k73mZnluAQKE1nB94IP5y1xSkMY%3D&from=3213915784&se=false&biz_tag=pcweb_cover&l=20230317000040E64A9BC92C5D4748215F",
            "https://p3-pc-sign.douyinpic.com/tos-cn-p-0015/5adca00ebb5642a0a13eae1875694f2c_1673771890~tplv-dy-360p.jpeg?x-expires=1680192000&x-signature=n3zkCuMKeaLs%2BVBeyoK5GDPmgz0%3D&from=3213915784&se=false&biz_tag=pcweb_cover&l=20230317000040E64A9BC92C5D4748215F"
          ],
          "width": 720
        },
        "play_addr": {
          "data_size": 3219940,
          "file_cs": "c:0-14919-8a6b|d:0-1609969-92a0,1609970-3219939-c228|a:v0300fg10000cf1rmibc77ubs1je374g",
          "file_hash": "3cb71c7c985a07219d3ee75e21995cea",
          "height": 1440,
          "uri": "v0300fg10000cf1rmibc77ubs1je374g",
          "url_key": "v0300fg10000cf1rmibc77ubs1je374g_h264_1080p_1991612",
          "url_list": [
            "http://v26-web.douyinvod.com/3f403c347ac78cd11b51c0e5b6e35d26/64134b44/video/tos/cn/tos-cn-ve-15/osIDUQAEe0b4Apzx4fjntnrGJ2LAkhDgDhdYB2/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1944&bt=1944&cs=0&ds=4&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=0&rc=NDs5ZmQzZjU7aDY5Ozc8Z0BpajpoNGU6Zmx1aTMzNGkzM0A1YzYvLzVjNTAxMS8tNC41YSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
            "http://v3-web.douyinvod.com/caa9d6d8f368238b9db8c62183e0acfc/64134b44/video/tos/cn/tos-cn-ve-15/osIDUQAEe0b4Apzx4fjntnrGJ2LAkhDgDhdYB2/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1944&bt=1944&cs=0&ds=4&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=0&rc=NDs5ZmQzZjU7aDY5Ozc8Z0BpajpoNGU6Zmx1aTMzNGkzM0A1YzYvLzVjNTAxMS8tNC41YSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
            "https://www.douyin.com/aweme/v1/play/?video_id=v0300fg10000cf1rmibc77ubs1je374g&line=0&file_id=8d19740826434e3882fc802a2c96f881&sign=3cb71c7c985a07219d3ee75e21995cea&is_play_url=1&source=PackSourceEnum_PUBLISH"
          ],
          "width": 1080
        },
        "play_addr_265": {
          "data_size": 1042843,
          "file_cs": "c:0-12337-3ccf|d:0-521420-2291,521421-1042842-2f24|a:v0300fg10000cf1rmibc77ubs1je374g",
          "file_hash": "ae2d2f0e2ffe26e568054f244d1699f0",
          "height": 768,
          "uri": "v0300fg10000cf1rmibc77ubs1je374g",
          "url_key": "v0300fg10000cf1rmibc77ubs1je374g_bytevc1_540p_645024",
          "url_list": [
            "http://v26-web.douyinvod.com/84e2bb3d14ca423224eae76ede8d9b45/64134b44/video/tos/cn/tos-cn-ve-15/oIevuAkbALZUnP5xJdDfh2h4IBGtm6gDogzuA4/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=629&bt=629&cs=2&ds=6&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=11&rc=ZjdkOTVoN2gzaTk7ZTs0N0BpajpoNGU6Zmx1aTMzNGkzM0BfMTYvXjI0NmMxYy9gYGNhYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
            "http://v3-web.douyinvod.com/39c897217ceeac28de2af0ba2c30d16c/64134b44/video/tos/cn/tos-cn-ve-15/oIevuAkbALZUnP5xJdDfh2h4IBGtm6gDogzuA4/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=629&bt=629&cs=2&ds=6&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=11&rc=ZjdkOTVoN2gzaTk7ZTs0N0BpajpoNGU6Zmx1aTMzNGkzM0BfMTYvXjI0NmMxYy9gYGNhYSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
            "https://www.douyin.com/aweme/v1/play/?video_id=v0300fg10000cf1rmibc77ubs1je374g&line=0&file_id=d4f1c8cb28f64ff09e745ea2269a44bc&sign=ae2d2f0e2ffe26e568054f244d1699f0&is_play_url=1&source=PackSourceEnum_PUBLISH"
          ],
          "width": 576
        },
        "play_addr_h264": {
          "data_size": 3219940,
          "file_cs": "c:0-14919-8a6b|d:0-1609969-92a0,1609970-3219939-c228|a:v0300fg10000cf1rmibc77ubs1je374g",
          "file_hash": "3cb71c7c985a07219d3ee75e21995cea",
          "height": 1440,
          "uri": "v0300fg10000cf1rmibc77ubs1je374g",
          "url_key": "v0300fg10000cf1rmibc77ubs1je374g_h264_1080p_1991612",
          "url_list": [
            "http://v26-web.douyinvod.com/3f403c347ac78cd11b51c0e5b6e35d26/64134b44/video/tos/cn/tos-cn-ve-15/osIDUQAEe0b4Apzx4fjntnrGJ2LAkhDgDhdYB2/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1944&bt=1944&cs=0&ds=4&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=0&rc=NDs5ZmQzZjU7aDY5Ozc8Z0BpajpoNGU6Zmx1aTMzNGkzM0A1YzYvLzVjNTAxMS8tNC41YSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
            "http://v3-web.douyinvod.com/caa9d6d8f368238b9db8c62183e0acfc/64134b44/video/tos/cn/tos-cn-ve-15/osIDUQAEe0b4Apzx4fjntnrGJ2LAkhDgDhdYB2/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1944&bt=1944&cs=0&ds=4&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLRuD6ZU_4MIDbeJNv7T&mime_type=video_mp4&qs=0&rc=NDs5ZmQzZjU7aDY5Ozc8Z0BpajpoNGU6Zmx1aTMzNGkzM0A1YzYvLzVjNTAxMS8tNC41YSMxMGdwcjRfai5gLS1kLTBzcw%3D%3D&l=20230317000040E64A9BC92C5D4748215F&btag=8000",
            "https://www.douyin.com/aweme/v1/play/?video_id=v0300fg10000cf1rmibc77ubs1je374g&line=0&file_id=8d19740826434e3882fc802a2c96f881&sign=3cb71c7c985a07219d3ee75e21995cea&is_play_url=1&source=PackSourceEnum_PUBLISH"
          ],
          "width": 1080
        },
        "ratio": "1080p",
        "video_model": "",
        "width": 1080
      },
      "video_game_data_channel_config": {},
      "video_labels": [],
      "video_tag": [
        {
          "level": 1,
          "tag_id": 2027,
          "tag_name": "萌宠"
        },
        {
          "level": 2,
          "tag_id": 2027002,
          "tag_name": "宠物狗"
        },
        {
          "level": 3,
          "tag_id": 2027002003,
          "tag_name": "狗vlog日常"
        }
      ],
      "video_text": [],
      "voice_modify_id_list": null
    }
  ],
  "has_more": 1,
  "log_pb": {
    "impr_id": "20230317000040E64A9BC92C5D4748215F"
  },
  "max_cursor": 1673771886000,
  "min_cursor": 1673771886000,
  "post_serial": 2,
  "replace_series_cover": 1,
  "request_item_cursor": 1674630472000,
  "status_code": 0
}
    """

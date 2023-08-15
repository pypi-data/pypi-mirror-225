def get_user_info(url: str, cookies: str)->dict:
    """获取用户信息

    Args:
        url (str): 
            用户空间地址

            ```https://www.douyin.com/user/MS4wLjABAAAAP9IeZhDHS5xRBl20L8d-rDjNFokqnZTBVOw72A1GxzIIezcDJu6QzDCkNa3FsbY2```

            支持分享口令

            ```4- 长按复制此条消息，打开抖音搜索，查看TA的更多作品。 https://v.douyin.com/ScY3jxF/```


        cookies (str): 抓包获取

    Returns:
        dict: 用户基本信息
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

def parse_video(url: str, cookies: str) -> str:
    """解析视频

    Args:
        url (str): 
            视频播放页面地址

            ```https://www.douyin.com/video/7188795449468259623```

            支持分享口令

            ```2.00 fbA:/ 不准笑！# 翻唱歌曲 # 勇气大爆发 # 热门音乐🔥  https://v.douyin.com/SvkjGxL/ 复制此链接，打开Dou音搜索，直接观看视频！```

        cookies (str): 抓包获取

    Returns:
        str: 视频下载地址
            https://v26-web.douyinvod.com/f7faca2a086a6523cb8e380f031ba894/6415587b/video/tos/cn/tos-cn-ve-15c001-alinc2/owF7RhhUIAgyY6Ctl2fDSaop3YvD5AAnzBWeQJ/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=2496&bt=2496&cs=0&ds=4&ft=TqQkmM0Txxoupo._4PI12lMg4-iGNbLeapMZU_46zRGKSNv7T&mime_type=video_mp4&qs=0&rc=ZWRoOzw1aTRpOjw2Zjs5Z0Bpamtoczw6ZmZnajMzNGkzM0AxNGAxNi0xX2MxLzIvMDYvYSNvZjVncjRfYzZgLS1kLTBzcw%3D%3D&l=2023031813212853EA028CF0B44A610D8A&btag=10000
    """

def download_video(url: str, videopath: str, cookies: str):
    """下载视频

    Args:
        url (str): 
            视频播放页面地址

            ```https://www.douyin.com/video/7188795449468259623```

            支持分享口令

            ```2.00 fbA:/ 不准笑！# 翻唱歌曲 # 勇气大爆发 # 热门音乐🔥  https://v.douyin.com/SvkjGxL/ 复制此链接，打开Dou音搜索，直接观看视频！```

        videopath (str): 保存地址

        cookies (str): 抓包获取
    """
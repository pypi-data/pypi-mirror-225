from requests import Session, Response
from requests.cookies import RequestsCookieJar


def get_userinfo(session: Session, cookies: RequestsCookieJar) -> Response:
    """获取用户信息

    Args:
        session (Session): _description_
        cookies (RequestsCookieJar): 浏览器抓包获取

    Returns:
        Response: 返回请求
            成功 
{
  "extra": {
    "logid": "20230310145836BEE57739F7BA9D0DACD1",
    "now": 1678431516000
  },
  "login_app": "aweme",
  "status_code": 0,
  "user": {
    "avatar_larger": {
      "uri": "1080x1080/aweme-avatar/tos-cn-i-0813_66236bb2bc5d4bfab88a5c854ec22113",
      "url_list": [
        "https://p6.douyinpic.com/aweme/1080x1080/aweme-avatar/tos-cn-i-0813_66236bb2bc5d4bfab88a5c854ec22113.jpeg?from=2956013662",
        "https://p11.douyinpic.com/aweme/1080x1080/aweme-avatar/tos-cn-i-0813_66236bb2bc5d4bfab88a5c854ec22113.jpeg?from=2956013662",
        "https://p3.douyinpic.com/aweme/1080x1080/aweme-avatar/tos-cn-i-0813_66236bb2bc5d4bfab88a5c854ec22113.jpeg?from=2956013662"
      ]
    },
    "avatar_medium": {
      "uri": "720x720/aweme-avatar/tos-cn-i-0813_66236bb2bc5d4bfab88a5c854ec22113",
      "url_list": [
        "https://p6.douyinpic.com/aweme/720x720/aweme-avatar/tos-cn-i-0813_66236bb2bc5d4bfab88a5c854ec22113.jpeg?from=2956013662",
        "https://p11.douyinpic.com/aweme/720x720/aweme-avatar/tos-cn-i-0813_66236bb2bc5d4bfab88a5c854ec22113.jpeg?from=2956013662",
        "https://p3.douyinpic.com/aweme/720x720/aweme-avatar/tos-cn-i-0813_66236bb2bc5d4bfab88a5c854ec22113.jpeg?from=2956013662"
      ]
    },
    "avatar_thumb": {
      "uri": "100x100/aweme-avatar/tos-cn-i-0813_66236bb2bc5d4bfab88a5c854ec22113",
      "url_list": [
        "https://p6.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-i-0813_66236bb2bc5d4bfab88a5c854ec22113.jpeg?from=2956013662",
        "https://p11.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-i-0813_66236bb2bc5d4bfab88a5c854ec22113.jpeg?from=2956013662",
        "https://p3.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-i-0813_66236bb2bc5d4bfab88a5c854ec22113.jpeg?from=2956013662"
      ]
    },
    "aweme_count": 28,
    "bind_phone": "131******80",
    "bind_taobao_pub": false,
    "card_entries": null,
    "city_code": 1795565,
    "commerce_user_info": {
      "star_atlas": 0
    },
    "confer_mod": false,
    "custom_verify": "",
    "enterprise_verify_reason": "",
    "favoriting_count": 2,
    "follow_status": 0,
    "follower_count": 1,
    "follower_status": 0,
    "followers_detail": null,
    "following_count": 5,
    "geofencing": null,
    "has_orders": false,
    "is_ad_fake": false,
    "is_gov_media_vip": false,
    "is_preview": false,
    "local_code": "440300",
    "longvideo_permission": true,
    "mix_info": null,
    "mix_permission": true,
    "nickname": "dog",
    "original_musician": {
      "music_count": 0,
      "music_used_count": 0
    },
    "permission": {
      "anchor": [
        4
      ],
      "batch_images_publish": false,
      "csr_creator_anchor": false,
      "enable_set_charge_comment_audit": false,
      "hotspot": false,
      "important_record": false,
      "knowlege_mix": false,
      "long_title": true,
      "longvideo": true,
      "longvideo_15min": false,
      "longvideo_publish_ab": 1,
      "mix": true,
      "music": false,
      "playlet": false,
      "preview": false,
      "show_chapter_editor": 1,
      "toutiao_recommend_video": false,
      "upload_video_max_duration": 1800,
      "user_sign": false,
      "vr": false
    },
    "platform_sync_info": null,
    "policy_version": null,
    "rate": 1,
    "record_permission": false,
    "region": "CN",
    "sec_uid": "MS4wLjABAAAAr3X2kAUIhCsNYyc20oom84Nd1q73rgmp-QMcG8-22dVnJI-FrnwrDbDPciWFyi_d",
    "secret": 0,
    "short_id": "38500739040",
    "signature": "",
    "special_schedule": false,
    "status": 1,
    "story_open": false,
    "sync_to_xigua": 1,
    "tac": "tac='i+2gv0yaq1a2ns!i#ggjs\"yZl!%s\"l\"u&kLs#l l#vr*charCodeAtx0[!cb^i$1em7b*0d#>>>s j\\uffeel  s#'",
    "third_avatar_url": "https://sf1-cdn-tos.bdxiguastatic.com/img/user-avatar/5f5b01438d11c745a4a2347cee4a0f33~300x300.image",
    "third_name": "做有态度的粪青",
    "total_favorited": "4",
    "type_label": [],
    "uid": "3017485660982158",
    "unique_id": "38500739040",
    "user_admire_status": 0,
    "user_canceled": false,
    "verification_type": 1,
    "video_icon": {
      "uri": "",
      "url_list": []
    },
    "with_commerce_entry": false,
    "with_fusion_shop_entry": false,
    "with_shop_entry": false,
    "wx_tag": 0
  }
}
    """
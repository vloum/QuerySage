# from functools import reduce
# from hashlib import md5
# import urllib.parse
# import time
# import requests

# mixinKeyEncTab = [
#     46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
#     33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
#     61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
#     36, 20, 34, 44, 52
# ]

# cookie = '''buvid3=60DF259C-DB66-3789-F899-51C953F2AF0A47531infoc; b_nut=1703910447; CURRENT_FNVAL=4048; _uuid=21F1C13B-8754-6ECC-59D3-A825A1636F10954720infoc; buvid4=8C6B3355-C650-6CB3-865D-4AA29E6B5C7624648-023100103-6hf+YW6uzXv5j0A9VB16dQ%3D%3D; rpdid=|(k|J||Y)|YR0J'u~|Jmu|Rl); header_theme_version=CLOSE; home_feed_column=5;fingerprint=17bf9927266dbdc2e8164a5cb0555037; buvid_fp_plain=undefined; DedeUserID=594962304; DedeUserID__ckMd5=4fc8071b0b307b7c; CURRENT_QUALITY=80; PVID=1;enable_web_push=ENABLE; iflogin_when_web_push=1; bsource=search_bing; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDg4MzEzNTMsImlhdCI6MTcwODU3MjA5MywicGx0IjotMX0.7nWogW5mjUiBdctE4sJ6GK4wFd1Gae3Ml0pbOVjnQ6Y; bili_ticket_expires=1708831293; SESSDATA=1794c296%2C1724125782%2Ceacdc%2A21CjCuMDMp_WA-Fbr79XKPwekhirlBh-9o9hUYMQIc-or4V51PZxWfL4m-0wAVLlqci2USVlpUSGZ1dTF3TjNDYVBSaDE4UkRyb2VJWjkybTNneVM4U1AwTWRhWjlCUWgwQ0RNczFDaXdDNmlxS3ZTRkowRHlqSmZwVDNzcFNNMUpXdGl5a1Utbk5BIIEC; bili_jct=3cf43fa12eb5e9c6f4112482566c9122; sid=dqo87h87; b_lsid=8CC43B10E_18DCF2880EE; bp_video_offset_594962304=900113484687081545; browser_resolution=1440-788; buvid_fp=17bf9927266dbdc2e8164a5cb0555037'''

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
#     "Host": "api.bilibili.com",
# }

# def getMixinKey(orig: str):
#     '对 imgKey 和 subKey 进行字符顺序打乱编码'
#     return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]

# def encWbi(params: dict, img_key: str, sub_key: str):
#     '为请求参数进行 wbi 签名'
#     mixin_key = getMixinKey(img_key + sub_key)
#     curr_time = round(time.time())
#     params['wts'] = curr_time                                   # 添加 wts 字段
#     params = dict(sorted(params.items()))                       # 按照 key 重排参数
#     # 过滤 value 中的 "!'()*" 字符
#     params = {
#         k : ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
#         for k, v 
#         in params.items()
#     }
#     query = urllib.parse.urlencode(params)                      # 序列化参数
#     wbi_sign = md5((query + mixin_key).encode()).hexdigest()    # 计算 w_rid
#     params['w_rid'] = wbi_sign
#     return params

# def getWbiKeys() -> tuple[str, str]:
#     '获取最新的 img_key 和 sub_key'
#     resp = requests.get('https://api.bilibili.com/x/web-interface/nav', headers=headers)
#     resp.raise_for_status()
#     json_content = resp.json()
#     img_url: str = json_content['data']['wbi_img']['img_url']
#     sub_url: str = json_content['data']['wbi_img']['sub_url']
#     img_key = img_url.rsplit('/', 1)[1].split('.')[0]
#     sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
#     return img_key, sub_key

# img_key, sub_key = getWbiKeys()

# signed_params = encWbi(
#     params={
#         'keyword': 'vue3'
#     },
#     img_key=img_key,
#     sub_key=sub_key
# )
# query = urllib.parse.urlencode(signed_params)
# print(signed_params)
# print(query)

# def search_bilibili(keyword: str):
#     '搜索关键词'
#     print(keyword)
#     resp = requests.get(f'https://api.bilibili.com/x/web-interface/wbi/search/all/v2?{query}', headers=headers)
#     resp.raise_for_status()
#     return resp.json()
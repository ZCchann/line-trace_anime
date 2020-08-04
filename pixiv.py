from pixivpy3 import *
import json

api = AppPixivAPI()
api.login("userbay", "userpay")   #游客登录

def download_day_illust(replyToken):
    msg = ""
    json_result = api.illust_ranking('day')
    for illust in json_result.illusts[:5]:  #取排行前5张图
        image_url = "https://www.pixiv.net/artworks/" + str(illust.id)
        msg += image_url + '\n\n'

    message = {  # line发送图片格式
        "replyToken": replyToken,
        "messages": [{
            "type": "text",
            "text": msg
        }]
    }
    return json.dumps(message)
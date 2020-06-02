from pixivpy3 import *
from datetime import datetime,timedelta
import os
import json

#读取json文件内的参数
seting = json.load(open("config.json",encoding='utf-8'))
image_file_url = seting["image_file_url"]

api = AppPixivAPI()
api.login("userbay", "userpay")   #游客登录

def download_day_illust(replyToken):
    message = {  # line发送图片格式
        "replyToken": replyToken,
        "messages": []
    }
    mode = "day_illust"
    now_time = datetime.now().strftime('%H:%M:%S') #pixiv排行榜12点更新，未到12点取前一日的排行
    if now_time < "11:00:00":
        # time = (datetime.now() + timedelta(days=-1)).strftime("%Y-%m-%d")
        data = {
            "type": "text",
            "text": "Pixiv排行榜还没更新哦 请在日本时间11点以后再尝试"
        }
        message["messages"].append(data)
        return json.dumps(message)
    else:
        time = datetime.now().strftime("%Y-%m-%d")
        directory = "/data/pixiv/" + mode + "/" + time  #图片文件目录
        if os.path.exists(directory):
            file_name = os.listdir(directory)
            for i in range(len(file_name)):
                url = image_file_url + mode + "/" + time + "/" + file_name[i]
                data = {
                    "type": "image",
                    "originalContentUrl": url,
                    "previewImageUrl": url
                }
                message["messages"].append(data)
            return json.dumps(message)
        else:
            os.makedirs(directory)
            json_result = api.illust_ranking('day')
            for illust in json_result.illusts[:5]:  #取排行前5张图
                image_url = illust.meta_single_page.get('original_image_url', illust.image_urls.large)
                url_basename = os.path.basename(image_url)
                extension = os.path.splitext(url_basename)[1] #文件后缀
                file_name = "id_%d%s" % (illust.id, extension)
                api.download(illust.image_urls.medium, path=directory,name=file_name)
                url = image_file_url + mode + "/" + time + "/" + file_name
                data = {
                    "type": "image",
                    "originalContentUrl": url,
                    "previewImageUrl": url
                }
                message["messages"].append(data)
            return json.dumps(message)
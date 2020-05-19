from pixivpy3 import *
import os
import time
import json

#读取json文件内的参数
seting = json.load(open("config.json",encoding='utf-8'))
image_file_url = seting["image_file_url"]

api = AppPixivAPI()
api.login("userbay", "userpay")   # Not required
time = str(time.strftime("%Y-%m-%d", time.localtime()))
directory = "/data/pixiv/" + time #创建文件夹

def download_day_illust(reply):
    message = {  # line发送图片格式
        "replyToken": reply,
        "messages": []
    }
    if os.path.exists(directory):
        file_name = os.listdir(directory)
        for i in range(len(file_name)):
            url = image_file_url + time + "/"+ file_name[i]
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
        for illust in json_result.illusts[:5]:
            image_url = illust.meta_single_page.get('original_image_url', illust.image_urls.large)
            url_basename = os.path.basename(image_url)
            extension = os.path.splitext(url_basename)[1] #文件后缀
            file_name = "id_%d%s" % (illust.id, extension)
            api.download(illust.image_urls.medium, path=directory,name=file_name)
            url = image_file_url + time + "/" + file_name
            data = {
                "type": "image",
                "originalContentUrl": url,
                "previewImageUrl": url
            }
            message["messages"].append(data)
        return json.dumps(message)
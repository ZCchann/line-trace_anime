from pixivpy3 import *
import os
import time
import json

#读取json文件内的参数
seting = json.load(open("config.json",encoding='utf-8'))
domain = seting["server_domain"]

api = AppPixivAPI()
api.login("userbay", "userpay")   # Not required
directory = "pixiv/" + str(time.strftime("%Y-%m-%d", time.localtime())) #创建文件夹

def download_day_illust():
    if os.path.exists(directory):
        file_name = os.listdir(directory)
        url = []
        for i in range(len(file_name)):
           url.append(domain + "/" +directory + "/"+ file_name[i] )
        return url
    else:
        os.makedirs(directory)
        json_result = api.illust_ranking('day')
        file_name = []
        for illust in json_result.illusts[:5]:
            image_url = illust.meta_single_page.get('original_image_url', illust.image_urls.large)
            url_basename = os.path.basename(image_url)
            extension = os.path.splitext(url_basename)[1] #文件后缀
            name = "id_%d%s" % (illust.id, extension)
            file_name.append("zcchann.top"+ "/" + directory + "/" + name)
            api.download(illust.image_urls.medium, path=directory,name=name)
        return file_name
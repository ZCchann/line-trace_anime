import requests
import json
def tra_image(reply_Token, image_url, number, files):
    response = requests.post(url=image_url, files=files)  # 获取trace.moe的返回信息
    response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
    result = response.json()  # 转换成json格式
    if result["header"]["status"] == -2:
        vaule = "今日机器人搜索次数已达上限 请于24小时后再进行搜索"
    elif result["header"]["status"] != -2:
        try:
            similarity = result['results'][0]['header']['similarity']  # 相似度
        except KeyError:
            similarity = ""
        try:
            jp_name = result['results'][0]['data']['jp_name']
        except KeyError:
            jp_name = ""
        try:
            ext_urls = result['results'][0]['data']['ext_urls'][0]
        except KeyError:
            ext_urls = ""
        try:
            pixiv_id = int(result['results'][0]['data']['pixiv_id'])
        except KeyError:
            pixiv_id = ""
        try:
            member_name = result['results'][0]['data']['member_name']
        except KeyError:
            member_name = ""
        try:
            title = result['results'][0]['data']['title']
        except KeyError:
            title = ""
        vaule = "相似度 " + str(similarity) + '%' + '\n' + "作者名称 " + str(member_name) + '\n' + "图片名称 " + str(
            title) + '' + jp_name + '\n' + "P站id " + str(pixiv_id) + '\n' + "图片链接 " + '\n' + ext_urls
    huifu = {
        "replyToken": reply_Token,
        "messages": [{
            "type": "text",
            "text": vaule + '\n' + "本日机器人搜索剩余次数" + str(number[0])
        }]
    }
    return json.dumps(huifu)


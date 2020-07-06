#!/usr/bin/python3
from flask import Flask, request
from linebot import LineBotApi
from image import *
from reply_message import *
from bangumi import *
from number import *
from pixiv import *
import json
import requests
import logging
import base64
import hashlib
import hmac

# 设置日志
logging.basicConfig(filename="var/app.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 读取json文件内的参数
seting = json.load(open("config.json", encoding='utf-8'))
line_bot = seting["line_bot_Channel_access_token"]
saucenao_key = seting["saucenao_api_key"]
line_bot_hannel = seting["line_bot_Channel_secret"]
domain = seting["server_domain"]

app = Flask(__name__)

line_bot_api = LineBotApi(line_bot)
line_bot_token = line_bot
handler = line_bot_hannel
reply_url = "https://api.line.me/v2/bot/message/reply"  # line bot replyAPI地址
saucenao_url = 'https://saucenao.com/search.php?db=999&output_type=2&testmode=1&numres=16&api_key='  # saucenaoAPI地址
trace_moe_url = 'https://trace.moe/api/search?url='  # trace.moe的api地址
image_number = [190]  # saucenao每日搜索上限 默认上限为200 除非你有氪金 建议设置200以内
bangumi_number = [150]
image_userid_list = []  # 存放"搜索图片"用户id
bangumi_userid_list = []  # 存放"识别番剧"用户ID
trace_image_text = ["搜索图片", "搜索圖片"]
trace_bangumi_text = ["识别番剧截图", "識別番劇圖片"]

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)  # 接收传递来的信息
    channel_secret = line_bot_hannel  # Channel secret string
    hash = hmac.new(channel_secret.encode('utf-8'),
                    body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    i = eval(body)
    reply = i["events"][0]["replyToken"]
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + "{" + line_bot_token + "}",
    }
    push_type = i["events"][0]["message"]["type"]  # line推送过来的类型
    try:
        push_text = i["events"][0]["message"]["text"]  # line推送过来的类型为文本
    except KeyError:
        push_text = ""
    push_userid = i["events"][0]["source"]["userId"]  # line推送过来的用户id
    if push_type == "text" and push_text in trace_image_text:
        requests.post(url=reply_url, data=reply_message(reply), headers=header)
        if push_userid not in image_userid_list:
            image_userid_list.append(push_userid)
    elif push_type == "text" and push_text in trace_bangumi_text:
        requests.post(url=reply_url, data=reply_message(reply), headers=header)
        if push_userid not in bangumi_userid_list:
            bangumi_userid_list.append(push_userid)
    elif push_type == "text" and push_text == "查询次数":
        requests.post(url=reply_url, data=remaining_number(reply, image_number, bangumi_number), headers=header)
    elif push_type == "text" and push_text == "今日排行":
        requests.post(url=reply_url, data=download_day_illust(reply), headers=header)
    elif push_type == "image":
        image_id = i["events"][0]["message"]["id"]
        if push_userid in image_userid_list:
            if image_number[0] > 0:
                c = image_number[0] - 1  # 每发送一张图片 计数器-1
                image_number.clear()
                image_number.append(c)
                message_content = line_bot_api.get_message_content(image_id)  # 从line服务器下载图片到本地服务器
                with open("/data/images/" + image_id + ".jpg", 'wb') as fd:
                    for chunk in message_content.iter_content():
                        fd.write(chunk)
                images_url = domain + image_id + ".jpg"
                search_image_url = saucenao_url + saucenao_key + "&url=" + images_url
                requests.post(url=reply_url, data=tra_image(reply, search_image_url, image_number), headers=header)
                image_userid_list.remove(push_userid)
            elif image_number[0] == 0:
                requests.post(url=reply_url, data=error_message(reply), headers=header)
        elif push_userid in bangumi_userid_list:
            if bangumi_number[0] > 0:
                c = bangumi_number[0] - 1  # 每发送一张图片 计数器-1
                bangumi_number.clear()
                bangumi_number.append(c)
                message_content = line_bot_api.get_message_content(image_id)  # 从line服务器下载图片到本地服务器
                with open("/data/images/" + image_id + ".jpg", 'wb') as fd:
                    for chunk in message_content.iter_content():
                        fd.write(chunk)
                images_url = domain + image_id + ".jpg"
                trace_url = trace_moe_url + images_url
                requests.post(url=reply_url, data=tra_bangumi(reply, trace_url, bangumi_number), headers=header)
                bangumi_userid_list.remove(push_userid)
            elif bangumi_number[0] > 0:
                requests.post(url=reply_url, data=error_message(reply), headers=header)
    return 'OK'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

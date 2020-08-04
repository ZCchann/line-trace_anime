#!/usr/bin/python3
import config
import base64
import hashlib
import hmac
import io
import os
from flask import Flask, request
from linebot import LineBotApi
from linebot.models import TextSendMessage
from image import *
from reply_message import *
from bangumi import *
from number import *
from pixiv import *
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

executor = ThreadPoolExecutor(1)  # 设置异步线程1

line_bot_token = os.environ["line_bot_Channel_access_token"]
line_bot_secret = os.environ["line_bot_Channel_secret"]
saucenao_key = os.environ["saucenao_api_key"]

# line_bot = config.line_bot_Channel_access_token
# saucenao_key = config.saucenao_api_key
# line_bot_hannel = config.line_bot_Channel_secret

app = Flask(__name__)

line_bot_api = LineBotApi(line_bot_token)
handler = line_bot_secret
reply_url = "https://api.line.me/v2/bot/message/reply"  # line bot replyAPI地址
saucenao_url = 'https://saucenao.com/search.php?db=999&output_type=2&testmode=1&numres=16&api_key='  # saucenaoAPI地址
trace_moe_url = 'https://trace.moe/api/search?url='  # trace.moe的api地址
image_number = [190]  # saucenao每日搜索上限 默认上限为200 除非你有氪金 建议设置200以内
bangumi_number = [150]
image_userid_list = []  # 存放"搜索图片"用户id
bangumi_userid_list = []  # 存放"识别番剧"用户ID
group_image_userid_list = []  # 存放群组类型"搜索图片"用户id
group_bangumi_userid_list = []  # 存放群组类型"识别番剧"用户ID
trace_image_text = ["搜索图片", "搜索圖片"]
trace_bangumi_text = ["识别番剧截图", "識別番劇圖片"]
time = ""

@app.route("/callback", methods=['POST'])
def callback():
    executor.submit(reset_number)
    body = request.get_data(as_text=True)  # 接收传递来的信息
    hash = hmac.new(line_bot_secret.encode('utf-8'),
                    body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    i = eval(body)
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + "{" + line_bot_token + "}"
    }

    reply = i["events"][0]["replyToken"]  # 获取回复口令
    message_type = i["events"][0]["source"]["type"]  # 获取回复类型
    push_type = i["events"][0]["message"]["type"]  # line推送过来的类型
    push_userid = i["events"][0]["source"]["userId"]  # line推送过来的用户id
    try:
        push_text = i["events"][0]["message"]["text"]  # line推送过来的类型为文本
    except KeyError:
        push_text = ""

    # 用户推送命令
    if push_type == "text" and push_text in trace_image_text and message_type == "user":  # 私聊 搜索图片
        requests.post(url=reply_url, data=reply_message(reply), headers=header)
        if push_userid not in image_userid_list:
            image_userid_list.append(push_userid)
    elif push_type == "text" and push_text in trace_bangumi_text and message_type == "user":  # 私聊 识别番剧截图
        requests.post(url=reply_url, data=reply_message(reply), headers=header)
        if push_userid not in bangumi_userid_list:
            bangumi_userid_list.append(push_userid)
    elif push_type == "text" and push_text in trace_image_text and message_type == "group":  # 群聊 搜索图片
        requests.post(url=reply_url, data=reply_message(reply), headers=header)
        if push_userid not in image_userid_list:
            group_image_userid_list.append(push_userid)
    elif push_type == "text" and push_text in trace_bangumi_text and message_type == "group":  # 群聊 识别番剧截图
        requests.post(url=reply_url, data=reply_message(reply), headers=header)
        if push_userid not in bangumi_userid_list:
            group_bangumi_userid_list.append(push_userid)
    elif push_type == "text" and push_text == "查询次数":
        requests.post(url=reply_url, data=remaining_number(reply, image_number, bangumi_number), headers=header)
    elif push_type == "text" and push_text == "今日排行":
        requests.post(url=reply_url, data=download_day_illust(reply), headers=header)
    # 用户推送图片
    elif push_type == "image":
        image_id = i["events"][0]["message"]["id"]
        if push_userid in image_userid_list and message_type == "user":  # 私聊搜素图片
            if image_number[0] > 0:
                c = image_number[0] - 1  # 每发送一张图片 计数器-1
                image_number.clear()
                image_number.append(c)
                image_userid_list.remove(push_userid)
                img = download_image(image_id)
                files = {'file': ("image.png", img.getvalue())}
                search_image_url = saucenao_url + saucenao_key
                requests.post(url=reply_url, data=tra_image(reply, search_image_url, image_number, files),
                              headers=header)
            elif image_number[0] == 0:
                requests.post(url=reply_url, data=error_message(reply), headers=header)
        elif push_userid in bangumi_userid_list and message_type == "user":  # 私聊识别番剧截图
            if bangumi_number[0] > 0:
                c = bangumi_number[0] - 1  # 每发送一张图片 计数器-1
                bangumi_number.clear()
                bangumi_number.append(c)
                bangumi_userid_list.remove(push_userid)
                img = download_image(image_id)
                files = {'image': ("image.png", img.getvalue())}
                trace_url = trace_moe_url
                requests.post(url=reply_url, data=tra_bangumi(reply, trace_url, bangumi_number, files),
                              headers=header)
            elif bangumi_number[0] > 0:
                requests.post(url=reply_url, data=error_message(reply), headers=header)
        elif push_userid in group_image_userid_list and message_type == "group":  # 群聊搜索图片
            if image_number[0] > 0:
                c = image_number[0] - 1  # 每发送一张图片 计数器-1
                image_number.clear()
                image_number.append(c)
                group_image_userid_list.remove(push_userid)
                img = download_image(image_id)
                files = {'image': ("image.png", img.getvalue())}
                search_image_url = saucenao_url + saucenao_key
                requests.post(url=reply_url, data=tra_image(reply, search_image_url, image_number, files),
                              headers=header)
            elif bangumi_number[0] > 0:
                requests.post(url=reply_url, data=error_message(reply), headers=header)
        elif push_userid in group_bangumi_userid_list and message_type == "group":  # 群聊识别番剧截图
            if bangumi_number[0] > 0:
                c = bangumi_number[0] - 1  # 每发送一张图片 计数器-1
                bangumi_number.clear()
                bangumi_number.append(c)
                group_bangumi_userid_list.remove(push_userid)
                img = download_image(image_id)
                files = {'file': ("image.png", img.getvalue())}
                trace_url = trace_moe_url
                requests.post(url=reply_url, data=tra_bangumi(reply, trace_url, bangumi_number, files),
                              headers=header)
            elif bangumi_number[0] > 0:
                requests.post(url=reply_url, data=error_message(reply), headers=header)
    return 'OK'


def reset_number():
    global time
    nowtime = datetime.now().strftime("%Y-%m-%d")
    if nowtime == time:
        pass
    else:
        image_number.clear()
        bangumi_number.clear()
        image_number.append(190)
        bangumi_number.append(150)
        time = nowtime


def download_image(image_id):
    print(image_id)
    message_content = line_bot_api.get_message_content(image_id)  # 从line服务器下载图片到本地服务器
    img = io.BytesIO()
    for chunk in message_content.iter_content():
        img.write(chunk)
    return img


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

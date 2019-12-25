from flask import Flask, request
from linebot import LineBotApi
import json
import requests
import logging
import base64
import hashlib
import hmac

#设置日志
logging.basicConfig(filename="./trace.log",format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#读取json文件内的参数
set = open("config.json",encoding='utf-8')
seting = json.load(set)
line_bot = seting["line_bot_Channel_access_token"]
saucenao_key = seting["saucenao_api_key"]
line_bot_hannel = seting["line_bot_Channel_secret"]
domain = seting["server_domain"]

app = Flask(__name__)

line_bot_api = LineBotApi(line_bot)
line_bot_token = line_bot
handler = line_bot_hannel
saucenao_url = 'https://saucenao.com/search.php?db=999&output_type=2&testmode=1&numres=16&api_key='

number = [190]  #saucenao每日搜索上限 默认上限为200 除非你有氪金 建议设置200以内

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)  # 接收传递来的信息
    channel_secret = line_bot_hannel  # Channel secret string
    hash = hmac.new(channel_secret.encode('utf-8'),
                    body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    i = eval(body)

    reply_url = "https://api.line.me/v2/bot/message/reply"
    reply = i["events"][0]["replyToken"]
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + "{" + line_bot_token + "}",
    }

    if number[0] != 0:
        if i["events"][0]["message"]["type"] == "image":
            c = number[0] -1   #每发送一张图片 计数器-1
            number.clear()
            number.append(c)
            if i["events"][0]["message"]["type"] == "image":
                image_id = i["events"][0]["message"]["id"]

                message_content = line_bot_api.get_message_content(image_id)  # 从line服务器下载图片到本地服务器
                with open("/data/images/" + image_id + ".jpg", 'wb') as fd:
                    for chunk in message_content.iter_content():
                        fd.write(chunk)

                images_url = domain + image_id + ".jpg"
                search_image_url = saucenao_url + saucenao_key + "&url="
                response = requests.get(url=search_image_url + images_url)  # 获取trace.moe的返回信息
                response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
                result = response.json()  # 转换成json格式
                try:
                    status = result["header"]["status"]
                except:
                    status = 1

                if status < 1:
                    vaule = "今日机器人搜索次数已达上限 请于24小时后再进行搜索"
                else:
                    similarity = result['results'][0]['header']['similarity']  # 相似度
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
                        "replyToken": reply,
                        "messages": [{
                            "type": "text",
                            "text": vaule + '\n' + "本日机器人搜索剩余次数" + number[0]
                    }]
                    }
                    requests.post(url=reply_url, data=json.dumps(huifu), headers=header)

    elif number[0] <= 0:
        vaule = "今日机器人搜索次数已达上限 请于24小时后再进行搜索"
        huifu = {
            "replyToken": reply,
            "messages": [{
                "type": "text",
                "text": vaule
            }]
        }
        requests.post(url=reply_url, data=json.dumps(huifu), headers=header)

    return 'OK'

if __name__ == "__main__":
    app.run(port='5000')
from flask import Flask, request
from linebot import LineBotApi
import json
import requests

#读取json文件内的参数
set = open("seting.json",encoding='utf-8')
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
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']  # 获取header
    body = request.get_data()  # 接收传递来的信息
    i = eval(body)

    if i["events"][0]["message"]["type"] == "image":
        image_id = i["events"][0]["message"]["id"]

        message_content = line_bot_api.get_message_content(image_id) #从line服务器下载图片到本地服务器
        with open("/data/images"+ image_id + ".jpg", 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)

        images_url = domain + image_id + ".jpg"
        search_image_url = saucenao_url + saucenao_key + "&url="
        response = requests.get(url=search_image_url+images_url)  # 获取trace.moe的返回信息
        response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
        result = response.json()  # 转换成json格式
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
        reply_url = "https://api.line.me/v2/bot/message/reply"
        reply = i["events"][0]["replyToken"]
        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + "{" + line_bot_token + "}",
        }
        huifu = {
            "replyToken": reply,
            "messages": [{
                "type": "text",
                "text": "相似度 " + str(similarity) + '%' + '\n' +
                                   "作者名称 " + str(member_name) + '\n' +
                                   "图片名称 " + str(title) + '' + jp_name + '\n' +
                                   "P站id " + str(pixiv_id) + '\n' +
                                   "图片链接 " + '\n' + ext_urls
            }]
        }
        requests.post(url=reply_url, data=json.dumps(huifu), headers=header)
        return json.dumps(huifu)


if __name__ == "__main__":
    app.run()
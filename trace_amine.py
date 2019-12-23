from flask import Flask, request, jsonify
from linebot import LineBotApi
import json
import requests

app = Flask(__name__)

line_bot_api = LineBotApi('SWQQkQbKu6C9n2L+a5A8sYEQqVdye8AyMqp3ONESJep23DRDC8tvb/28opljLgrROChzq7IX04xPpC07OG5vTc46B9+w2orifRVma144fnVZ6bZkoG2PmEEcn0+rEJQGLXXAsgacLxBHrs4XXuOdWgdB04t89/1O/w1cDnyilFU=')

line_bot_token = 'SWQQkQbKu6C9n2L+a5A8sYEQqVdye8AyMqp3ONESJep23DRDC8tvb/28opljLgrROChzq7IX04xPpC07OG5vTc46B9+w2orifRVma144fnVZ6bZkoG2PmEEcn0+rEJQGLXXAsgacLxBHrs4XXuOdWgdB04t89/1O/w1cDnyilFU='
handler = '648c59363849c97a023fe40ea27fd04d'

search_image_url = 'https://saucenao.com/search.php?db=999&output_type=2&testmode=1&numres=16&api_key=91835487587906f735bad34ebe8e9519ec7ef72e&url='
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']  # 获取header
    # get request body as text
    body = request.get_data()  # 接收传递来的信息
    i = eval(body)

    if i["events"][0]["message"]["type"] == "image":
        image_id = i["events"][0]["message"]["id"]
        message_content = line_bot_api.get_message_content(image_id)
        with open("/"+ image_id + ".jpg", 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)

        images_url = "https://zcchann.top/" + image_id + ".jpg"
        response = requests.get(url=search_image_url+images_url)  # 获取trace.moe的返回信息
        response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
        result = response.json()  # 转换成json格式
        print(type(result))


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
    app.run(debug=True)
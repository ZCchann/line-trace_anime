from flask import Flask, request, abort
import json
import requests

app = Flask(__name__)

line_bot_api = LineBotApi('SWQQkQbKu6C9n2L+a5A8sYEQqVdye8AyMqp3ONESJep23DRDC8tvb/28opljLgrROChzq7IX04xPpC07OG5vTc46B9+w2orifRVma144fnVZ6bZkoG2PmEEcn0+rEJQGLXXAsgacLxBHrs4XXuOdWgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('648c59363849c97a023fe40ea27fd04d')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']  #获取header
    print("header是 " + signature)
    # get request body as text
    body = request.get_data(as_text=True)  #接收传递来的信息
    if body["message"]["type"] == "image":
        reply_url = "https://api.line.me/v2/bot/message/reply"
        reply = body["replyToken"]
        huifu = {
            "Content-Type":"application/json",
            "Authorization":"Bearer "+"{"+line_bot_api+"}",
            "replyToken":reply,
            "messages":[{
                "type": "text",
                "text":"123456"
            }]
        }
        return json.dumps(huifu)

if __name__ == "__main__":
    app.run(port='5000')
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('SWQQkQbKu6C9n2L+a5A8sYEQqVdye8AyMqp3ONESJep23DRDC8tvb/28opljLgrROChzq7IX04xPpC07OG5vTc46B9+w2orifRVma144fnVZ6bZkoG2PmEEcn0+rEJQGLXXAsgacLxBHrs4XXuOdWgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('648c59363849c97a023fe40ea27fd04d')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']  #获取header

    # get request body as text
    body = request.get_data(as_text=True)  #接收传递来的信息
    print("传递来的消息" + body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))
    if event.message.text == "搜索图片":
        line_bot_api.reply_message(
            event.reply_token,
        TextSendMessage(text="请发送图片")
            )



if __name__ == "__main__":
    app.run()
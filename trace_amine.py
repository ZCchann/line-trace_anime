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

channel_access_token = 'SWQQkQbKu6C9n2L+a5A8sYEQqVdye8AyMqp3ONESJep23DRDC8tvb/28opljLgrROChzq7IX04xPpC07OG5vTc46B9+w2orifRVma144fnVZ6bZkoG2PmEEcn0+rEJQGLXXAsgacLxBHrs4XXuOdWgdB04t89/1O/w1cDnyilFU='
channel_secret = '648c59363849c97a023fe40ea27fd04d'
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='hello,'+event.message.text))

@handler.default()
def default(event):
    print(event)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Currently Not Support None Text Msg'))
    pass


if __name__ == "__main__":
    app.run()
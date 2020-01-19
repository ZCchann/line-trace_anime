import json

def reply_message(replyToken):
    huifu = {
        "replyToken": replyToken,
        "messages": [{
            "type": "text",
            "text": "请发送图片",
            "quickReply": {    #quickReply模块 调用line相簿
                "items": [
                    {
                        "type": "action",
                        "action": {
                            "type": "cameraRoll",
                            "label": "点我发送图片"
                                    }
                    }
                ]
            }
        }
    ]
    }
    return json.dumps(huifu)

def error_message(replyToken):
    huifu = {
        "replyToken": replyToken,
        "messages": [{
            "type": "text",
            "text": "今日机器人搜索次数已达上限 请于24小时后再进行搜索"
        }]
    }
    return json.dumps(huifu)

import json

def reply_message(replyToken):
    huifu = {
        "replyToken": replyToken,
        "messages": [{
            "type": "text",
            "text": "请发送完整图片，屏幕截图、部分截图等有黑边或非图片信息资讯的内容会造成搜索结果有误",
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

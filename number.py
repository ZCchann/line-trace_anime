import json

def remaining_number(reply_Token,image_number,bangumi_number):
    huifu = {
        "replyToken": reply_Token,
        "messages": [{
            "type": "text",
            "text": "搜图剩余次数:" + str(image_number[0]) + "\n" +
                    "识别番剧剩余次数:" + str(bangumi_number[0])
        }]
    }
    return json.dumps(huifu)
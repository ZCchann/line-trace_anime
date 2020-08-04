import requests
import json

def tra_bangumi(reply_Token, trace_url, image_remaining_number, files):
    response = requests.post(trace_url, files=files)  # 获取trace.moe的返回信息
    response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
    result = response.json()  # 转换成dict格式
    js = json.dumps(result, sort_keys=True, indent=4, separators=(',', ':'))
    animename = result["docs"][0]["title_chinese"]  # 切片番剧名称
    similarity = result["docs"][0]["similarity"]  # 切片相似度
    time = result["docs"][0]["at"]  # 切片时间
    episode = result["docs"][0]["episode"]  # 切片集数
    try:
        decimal = "." + str(similarity * 100).split('.')[1][:2]   #切片小数点后的内容 如果为空则不返回
    except IndexError:
        decimal = ""
    huifu = {
        "replyToken": reply_Token,
        "messages": [{
            "type": "text",
            "text": "番剧名称：" + animename + " 第" + str(episode) + "集" + '\n'
                     "相似度：" + str(similarity * 100).split('.')[0] + decimal + "%" + '\n'
                    + "时间：" + str(time / 60).split('.')[0]
                    + '分' + str(time % 60).split('.')[0] + "秒" + '\n' +
                    "本机器人今日剩余搜索次数" + str(image_remaining_number)
        }]
    }
    return json.dumps(huifu)

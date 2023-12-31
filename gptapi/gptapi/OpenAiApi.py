# -*- coding: utf-8 -*-
# 对接ChatGPT
from requests import post as requests_post


def getlength(text):  # 字符串计算
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text, max_context):  # 字符串列表删除
    checklen_len = len(text)
    text_len = 0
    checklen_text = text
    while (getlength(checklen_text) > max_context):
        text_len += 1
        if text_len == checklen_len:
            txt = checklen_text[-1]['content'][:max_context]
            checklen_text[-1]['content'] = txt
        else:
            del checklen_text[0]
    return checklen_text


# 聊天对话
def generate_text(prompt,api_config):
    """
    :param prompt: 历史对话内容，[{},{}]
    :param api_config: ChatGPT的API配置信息
    :return: 返回聊天系统的对话
    """
    try:
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_config['api_key']}"}
        prompt = checklen(prompt,api_config['max_context'])
        data = {
            "messages": prompt,
            "model": api_config['model'],
            "max_tokens": api_config['max_tokens'],
            "temperature": api_config['temperature'],
        }
        try:
            response = requests_post(api_config['url'], headers=headers, json=data)
        except Exception as e:
            return {"code": False, "mes": f'连接不上 {api_config["url"]} 的服务器，可能是网络问题！ 请更换代理！\n {e}'}
        if response.status_code == 200:
            completions = response.json()["choices"][0]['message']["content"]  # 获取信息内容
            if response.json()["usage"]['completion_tokens'] < data['max_tokens']:
                return {"code": True, "mes": completions}
            else:
                return {"code": True, "mes": completions + f'\n 回复太多，仅显示部分！仅显示{api_config["max_tokens"]}个token'}
        if response.status_code == 401:
            if response.json()['error']['code'] is None:
                return {"code": False, "mes": f'请填写api_key！\n\n{response.text}'}
            if response.json()['error']['code'] == 'invalid_api_key':
                return {"code": False, "mes": f'api_key不对，请检查！\n\n{response.text}'}
            return {"code": False, "mes": f'错误，地址：{api_config["url"]}\n\n提示信息：\n\n{response.text}'}
        if response.status_code == 400:
            return {"code": False, "mes": f'信息有误或返回太大！返回信息： {response.text}'}
        if response.status_code == 429:
            return {"code": False, "mes": 'api没有额度或其他：' + response.json()["error"]["message"]}
        if response.status_code == 404:
            return {"code": False, "mes": '该模型可能不支持：' + response.json()["error"]["message"]}
        return {"code": False, "mes": f'api返回的信息好像有问题，信息返回：{response.text}'}
    except Exception as e:
        return {"code": False, "mes": f'对接ChatGPT 程序出错了！暂时不清楚情况！{e}'}


# 图片生成
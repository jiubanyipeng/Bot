# coding:utf-8
import websocket
from json import dumps as json_dumps, loads as json_loads
from requests import post as requests_post
from os import makedirs as os_makedirs
from time import localtime, time, strftime
from asyncio import run as asyncio_run
import SparkApi  # 讯飞模型接口，由于用websocket进行通讯，和cqhttp冲突只能分开


# 异步写入文件
async def write_json(file_path, data):
    try:
        with open(f'./BotLog/{file_path}.log', 'a', encoding='utf-8') as file:
            file.write(data)
    except PermissionError:
        return {'code': False, 'mes': f'文件:{file_path},无写入权限'}
    except Exception as e:
        return {'code': False, 'mes': e}


# 对话数据处理，将对话数据进行切割
def chat_manage(user_id, role, chat_content, message_type, group_id='0'):
    def getText(context):  # 对话的字符串修改
        jsoncon = {"role": role, "content": context}
        text.append(jsoncon)
        return text

    def getlength(text):  # 字符串计算
        length = 0
        for content in text:
            temp = content["content"]
            leng = len(temp)
            length += leng
        return length

    def checklen(text):  # 字符串列表删除
        checklen_text = text
        while (getlength(checklen_text) > bot_config['max_tokens']):  # 目前大部分的模型仅支持到8192
            del checklen_text[0]
        return checklen_text

    group_pass = False

    # 会话初始化处理
    if message_type == 'group':
        if user_id not in chat_json:
            chat_json[user_id] = {'group': {group_id: {'chat_data': []}}}
        elif 'group' not in chat_json[user_id]:
            chat_json[user_id]['group'] = {group_id: {'chat_data': []}}
        elif group_id not in chat_json[user_id]['group']:
            chat_json[user_id]['group'][group_id] = {'chat_data': []}

        text = chat_json[user_id]['group'][group_id]['chat_data']
        group_pass = True
    else:
        if user_id not in chat_json:
            chat_json[user_id] = {'private': {'chat_data': []}}
        elif 'private' not in chat_json[user_id]:
            chat_json[user_id]['private'] = {'chat_data': []}

        text = chat_json[user_id]['private']['chat_data']
    if group_pass:
        if role == 'assistant':
            chat_json[user_id]['group'][group_id]['chat_data'] = getText(chat_content)
        else:
            chat_json[user_id]['group'][group_id]['chat_data'] = checklen(getText(chat_content))
            return text
    else:
        if role == 'assistant':
            chat_json[user_id]['private']['chat_data'] = getText(chat_content)
        else:
            chat_json[user_id]['private']['chat_data'] = checklen(getText(chat_content))
            return text


# 对接ChatGPT的挨批接口模型
def generate_text(prompt):
    try:
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_config['api_key']}"}
        data = {
            "messages": prompt,
            "model": api_config['model'],
            "max_tokens": api_config['max_tokens'],
            "temperature": api_config['temperature'],
        }
        try:
            response = requests_post(api_config['url'], headers=headers, json=data)
        except Exception as e:
            return {"code": False, "mes": f'连接不上 {url} 的服务器，可能是网络问题！ 请更换代理！\n {e}'}
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
            return {"code": False, "mes": f'错误，地址：{url}\n\n提示信息：\n\n{response.text}'}
        if response.status_code == 400:
            return {"code": False, "mes": f'信息有误或返回太大！返回信息： {response.text}'}
        if response.status_code == 429:
            return {"code": False, "mes": 'api没有额度或其他：' + response.json()["error"]["message"]}
        if response.status_code == 404:
            return {"code": False, "mes": '该模型可能不支持：' + response.json()["error"]["message"]}
        return {"code": False, "mes": f'api返回的信息好像有问题，信息返回：{response.text}'}
    except Exception as e:
        return {"code": False, "mes": f'对接ChatGPT 程序出错了！暂时不清楚情况！{e}'}


# API对接使用
def run_api(chat_data):
    mes = {'code': False, 'mes': 'API对接函数错误'}
    if bot_config['api_name'] == "xunfei":
        SparkApi.main(api_config, chat_data)  # 执行，返回的是完成的，将原先的流式返回注释了,注意这里的报错没有进行处理
        mes = {'code': True, 'mes': SparkApi.answer}
        SparkApi.answer = ''  # 重新清空缓存，防止会话速度太快将问题继续进行访问，但会严重影响响应速度
    elif bot_config['api_name'] == "openai":
        mes = generate_text(chat_data)  # 发送数据并返回答案,返回的是字典
    return mes


# 消息发送通用封装
def send_msg(mes_data, user_id, type='group', group_id='0'):  # 消息是否为真、回复给谁、回复类型
    user_id = int(user_id)
    if type == 'private':
        data_mes = {"action": "send_msg",
                    "params": {"message_type": 'private', "user_id": user_id, 'message': mes_data['mes']}}
    else:
        data_mes = {"action": "send_group_msg",
                    "params": {"group_id": group_id, "message": f"[CQ:at,qq={user_id}] {mes_data['mes']}"}}

    return json_dumps(data_mes)  # 返回字符串形式的数据


# 客户端接收服务端数据时触发
def on_message(ws, message):
    data = json_loads(message)

    # 减少cqhttp之间的通信，返回非信息不进行通信
    if data.get('post_type', '') != "message":
        return False

    private_code, group_code = True, True  # 账号权限验证信息是否允许
    user_id = str(data.get('user_id', '0'))  # 将数字账号转为字符串账号
    user_mes_list = []

    if qq_config['private_disabled']:  # 是否启用私发仅允许部分账号
        if user_id not in qq_config['permit_group']:
            private_code = False

    if qq_config['group_disabled']:  # 是否启用群发仅允许部分账号
        if user_id not in qq_config['permit_group']:
            group_code = False
    # 信息和账号验证
    if private_code and data['message_type'] == 'private':
        user_mes_list = chat_manage(user_id, 'user', data["message"], data['message_type'])
        send_code = True
    elif group_code and data['message_type'] == 'group':
        # 判断是否是 @ 机器人的消息
        if f"[CQ:at,qq={data.get('self_id')}]" in data.get("message"):  # @123 @123你好
            sickle_mes = data["message"].replace(f'[CQ:at,qq={data["self_id"]}]', '').strip()  # 将群信息@替换处理，仅保留信息内容
            data.update({'message': sickle_mes})
            user_mes_list = chat_manage(user_id, 'user', sickle_mes, data['message_type'], data['group_id'])
            send_code = True
        else:
            # 不是@机器人，所以不进行回复，如果进行回复还需要做机器人信息回复的处理
            return False
    else:
        send_code = False

    # 信息发送确认
    if send_code:
        mes = run_api(user_mes_list)
        if mes['code']:
            chat_manage(user_id, 'assistant', mes['mes'], data['message_type'],
                        data.get('group_id', ''))  # 将api对话添加到缓存会话中
            # 这里是写入日志
            if bot_config['bot_chat_log']:
                log_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
                mes_log = f"[{log_time}] [{data['message_type']}:{data.get('group_id', '')}:{user_id}] \n[user:{data['message']}]\n[assistant:{mes['mes']}]\n"
                asyncio_run(write_json(user_id, mes_log))
        else:
            mes = {'code': False, 'mes': 'api 接口返回错误，请检查！'}
    else:
        # 这里是账号权限没有通过的，这里应该直接结束还是提示账号不允许，等待考虑
        mes = {'code': False, 'mes': '对不起，您的账号不在允许范围，详情请询问 玖伴一鹏'}
    data_mes = send_msg(mes, user_id, data.get('message_type'), data.get('group_id', '0'))
    ws.send(data_mes)


# 通信发生错误时触发
def on_error(ws, error):
    print("{}返回错误:{}".format(ws, error))


# 连接关闭时触发
def on_close(ws):
    print("### 关闭 ###")


# 连接建立时触发
def on_open(ws):
    ws.send('{"action":get_msg, "params":{"message_id":1}')  # 获取消息


chat_json = {}  # 对话缓存变量
qq_config = {}  # qq配置文件
api_config = {}  # 对接API平台的配置文件
bot_config = {}  # 全部的配置文件信息

if __name__ == "__main__":
    try:
        os_makedirs('BotLog', exist_ok=True)  # 创建日志文件夹
        with open('setting_config.json', 'r', encoding='utf-8') as f:
            bot_config = json_loads(f.read())
        api_name = bot_config['api_name']
        api_config = bot_config[f'{api_name}_config']
        access_token = bot_config['access_token']  # 你设置的access_token
        url = bot_config['cqhttp_url']  # cqhttp运行的 ip:端口 或 域名:端口
        qq_config = bot_config['qq_config']
        websocket.enableTrace(False)  # websocket信息显示
        ws = websocket.WebSocketApp(f"ws://{url}/?access_token={access_token}", on_message=on_message,
                                    on_error=on_error, on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()
    except Exception as e:
        print('配置文件有问题，请检查，以下是报错信息：\n', e)

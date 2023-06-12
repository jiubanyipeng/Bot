import websocket
from json import load as json_load,dump as json_dump,dumps as json_dumps,loads as json_loads
from requests import post as requests_post
from os import makedirs as os_makedirs,path,stat
from time import strftime,localtime
from asyncio import run as asyncio_run
from time import sleep
# 应该要添加一个配置文件重新载入的功能和清除这些会话的缓存
# 使用异步请求将性能优化,api接口每一秒只允许请求三次，感觉没有必要进行优化
# 进一步优化连续提交的信息 目前是根据天，后面应该是前十条信息，有可能不做修改


# 异步读文件
async def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json_load(file)
            return {'code': True, 'mes': data,'file_path':file_path}
    # except json.JSONDecodeError as e:
    #     pass
    except Exception as e:
        return {'code': False, 'mes': e}


# 异步写入文件，会根据原来的追加进行写入，文件数据格式为列表类型
async def write_json(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json_dump(data, file,ensure_ascii=False)
        return {'code': True, 'mes': '写入数据完成'}
    except PermissionError:
        return {'code': False, 'mes': f'文件:{file_path},无写入权限'}
    except Exception as e:
        return {'code': False, 'mes': e}


# 异步文件写操作
async def file_write(file_path,info):
    try:
        read_data = await read_json(file_path)
        if read_data['code']:  # 如果文件不存在或数据为空，初始化数据为空列表
            data = read_data['mes']
        else:
            data = []
        data.append(info)
        # 写入 JSON 文件
        return await write_json(file_path, data)  # 需要根据读文件返回文件的路径地址
    except Exception as e:
        return {'code': False, 'mes': e}


# 读取文件，会自动根据当前本地时间查询，文件和文件夹不存在会自动创建
def file_read(file_path):
    current_time = strftime("%Y-%m-%d", localtime())  # 2023-06-09
    openai_data_path = f'./openai_data/{current_time}'
    # 创建文件夹（如果不存在）
    os_makedirs(openai_data_path, exist_ok=True)
    data_path = f'{openai_data_path}/{file_path}.json'
    try:
        # 判断文件是否存在且数据不为空
        if path.isfile(data_path) and stat(data_path).st_size > 0:
            with open(data_path, 'r', encoding='utf-8') as file:
                data = json_load(file)
                return {'code': True, 'mes': data, 'file_path': data_path}
        else:
            with open(data_path, 'w', encoding='utf-8') as f:
                pass  # 文件不存在就会创建文件
            return {'code': True, 'mes': [], 'file_path': data_path}
    except FileNotFoundError:
        return {'code': False, 'mes': '文件不存在', 'file_path': data_path}
    except PermissionError:
        return {'code': False, 'mes': f'文件:{data_path},无读取权限'}
    except Exception as e:
        return {'code': False, 'mes': e}


# 对接ChatGPT模型
def generate_text(prompt):
    global global_api_key, global_model,global_proxy
    try:
        if len(global_proxy) < 3:
            url = 'https://api.chatgpt.com/v1/chat/completions'
        else:
            url = global_proxy
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_api_key}"}
        data = {
            "messages": prompt,  # [{},{}]
            "model": global_model,
            "max_tokens": 2000,
            "temperature": 0.5,
            "top_p": 1,
            "n": 1,
        }
        try:
            response = requests_post(url, headers=headers, json=data)
        except Exception as e:
            return {"code": False, "mes": f'连接不上 {url} 的服务器，可能是网络问题！ 请更换代理！'}
        if response.status_code == 200:
            completions = response.json()["choices"][0]['message']["content"]  # 获取信息内容
            if response.json()["usage"]['completion_tokens'] < data['max_tokens']:
                return {"code": True, "mes": completions}
            else:
                return {"code": True, "mes": completions + '\n 回复太多，仅显示部分！仅显示2000个字'}
        if response.status_code == 401:
            if response.json()['error']['code'] == None:
                return {"code": False, "mes": '请填写api_key！'}
            if response.json()['error']['code'] == 'invalid_api_key':
                return {"code": False, "mes": 'api_key不对，请检查！'}
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


# 消息发送通用封装
def send_msg(mes_data, user_id, type='group', group_id='0'):  # 消息是否为真、回复给谁、回复类型
    if type == 'private':
        data_mes = {"action": "send_msg",
                    "params": {"message_type": 'private', "user_id": user_id, 'message': mes_data['mes']}}
    else:
        data_mes = {"action": "send_group_msg",
                    "params": {"group_id": group_id, "message": f"[CQ:at,qq={user_id}] {mes_data['mes']}"}}

    return json_dumps(data_mes)  # 返回字符串形式的数据


# 将用户进行封装信息
def prompt(message,user_id):
    user_message_info = {"role": "user", "content": message}
    # 是否开启连续对话
    global global_continuous
    if global_continuous == 'true':
        # 先读取文件，文件不存在创建文件
        continuous_messagedata = file_read(user_id)
        if continuous_messagedata['code']:
            prompts = continuous_messagedata['mes']
            prompts.append(user_message_info)
        else:
            prompts = [user_message_info]

        return {'code': True, 'message': prompts, 'file_path':continuous_messagedata['file_path']}
    else:
        prompts = [user_message_info]
        return {'code': False, 'message': prompts}


# 客户端接收服务端数据时触发
def on_message(ws, message):
    global global_show_quiz, global_private_disabled
    data = json_loads(message)
    # 添加清除缓存功能和重新加载配置

    # 私人信息处理
    if data.get('message_type') == 'private':
        prompts = prompt(data.get("message"), data['user_id'])
        if global_show_quiz == 'true':
            message = {'code': True, 'mes': f'问题：{data.get("message")} \n 正在为您查询中......'}
            ws.send(send_msg(message, data['user_id'], 'private'))

        # 是否仅允许部分QQ
        if global_private_disabled == 'true':
            # 该账号是否存在允许范围
            global global_private_group
            if str(data['user_id']) in global_private_group:
                mes = generate_text(prompts['message'])  # 发送数据并返回答案,返回的是字典
                if mes['code'] and prompts['code']:
                    asyncio_run(file_write(prompts['file_path'], {"role": "user", "content":data.get("message")}))
                    asyncio_run(file_write(prompts['file_path'],{"role": "assistant", "content":mes['mes']}))
            else:
                mes = {'code': False, 'mes': '对不起，您的账号不在允许范围，详情请询问 玖伴一鹏'}

            data_mes = send_msg(mes, data['user_id'], 'private')
            ws.send(data_mes)
        else:
            mes = generate_text(prompts['message'])
            if mes['code'] and prompts['code']:
                asyncio_run(file_write(prompts['file_path'], {"role": "user", "content": data.get("message")}))
                asyncio_run(file_write(prompts['file_path'], {"role": "assistant", "content": mes['mes']}))
            data_mes = send_msg(mes, data['user_id'], 'private')
            ws.send(data_mes)

    # 群消息
    elif data.get('message_type') == 'group':
        # 判断是否是 @ 机器人的消息
        if f"[CQ:at,qq={data['self_id']}]" in data.get("message"):  # @123 @123你好
            sickle_mes = data.get("message").replace(f'[CQ:at,qq={data["self_id"]}]', '').strip()  # 将群信息@替换处理，仅保留信息内容
            prompts = prompt(sickle_mes, str(data['group_id']) + '-' +  str(data['user_id']))
            if global_show_quiz == 'true':
                mes_reply = {'code': True, 'mes': f'正在为您查询中......'}
                ws.send(send_msg(mes_reply, data['user_id'], group_id=data['group_id']))
            global global_group_disabled
            if global_group_disabled == "true":
                mes = {'code': False, 'mes': '对不起，暂时取消了对接的功能'}
            else:
                mes = generate_text(prompts['message'])
                if mes['code'] and prompts['code']:
                    asyncio_run(file_write(prompts['file_path'], {"role": "user", "content": sickle_mes}))
                    asyncio_run(file_write(prompts['file_path'], {"role": "assistant", "content": mes['mes']}))
            data_mes = send_msg(mes, data['user_id'], group_id=data['group_id'])  # 将信息发送到信息封装函数
            ws.send(data_mes)
        # 不管是不是@机器人都进行回复，暂时不做


# 通信发生错误时触发
def on_error(ws, error):
    print("{}返回错误:{}".format(ws, error))


# 连接关闭时触发
def on_close(ws):
    print("### 关闭 ###")


# 连接建立时触发
def on_open(ws):
    ws.send('{"action":get_msg, "params":{"message_id":1}')  # 获取消息


# 读配置文件
def read_setting():
    try:
        with open('./openai_config-1.1.json', 'r', encoding='utf-8') as f:
            data = json_loads(f.read())
            return {'code': True, 'mes': data}

    except Exception as e:
        return {'code': False, 'mes': e}


if __name__ == "__main__":
    data = read_setting()

    if data['code']:
        setting_mes = data['mes']
        access_token = setting_mes['access_token']  # 你设置的access_token
        url = setting_mes['url']  # ip:端口 或 域名:端口
        global_api_key = setting_mes['global_api_key']  # ChatGPT 的api-key
        global_model = setting_mes['global_model']  # openai的模型，目前免费版本中比较好的是这个，其他的模型没有测试过
        global_group_disabled = setting_mes['global_group_disabled']  # 默认在QQ群里面的@使用模型回答，yes则禁用，默认是全部人，不允许单个
        global_private_disabled = setting_mes['global_private_disabled']  # 是否仅允许指定的QQ号回答，yes则禁用
        global_private_group = setting_mes['global_private_group']  # 启用仅允许指定的QQ号回答，需要添加账号
        global_proxy = setting_mes['proxy']  # 代理
        global_show_quiz = setting_mes['show_quiz']  # 是否显示提出问题
        global_continuous = setting_mes['global_continuous']  # 是否连续提问
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(f"ws://{url}/?access_token={access_token}", on_message=on_message,
                                    on_error=on_error, on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()

    else:
        print('配置文件有问题！十秒后将自动退出，以下是报错信息：')
        print(data['mes'])
        sleep(10)


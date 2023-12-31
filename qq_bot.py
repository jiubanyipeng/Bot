# coding:utf-8
from asyncio import run as asyncio_run
from json import dumps as json_dumps, loads as json_loads
from os import makedirs as os_makedirs
from time import localtime, time, strftime, sleep
import websocket
from requests import get as requests_get
from gptapi import XunFeiApi, OpenAiApi, TongYiQianWen


# 异步写入文件
async def write_json(file_path, data):
    try:
        with open(f'./BotLog/qq/{file_path}.log', 'a', encoding='utf-8') as file:
            file.write(data)
    except PermissionError:
        return {'code': False, 'mes': f'文件:{file_path}.log,无写入权限'}
    except Exception as e:
        return {'code': False, 'mes': e}


# 聊天对话数据处理，将对话数据进行切割
def chat_manage(user_id, role, chat_content, message_type, group_id='0'):
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
            chat_json[user_id]['group'][group_id]['chat_data'] = {"role": 'assistant', "content":chat_content}
        else:
            chat_json[user_id]['group'][group_id]['chat_data'] = {"role": 'user', "content":chat_content}
            return text
    else:
        if role == 'assistant':
            chat_json[user_id]['private']['chat_data'] = {"role": 'assistant', "content":chat_content}
        else:
            chat_json[user_id]['private']['chat_data'] = {"role": 'user', "content":chat_content}
            return text


# 机器人指令处理
def bot_commands():
    pass


# 机器人配置文件修改操作
def bot_update():
    pass


# QQ聊天信息处理
def qq_char_processor(user_mes_list,user_id,user_mes,type='private',group_id='0'):
    mes = run_api(user_mes_list)
    # 将api对话添加到缓存会话中
    chat_manage(user_id, 'assistant', mes['mes'], type,group_id)

    # 这里是写入日志
    if bot_config['bot_chat_log']:
        log_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        mes_log = f"[{log_time}] [{type}:{group_id}:{user_id}] \n[user:{user_mes}]\n[assistant:{mes['mes']}]\n"
        asyncio_run(write_json(user_id, mes_log))

    data_mes = send_msg(mes, user_id, type, group_id)
    # sleep(0.5)  # 限制发送消息的速度
    ws.send(data_mes)


# QQ图片信息处理
def qq_picture_processor():
    pass


# GPT的API对接使用
def run_api(chat_data):
    mes = {'code': False, 'mes': 'API对接函数错误'}
    if bot_config['name_api'] == "xunfei_config":
        XunFeiApi.main(api_config, chat_data)  # 执行，返回的是完成的，将原先的流式返回注释了,注意这里的报错没有进行处理
        mes = {'code': True, 'mes': XunFeiApi.answer}
        XunFeiApi.answer = ''  # 重新清空缓存，防止会话速度太快将问题继续进行访问，但会严重影响响应速度
    elif bot_config['name_api'] == "openai_config":
        mes = OpenAiApi.generate_text(chat_data, api_config)  # 发送数据并返回答案,返回的是字典
    elif bot_config['name_api'] == "tyqw_config":
        mes = TongYiQianWen.generate_text(chat_data,api_config)
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
    user_id = str(data.get('user_id', '0'))  # 将数字账号转为字符串账号

    # 减少cqhttp之间的通信，返回非信息不进行通信
    if data.get('post_type', '') != "message":
        return False
    # 机器人指令
    if '/bot ' == data["message"][0:5]:
        if user_id in qq_config.get('admin_group', []):
            pass
        else:
            mes = {'code': False, 'mes': f'账号：{user_id} 不属于管理员'}
            ws.send(send_msg(mes, user_id, data.get('message_type'), data.get('group_id', '0')))
            return False
    # 信息和账号验证
    if data['message_type'] == 'private':
        if qq_config['private_disabled']:  # 是否启用私发仅允许部分账号
            if user_id not in qq_config['permit_group']:
                return False
        qq_char_processor(chat_manage(user_id, 'user', data["message"], data['message_type']),user_id,data["message"])
    elif data['message_type'] == 'group':
        # 判断是否是 @ 机器人的消息
        if f"[CQ:at,qq={data.get('self_id')}]" in data.get("message"):
            # 是否启用群发仅允许部分账号
            if qq_config['group_disabled']:
                if user_id not in qq_config['permit_group']:
                    return False
            sickle_mes = data["message"].replace(f'[CQ:at,qq={data["self_id"]}]', '').strip()  # 将群信息@替换处理，仅保留信息内容
            data.update({'message': sickle_mes})
            qq_char_processor(chat_manage(user_id, 'user', sickle_mes, data['message_type'], data['group_id']),user_id,sickle_mes)
        else:
            # 不是@机器人，所以不进行回复
            return


# 通信发生错误时触发
def on_error(ws, error):
    print("{}\n在和go-cqhttp进行通信发生错误:{}".format(ws, error))
    if '[WinError 10061]' in str(error):
        print('请检查配置文件与go-cqhttp的地址和端口是否正确，或go-cqhttp是否运行成功')


# 连接关闭时触发
def on_close(ws, close_status_code, close_msg):
    print("### 关闭对接程序 ###")
    sleep(3)


# 连接建立时触发
def on_open(ws):
    ws.send('{"action":get_msg, "params":{"message_id":1}')  # 获取消息


chat_json = {}  # 对话缓存变量
qq_config = {}  # qq配置文件
api_config = {}  # 对接API平台的配置文件
bot_config = {}  # 全部的配置文件信息

if __name__ == "__main__":
    try:
        os_makedirs('BotLog/qq', exist_ok=True)
        with open('setting_config.json', 'r', encoding='utf-8') as f:
            bot_config = json_loads(f.read())
        api_config = bot_config[bot_config['name_api']]
        access_token = bot_config['cqhttp']['access_token']
        url = bot_config['cqhttp']['cqhttp_url']
        qq_config = bot_config['qq_config']
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(f"ws://{url}/?access_token={access_token}", on_message=on_message,
                                    on_error=on_error, on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()
    except FileNotFoundError:
        print('对接的配置文件：setting_config 出现故障，请检查！\n如果配置文件不存在，将会创建，如果是权限不足给赋予读写文件权限。\n创建配置文件中...')
        try:
            url_config = 'https://www.jiubanyipeng.com/laboratory/gpt_qqbot/setting_config.json'  # 为了方便后期的维护更新
            setting_config = requests_get(url_config).text.replace('\r\n', '\n')  # 格式化为字符串，防止乱码和后期可能整改其它方案
            with open('./setting_config.json', 'w', encoding='utf-8') as f:
                f.write(setting_config)
                print('文件创建完成，请填写配置文件信息！')
                sleep(5)
        except Exception as e:
            print('远程文件无法访问，可能是本地网络问题或远程文件不存在，远程文件地址:')
    except Exception as e:
        print('以下是报错信息：\n', e)
        print('退出')
        sleep(10)


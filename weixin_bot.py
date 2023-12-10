# coding:utf-8
from flask import Flask, request
from os import makedirs as os_makedirs
from json import  loads as json_loads
from requests import post as requests_post, get as requests_get
from time import localtime, time, strftime, sleep
from asyncio import run as asyncio_run
from gptapi import XunFeiApi
import qq_bot

app = Flask(__name__)


# 异步写入文件
async def write_json(file_path, data):
    try:
        with open(f'./BotLog/weixin/{file_path}.log', 'a', encoding='utf-8') as file:
            file.write(data)
    except PermissionError:
        return {'code': False, 'mes': f'文件:{file_path}.log,无写入权限'}
    except Exception as e:
        return {'code': False, 'mes': e}


# 聊天对话数据处理，将对话数据进行切割，返回历史聊天记录，列表形式
def chat_manage(wxid, chat_content, role='user', roomid=''):
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
    # 私聊和群 初始会话化处理
    if len(roomid) > 1:  # 通过roomid判断是否为群信息
        if wxid not in chat_json:
            chat_json[wxid] = {'group': {roomid: {'chat_data': []}}}
        elif 'group' not in chat_json[wxid]:
            chat_json[wxid]['group'] = {roomid: {'chat_data': []}}
        elif roomid not in chat_json[wxid]['group']:
            chat_json[wxid]['group'][roomid] = {'chat_data': []}
        text = chat_json[wxid]['group'][roomid]['chat_data']
        group_pass = True
    else:
        if wxid not in chat_json:
            chat_json[wxid] = {'private': {'chat_data': []}}
        elif 'private' not in chat_json[wxid]:
            chat_json[wxid]['private'] = {'chat_data': []}
        text = chat_json[wxid]['private']['chat_data']

    if group_pass:
        if role == 'assistant':
            chat_json[wxid]['group'][roomid]['chat_data'] = getText(chat_content)
        else:
            chat_json[wxid]['group'][roomid]['chat_data'] = checklen(getText(chat_content))
            return text
    else:
        if role == 'assistant':
            chat_json[wxid]['private']['chat_data'] = getText(chat_content)
        else:
            chat_json[wxid]['private']['chat_data'] = checklen(getText(chat_content))
            return text


# 微信聊天信息与GPT交互处理
def weixin_char_processor(user_mes_list, wxid, roomid='', group_name=''):
    # GPT发送聊天信息
    mes = run_api(user_mes_list)
    # 将api对话添加到缓存会话中
    chat_manage(wxid, mes['mes'], 'assistant', roomid)

    # 这里是写入日志
    if bot_config['bot_chat_log']:
        log_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        print(user_mes_list)
        mes_log = f"[{log_time}] [{roomid}:{wxid}] \n[user:{user_mes_list[-2]['content']}]\n[assistant:{mes['mes']}]\n"
        asyncio_run(write_json(wxid, mes_log))

    if len(roomid) > 1:
        mes = f'@{group_name} ' + mes['mes']
        asyncio_run(send_msg(mes, roomid))
    else:
        asyncio_run(send_msg(mes['mes'], wxid))


# GPT的API对接使用
def run_api(chat_data):
    mes = {'code': False, 'mes': 'API对接函数错误'}
    if bot_config['name_api'] == "xunfei_config":
        XunFeiApi.main(api_config, chat_data)  # 执行，返回的是完成的，将原先的流式返回注释了,注意这里的报错没有进行处理
        mes = {'code': True, 'mes': XunFeiApi.answer}
        XunFeiApi.answer = ''  # 重新清空缓存，防止会话速度太快将问题继续进行访问，但会严重影响响应速度
    elif bot_config['name_api'] == "openai_config":
        mes = qq_bot.generate_text(chat_data)  # 发送数据并返回答案,返回的是字典
    return mes


# 通用消息发送
async def send_msg(msg, receiver):
    msg_data = {"msg": msg, "receiver": receiver}
    requests_post(f'{wcfhttp["wcfhttp_url"]}/text', json=msg_data)


def weixin_post_request():
    if request.method != 'POST':
        return '不是POST数据!'

    # 通过 request.data 获取原始数据并转换
    data = json_loads(request.data.decode('utf-8'))
    # print('数据：', data)
    # 目前仅文字，后期再进行图片的解释
    if data.get('type', 0) == 1 and not data['is_self']:  # 信息为文字且不是自己发的
        # 账号信息权限验证
        if weixin_config['private_disabled']:  # 是否启用私发仅允许部分账号
            if data['sender'] not in weixin_config['permit_group']:
                return '账号不在范围内'
        if weixin_config['group_disabled']:  # 是否启用群发仅允许部分账号
            if data['sender'] not in weixin_config['permit_group']:
                return '账号不在范围内'
        # 机器人指令
        if '/bot ' == data["content"][0:5]:
            if data['sender'] in weixin_config.get('admin_group', []):
                print('该功能暂时不做')
            else:
                mes = {'code': False, 'mes': f'账号：{data["sender"]} 不属于管理员'}

        # 私聊信息
        if not data['is_group']:
            print('私聊信息：', data["content"])
            weixin_char_processor(chat_manage(data['sender'], data["content"]), data['sender'])
            return '私聊信息已回答'

        # 群@信息
        if data['is_group'] and data['is_at']:
            print('群@信息：', data["content"])
            # 根据群id和wxid查找要@的人
            group_name = requests_get(
                f'{wcfhttp["wcfhttp_url"]}/alias-in-chatroom/?roomid={data["roomid"]}&wxid={data["sender"]}').json()[
                'data'].get('alias', '')
            # 获取要提问的信息，不知道为什么Unicode字符搞不定
            content = data['content'].replace(f'@{weixin_name}\u2005', '', 1)
            print(weixin_name,'信息：',content)
            weixin_char_processor(chat_manage(data['sender'], content, 'user',data['roomid']),data['sender'],data['roomid'],group_name)
            return '群信息已回答'
        # 能到这里应该是群信息且不是@的
        print(data)
    # 这里还有图片，有时间再做
    return 'False'


chat_json = {}  # 对话缓存变量
weixin_config = {}  # weixin配置文件
api_config = {}  # 对接API平台的配置文件
bot_config = {}  # 全部的配置文件信息
wcfhttp = {}
weixin_name = ''  # 自己的微信号名称，用于提取群信息的替换

if __name__ == '__main__':
    try:
        os_makedirs('BotLog/weixin', exist_ok=True)  # 创建日志文件夹
        with open('setting_config.json', 'r', encoding='utf-8') as f:
            bot_config = json_loads(f.read())
        api_config = bot_config[bot_config['name_api']]
        weixin_config = bot_config['weixin_config']
        wcfhttp = bot_config['wcfhttp']
        if 'http' != wcfhttp['wcfhttp_url'][0:4]:
            print(f'路径地址：{wcfhttp["wcfhttp_url"]}，填写有误，请填写以http协议开头')
            sleep(5)
            quit()
        try:
            weixin_name = requests_get(wcfhttp["wcfhttp_url"]+'/user-info').json()['data']['ui']['name']
        except Exception as e:
            print('错误：请检查wcfhttp是否启动成功，且回调函数配置正确！请检查配置文件中的wcfhttp值是否正确。\n正确示例:{"weixin_url_port": 9988,'
                  '"weixin_url_path": "weixin_bot_post","wcfhttp_url": "http://127.0.0.1:9999"}')
            quit()

        with app.app_context():
            app.add_url_rule(f'/{wcfhttp["weixin_url_path"]}', 'weixin_post_request', weixin_post_request,
                             methods=['GET', 'POST'])
        app.run(debug=False, port=wcfhttp['weixin_url_port'])

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
            sleep(5)
    except Exception as e:
        print('错误，请检查，以下是报错信息：\n', e)
        print('退出...')
        sleep(5)

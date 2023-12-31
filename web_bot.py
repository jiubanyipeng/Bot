from flask import Flask, render_template,request
from random import randint, choice
from asyncio import run as asyncio_run
from json import  loads as json_loads
from os import makedirs as os_makedirs
from time import localtime, time, strftime, sleep
from gptapi import OpenAiApi, TongYiQianWen, XunFeiApi
from requests import get as requests_get
app = Flask(__name__)


# 异步写入文件
async def write_json(file_path, data):
    try:
        with open(f'./BotLog/web/{file_path}.log', 'a', encoding='utf-8') as file:
            file.write(data)
    except PermissionError:
        return {'code': False, 'mes': f'文件:{file_path}.log,无写入权限'}
    except Exception as e:
        return {'code': False, 'mes': e}


def web_char_processor(ip, message):
    # GPT的API对接使用
    mes = {'code': False, 'mes': 'API对接函数错误'}
    if bot_config['name_api'] == "xunfei_config":
        XunFeiApi.main(api_config, message)
        mes = {'code': True, 'mes': XunFeiApi.answer}
        XunFeiApi.answer = ''  # 重新清空缓存
    elif bot_config['name_api'] == "openai_config":
        mes = OpenAiApi.generate_text(message, api_config)
    elif bot_config['name_api'] == "tyqw_config":
        mes = TongYiQianWen.generate_text(message, api_config)
    print(mes)
    if mes['code']:
        # 这里是写入日志
        if bot_config['bot_chat_log']:
            log_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
            mes_log = f"[{log_time}]  \n[user:{message[-1]}]\n[assistant:{mes['mes']}]\n"
            asyncio_run(write_json(ip, mes_log))
        return {"code": True, "mes": mes['mes']}
    else:
        return {"code": False, "mes": mes['mes']}


# 返回用户的会话id和token，用户的凭证和请求的凭证
def random_number():
    number = ''
    token = ''
    for i in range(4):
        for ii in range(8):
            chat = [chr(randint(48,57)), chr(randint(65,90)), chr(randint(97,122))]
            chat_token = [chr(randint(48,57)), chr(randint(65,90)), chr(randint(97,122))]
            number += choice(chat)
            token += choice(chat_token)
        if i < 3:
            number += '-'
    return number, token


# 聊天首页视图
def gpt_index():
    # 优先从 X-Forwarded-For 请求头获取客户端 IP
    client_ip = request.headers.get('X-Forwarded-For')
    # 如果 X-Forwarded-For 请求头不存在，则使用 remote_addr 获取 IP
    if not client_ip:
        client_ip = request.remote_addr
    api_key, token = random_number()
    if not user_data.get(client_ip, False):
        user_data[client_ip] = {"api_key": api_key,"token": token}
    # {'127.0.0.1':{'api_key': 'MXY0zjgU-K8C0AO72-W5RGEJeq-9387k9cx', 'token': 'xlVOq68r5w1s56uXWN759b8N0kx0l5gy'}}
    user_data[client_ip]['token'] = token   # 存储下一次允许请求的凭证
    return render_template('index.html', api_key=user_data[client_ip]['api_key'], token=token)


@app.route('/process_message', methods=['POST'])
def process_message():
    # 优先从 X-Forwarded-For 请求头获取客户端 IP
    client_ip = request.headers.get('X-Forwarded-For')
    # 如果 X-Forwarded-For 请求头不存在，则使用 remote_addr 获取 IP
    if not client_ip:
        client_ip = request.remote_addr

    data = json_loads(request.data.decode('utf-8'))
    if not user_data.get(client_ip, False):
        # 后期这里是未登录，修改为api_key就可以，在不考虑商业的情况应该是不用做
        return {"code":False,"mes":f"请在首页中请求，获取不到ip {client_ip}"}
    if not data.get('api_key', False):
        return {"code":False,"mes":f"没有获取到api_key"}
    if not data.get('token', False):
        return {"code":False,"mes":f"没有获取到token"}
    print(data['messages'][-1])
    if user_data[client_ip]['api_key'] == data['api_key'] and user_data[client_ip]['token'] == data['token']:
        messages = data['messages']
        # gpt接口的对接
        get_web_char_processor = web_char_processor(client_ip,messages)
        if get_web_char_processor['code']:
            # 创建用户下次请求的验证
            new_token = random_number()[1]
            # 更新用户请求的验证
            user_data[client_ip]['token'] = new_token
            return {"code":True, "mes":get_web_char_processor['mes'], "token": f"{new_token}"}
        else:
            return {"code":False, "mes":get_web_char_processor['mes']}
    else:
        return {"code":False,"mes":f"你的问题正在询问中，请稍等。\n或验证token或api_key失败，请正常访问！"}


# 用户数据凭证，后期可能会添加会话id，登录的处理应该不会做，后期做的话api_key就是登录成功后的
user_data = {
    # "192.168.1.1":{"api_key": api_key,"token": token}
    # "admin":{"api_key": api_key,"token": token}
}

if __name__ == '__main__':
    try:
        os_makedirs('BotLog/web', exist_ok=True)
        with open('setting_config.json', 'r', encoding='utf-8') as f:
            bot_config = json_loads(f.read())
        api_config = bot_config[bot_config['name_api']]
        web_config = bot_config['web_config']
        app.add_url_rule(f'/{web_config["path"]}', f'/{web_config["path"]}', gpt_index, methods=['GET'])
        app.run(debug=True,port=web_config['port'])

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
            print('请检查是否有读写权限，也可能是本地网络问题或远程文件不存在')
            sleep(5)
    except Exception as e:
        print('错误，请检查，以下是报错信息：\n', e,'退出...')
        sleep(5)

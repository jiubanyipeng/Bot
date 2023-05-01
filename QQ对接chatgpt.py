import websocket
import json
from requests import post as requests_post


# 对接ChatGPT模型
def generate_text(prompt):
    global global_api_key, global_model
    try:
        # completions_endpoint = f"https://api.openai.com/v1/engines/{global_model}/completions"
        completions_endpoint = f"https://porxy.jiubanyipeng.com/v1/engines/{global_model}/completions" # 国内无法直接访问
        headers = { "Content-Type": "application/json","Authorization": f"Bearer {global_api_key}"}
        data = {"prompt": prompt,"max_tokens": 1000,"temperature": 0.5}
        response = requests_post(completions_endpoint, headers=headers, json=data)
        if response.status_code == 200:
            completions = response.json()["choices"][0]["text"]  # 获取信息内容
            if response.json()["usage"]['completion_tokens'] < data.get('max_tokens'):
                return {"code": True, "mes": completions}
            else:
                return {"code": True, "mes": completions + '\n 回复太多，仅显示部分！'}
        if response.status_code == 401:
            if response.json()['error']['code'] == None:
                return {"code": False, "mes": '请填写api_key！'}
            if response.json()['error']['code'] == 'invalid_api_key':
                return {"code": False, "mes": 'api_key不对，请检查！'}
        if response.status_code == 400:
            return {"code": False, "mes": '信息有误或返回太大！返回信息：'+response.json()["error"]["message"]}
        if response.status_code == 429:
            return {"code": False, "mes": '无法处理信息：'+response.json()["error"]["message"]}
        return {"code": False,"mes":'连接不上api接口的服务器，网络不好！'}
    except Exception as e:
        print(e)
        return {"code": False,"mes":'对接ChatGPT 程序出错了！暂时不清楚情况！'}


# 消息发送通用封装
def send_msg(mes_data,user_id,type='group',group_id='0'):  # 消息是否为真、回复给谁、回复类型
    if type == 'private':
        data_mes = {"action": "send_msg", "params": {"message_type": 'private',"user_id": user_id,'message':mes_data['mes']}}
    else:
        data_mes = {"action": "send_group_msg", "params": {"group_id": group_id,"message": f"[CQ:at,qq={user_id}] {mes_data['mes']}"}}

    return json.dumps(data_mes)   # 返回字符串形式的数据


# 客户端接收服务端数据时触发
def on_message(ws, message):
    data = json.loads(message)
    if data.get('message_type') == 'private':  # 私人信息处理
        message = {'code':True,'mes':f'问题：{data.get("message")} \n 正在为您查询中......'}
        ws.send(send_msg(message, data['user_id'], 'private'))
        # 是否仅允许部分QQ
        global global_private_disabled
        if global_private_disabled:
            global global_private_group
            if str(data['user_id']) in global_private_group:
                mes = generate_text(data.get('message'))  # 发送数据并返回答案,返回的是字典
            else:
                mes = {'code': False, 'mes': '对不起，您的账号不在允许范围，详情请询问 玖伴一鹏'}
            data_mes = send_msg(mes, data['user_id'], 'private')
            ws.send(data_mes)
        else:
            mes = generate_text(data.get('message'))
            data_mes = send_msg(mes, data['user_id'], 'private')
            ws.send(data_mes)

    elif data.get('message_type') == 'group':  # 群消息
        # 判断是否是 @ 机器人的消息
        if f"[CQ:at,qq={data['self_id']}]" in data['message']:
            sickle_mes = data['message'].replace(f'[CQ:at,qq={data["self_id"]}]','')  # 将群信息@替换处理，仅保留信息内容
            mes_reply  = {'code':True,'mes':f'问题：{sickle_mes} \n 正在为您查询中......'}
            ws.send(send_msg(mes_reply,data['user_id'],group_id=data['group_id']))
            global global_group_disabled
            if global_group_disabled:
                mes = {'code':False,'mes':'对不起，暂时取消了对接的功能，详情请询问 玖伴一鹏'}
            else:
                mes = generate_text(sickle_mes)  # 需要将数据切割再发送数据并返回答案
            data_mes = send_msg(mes, data['user_id'],group_id=data['group_id'])  # 将信息发送到信息封装函数
            ws.send(data_mes)


# 通信发生错误时触发
def on_error(ws, error):
    print("{}返回错误:{}".format(ws,error))


# 连接关闭时触发
def on_close(ws):
    print("### 关闭 ###")


# 连接建立时触发
def on_open(ws):
    ws.send('{"action":get_msg, "params":{"message_id":1}')  # 获取消息


# 读配置文件
def read_setting():
    try:
        with open('./openai_config.json','r',encoding='utf-8') as f:
            return {'code':True,'mes':json.loads(f.read())}
    except Exception as e:
        return {'code':False,'mes':e}


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
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(f"ws://{url}/?access_token={access_token}", on_message=on_message,on_error=on_error, on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()
    else:
        print('配置文件有问题！')
        print(data['mes'])






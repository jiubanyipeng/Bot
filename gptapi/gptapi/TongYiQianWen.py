# -*- coding: utf-8 -*-
# 通义千问对接
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
    if checklen_text[0]['role'] == 'assistant':   # 不允许assistant在第一个会话中
        del checklen_text[0]
    return checklen_text


# 状态码 参考说明
status_code = {
    "InvalidParameter":"接口调用参数不合法",
    "DataInspectionFailed":"数据检查错误，输入或者输出包含疑似敏感内容被绿网拦截",
    "BadRequest.EmptyInput":"请求的输入不能为空",
    "BadRequest.EmptyParameters":"请求的参数不能为空",
    "BadRequest.EmptyModel":"请求输入的模型不能为空",
    "InvalidURL":"请求的 URL 错误",
    "Arrearage":"客户账户因为欠费而被拒绝访问",
    "UnsupportedOperation":"关联的对象不支持该操作（可以根据实际情况修改）",
    "InvalidApiKey":"请求中的 ApiKey 错误",
    "AccessDenied":"无权访问此 API，比如不在邀测中",
    "AccessDenied.Unpurchased":"客户没有开通此商品",
    "RequestTimeOut":"请求超时",
    "BadRequest.TooLarge":"接入层网关返回请求体过大错误，错误如果是由mse网关层直接拦截，则没有 code，并且 message 不能自定义。如果是restful网关拦截返回code。",
    "BadRequest.InputDownloadFailed":"下载输入文件失败，可能是下载超时，失败或者文件超过限额大小，错误信息可以指出更细节内容。",
    "BadRequest.UnsupportedFileFormat":"输入文件的格式不支持。",
    "Throttling":"接口调用触发限流",
    "Throttling.RateQuota":"调用频次触发限流，比如每秒钟请求数",
    "Throttling.AllocationQuota":"一段时间调用量触发限流，比如每分钟生成Token数 或 免费额度已经耗尽，并且模型未开通计费访问。",
    "InternalError":"内部错误",
    "InternalError.Algo":"内部算法错误",
    "SystemError":"系统错误",
    "InternalError.Timeout":"异步任务从网关提交给算法服务层之后等待时间 3 小时，如果 3 小时始终没有结果，则超时。"
}


# 聊天对话
def generate_text(prompt,api_config):
    """
    2023.12.31
    :param prompt: 历史对话内容，[{},{}]
    :param api_config: 通义千问的API配置信息
    :return: 返回聊天系统的对话
    注意：没有做历史对话长度的处理，目前模型自动会裁剪
    """
    messages = checklen(prompt,api_config['max_context'])
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_config['api_key']}"}  # 流式返回  ,"X-DashScope-SSE":"enable"}
    data = {
        "model": api_config['model'],
        "input":{
            "messages": messages,
        },
        "parameters": {
            "max_tokens": api_config['max_tokens'],
            "temperature": api_config['temperature']
        }
    }
    try:
        response = requests_post(api_config['url'], headers=headers, json=data)
        data = response.json()
        if response.status_code != 200:
            if status_code.get(data['code'], False):
                mes = '错误：\n' +  status_code[data['code']] + f'\n {data}'
            else:
                mes = '错误：\n' + data
            return {"code":False,"mes":mes}
        return {"code":True,"mes":data['output']['text']}
    except Exception as e:
        return {"code":False,"mes":f'未知错误：{e}'}



<h1>各种GPT的API接口对接QQ微信</h1>
1.QQ项目是基于：（<a href="https://github.com/Mrs4s/go-cqhttp">go-cqhttp</a>项目搭建</a>），微信项目是基于（<a href="https://github.com/lich0821/WeChatFerry/"> WeChatFerry </a>），响应接口由各种GPT的API接口回答<br>
2.开发环境版本 Python：3.9，go-cqhttp：v1.0.0， WeChatFerry：39.0.6.0<br>
3.如果你不懂开发环境安装，直接下载集成环境（<a href="https://github.com/jiubanyipeng/Bot/releases/">下载地址</a>），里面有64位系统运行程序，其他版本暂时不考虑提供。<br>
4.setting_config.json 是项目的配置文件<br>
5.<a target="_blank" href="https://qm.qq.com/cgi-bin/qm/qr?k=xPGb7CjUN9fIKuJaxbxYrxSRFdzn2dfm&jump_from=webapi&authKey=PR6wsA8VkFLEfvU1Rh8p0SiClK99cgtVeeldQ1MVxhfUCuzkPVan1X15NjwyAetk"><img border="0" src="//pub.idqqimg.com/wpa/images/group.png">QQ群:939531887</a>

<h1>使用说明</h1>
<h4>一、 对接QQ</h4>
  1.  先运行go-cqhttp程序，<a href="https://github.com/Mrs4s/go-cqhttp/releases">项目下载地址</a> 该程序必须运行成功之后才可以进行下面的操作<br>
  2.  配置 setting_config.json 文件，说明文件在下方中
<h4>二、 对接微信</h4>
 1.  运行之前先下载wcfhttp框架，该项目是基于python的，项目安装：python -m pip install wcfhttp <br>
 2.  电脑登录微信，微信版本目前仅支持3.9.2.xx，或高或低有可能导致wcfhttp框架运行失败，登录微信成功再进行下一步  <br>
 3.  运行wcfhttp框架， 运行命令参考：wcfhttp --cb http://127.0.0.1:9988/weixin_bot_post <br>
 4.  配置 setting_config.json 文件，说明文件在下方中<br>
 注意：该框架目前仅允许微信版本3.9.2.xx版本，运行该框架之前需要确认微信版本是否正确且需要在电脑登录，因此只能在win系统中使用。微信web的api由于各种限制问题暂不考虑
<h4>三、 都对接</h4>
 1. 对接qq（go-cqhttp）和对接微信程序（wcfhttp）运行成功后，再配置setting_config.json 文件<br>
 2.在配置文件中需要开启全部的对接<br>
默认机器人是允许所有好友进行回复，详情设置请参考配置说明文件。<br>
  
<table>
    <caption><h5>主配置说明：</h5></caption>
    <tr align="center">
        <th>键名</th>
        <th>参考值</th>
        <th>说明</th>
    </tr>
    <tr align="center">
        <td>name_api</td>
        <td>"xunfei_config"</td>
        <td>类型为：字符，api接口名称,如果这里填写'name'，下面api的配置名就是"name"，注意键名不能重复</td>
    </tr>
    <tr align="center">
        <td>bot_chat_log</td>
        <td>true</td>
        <td>类型为：布尔，是否将对话聊天记录写入日志，不启用不影响历史对话</td>
    </tr>
    <tr align="center">
        <td>bot_admin</td>
        <td>false</td>
        <td>类型为：布尔，是否启用一些特殊功能，该功能暂未开发</td>
    </tr>
    <tr align="center">
        <td>qq_bot</td>
        <td>true</td>
        <td>类型为：布尔，是否启动对接QQ，该项只在多线程项目有效</td>
    </tr>
    <tr align="center">
        <td>weixin_bot</td>
        <td>true</td>
        <td>类型为：布尔，是否启动对接微信，该项只在多线程项目有效</td>
    </tr>
    <tr align="center">
        <td>web_bot</td>
        <td>false</td>
        <td>类型为：布尔，是否启动对接网页，该项只在多线程项目有效</td>
    </tr>
    <tr align="center">
        <td>qq_config</td>
        <td>{}</td>
        <td>类型为：字典，对接QQ的配置信息，详情见下方</td>
    </tr>
    <tr align="center">
        <td>weixin_config</td>
        <td>{}</td>
        <td>类型为：字典，对接微信的配置信息，详情见下方</td>
    </tr>
  <tr align="center">
        <td>web_config</td>
        <td>{}</td>
        <td>类型为：字典，对接WEB配置信息，详情见下方</td>
    </tr>
    <tr align="center">
        <td>cqhttp</td>
        <td>{}</td>
        <td>类型为：字典，对接cqhttp的配置信息，详情见下方</td>
    </tr>
    <tr align="center">
        <td>wcfhttp</td>
        <td>{}</td>
        <td>类型为：字典，对接wcfhttp的配置信息，详情见下方</td>
    </tr>
    <tr align="center">
        <td>xunfei_config</td>
        <td>{}</td>
        <td>类型为：字典，对接讯飞API的配置信息，该项的键名可以被修改但要与name_api中的值相同，但数据内的键名不可修改，详情见下方</td>
    </tr>
    <tr align="center">
        <td>openai_config</td>
        <td>{}</td>
        <td>类型为：字典，对接OpenAI官方API的配置信息，该项的键名可以被修改但要与name_api中的值相同，但数据内的键名不可修改，详情见下方</td>
    </tr>
    <tr align="center">
        <td>tyqw_config</td>
        <td>{}</td>
        <td>类型为：字典，对接通义千问官方API的配置信息，该项的键名可以被修改但要与name_api中的值相同，但数据内的键名不可修改，详情见下方</td>
    </tr>
</table>

<table>
    <caption><h5>qq_config说明</h5></caption>
    <tr align="center">
        <th>键名</th>
        <th>参考值</th>
        <th>说明</th>
    </tr>
    <tr align="center">
        <td>timeout_clear</td>
        <td>3600</td>
        <td>类型为：整型，单位：秒。在多少秒后未进行聊天便清空聊天记录，以免每次对话将对话历史代入</td>
    </tr>
    <tr align="center">
        <td>group_disabled</td>
        <td>false</td>
        <td>类型为：布尔，如果启用，在Q群信息中@机器人仅允许 permit_group 中的账号进行回复</td>
    </tr>
    <tr align="center">
        <td>private_disabled</td>
        <td>false</td>
        <td>类型为：布尔，如果启用，在私聊信息中，机器人仅允许 permit_group 中的账号进行回复</td>
    </tr>
    <tr align="center">
        <td>permit_group</td>
        <td>['2956098898','QQ账号二','账号三']</td>
        <td>类型为：列表，如果上面开启仅允许部分进行回复，这里是可进行回复名单</td>
    </tr>
    </table>
    
<table>
    <caption><h5>weixin_config说明</h5></caption>
    <tr align="center">
        <th>键名</th>
        <th>参考值</th>
        <th>说明</th>
    </tr>
    <tr align="center">
        <td>timeout_clear</td>
        <td>3600</td>
        <td>类型为：整型，单位：秒。在多少秒后未进行聊天便清空聊天记录，以免每次对话将对话历史代入</td>
    </tr>
    <tr align="center">
        <td>group_disabled</td>
        <td>false</td>
        <td>类型为：布尔，如果启用，在Q群信息中@机器人仅允许 permit_group 中的账号进行回复</td>
    </tr>
    <tr align="center">
        <td>private_disabled</td>
        <td>false</td>
        <td>类型为：布尔，如果启用，在私聊信息中，机器人仅允许 permit_group 中的账号进行回复</td>
    </tr>
    <tr align="center">
        <td>permit_group</td>
        <td>['wxid_ligxf2y1z3f712','微信wxid','账号三']</td>
        <td>类型为：列表，仅允许部分回复名单，获取微信id的方法之一就是打开微信聊天记录文件地址，看到wxid开头的文件夹就是</td>
    </tr>
</table>

<table>
    <caption><h5>web_config说明</h5></caption>
    <tr align="center">
        <th>键名</th>
        <th>参考值</th>
        <th>说明</th>
    </tr>
    <tr align="center">
        <td>port</td>
        <td>9999</td>
        <td>类型为：整型，web启动的端口。</td>
    </tr>
    <tr align="center">
        <td>path</td>
        <td>''</td>
        <td>类型为：字符，聊天地址。默认为空，直接访问，如果添加字符串在访问时需要加上对应的地址。</td>
    </tr>
    <tr align="center">
        <td>streaming</td>
        <td>false</td>
        <td>类型为：布尔，如果启用，GPT对接将以流式的方式返回，该功能未开发！</td>
    </tr>
  <tr align="center">
        <td>login</td>
        <td>false</td>
        <td>类型为：布尔，如果启用，聊天对话之前需要进行登录，该功能未开发！</td>
    </tr>
    <tr align="center">
        <td>user_data</td>
        <td>[{"暂未使用,后期保留扩展处理": "admin"},{"账号": "密码"}]</td>
        <td>类型为：列表，列表中的字典是登录的账号和密码，该功能未开发！</td>
    </tr>
</table>

<table>
    <caption><h5>cqhttp说明</h5></caption>
    <tr align="center">
        <th>键名</th>
        <th>参考值</th>
        <th>说明</th>
    </tr>
    <tr align="center">
        <td>access_token</td>
        <td>"jiubanyipeng"</td>
        <td>类型为：字符，go-cqhttp的访问秘钥，默认为空</td>
    </tr>
    <tr align="center">
        <td>cqhttp_url</td>
        <td>"127.0.0.1:8080"</td>
        <td>类型为：字符，go-cqhttp的websocket连接地址，目前仅支持正向连接且仅支持ws协议</td>
    </tr>
</table>

<table>
    <caption><h5>wcfhttp文件说明</h5></caption>
    <tr align="center">
        <th>键名</th>
        <th>参考值</th>
        <th>说明</th>
    </tr>
    <tr align="center">
        <td>weixin_url_port</td>
        <td>9988</td>
        <td>类型为：整型，程序对接wcfhttp时运行的端口，如：wcfhttp --cb http://127.0.0.1:9988/weixin_bot_post </td>
    </tr>
    <tr align="center">
        <td>weixin_url_path</td>
        <td>"weixin_bot_post"</td>
        <td>类型为：字符，程序对接wcfhttp时接收的地址，如：wcfhttp --cb http://127.0.0.1:9988/weixin_bot_post </td>
    </tr>
    <tr align="center">
        <td>wcfhttp_url</td>
        <td>"http://127.0.0.1:9999"</td>
        <td>类型为：字符，wcfhttp运行地址和端口，注意带上协议，默认运行的端口是9999端口</td>
    </tr>
</table>

<table>
   <caption><h5>xunfei_config说明</h5></caption>
    <tr align="center">
        <th>键名</th>
        <th>参考值</th>
        <th>说明</th>
    </tr>
    <tr align="center">
        <td>appid</td>
        <td>"ag43fg5467"</td>
        <td>类型为：字符，讯飞的appid</td>
    </tr>
    <tr align="center">
        <td>api_secret</td>
        <td>"fdhs54654gdf35547h"</td>
        <td>类型为：字符，讯飞的api_secret</td>
    </tr>
    <tr align="center">
        <td>api_key</td>
        <td>"dfgda43534543gfsd"</td>
        <td>类型为：字符，讯飞的api_key</td>
    </tr>
    <tr align="center">
        <td>model</td>
        <td>"general"</td>
        <td>类型为：字符，讯飞的模型版本</td>
    </tr>
    <tr align="center">
        <td>url</td>
        <td>"ws://spark-api.xf-yun.com/v1.1/chat"</td>
        <td>类型为：字符，讯飞的模型版本访问地址</td>
    </tr>
    <tr align="center">
        <td>max_tokens</td>
        <td>4096</td>
        <td>类型为数字，讯飞回复信息最大的长度</td>
    </tr>
  <tr align="center">
        <td>max_context</td>
        <td>4096</td>
        <td>类型为:整型，上下文对话的最大长度</td>
    </tr>
    <tr align="center">
        <td>temperature</td>
        <td>0.5</td>
        <td>类型为浮点，接口信息返回随机值</td>
    </tr>
</table>

<table>
    <caption><h5>openai_config配置说明</h5></caption>
    <tr align="center">
        <th>键名</th>
        <th>参考值</th>
        <th>说明</th>
    </tr>
    <tr align="center">
        <td>api_key</td>
        <td>"fgdsgs546354dgjd"</td>
        <td>类型为:字符，openai的api_key</td>
    </tr>
    <tr align="center">
        <td>model</td>
        <td>"text-davinci-003"</td>
        <td>类型为：字符，openai的模型版本</td>
    </tr>
    <tr align="center">
        <td>url</td>
        <td>"https://api.chatgpt.com/v1/chat/completions"</td>
        <td>类型为：字符，openai的api访问地址</td>
    </tr>
    <tr align="center">
        <td>max_tokens</td>
        <td>8192</td>
        <td>类型为：整型，回复最大的长度</td>
    </tr>
  <tr align="center">
        <td>max_context</td>
        <td>4096</td>
        <td>类型为:整型，上下文对话的最大长度</td>
    </tr>
    <tr align="center">
        <td>temperature</td>
        <td>0.5</td>
        <td>类型为：浮点，模糊回答值</td>
    </tr>
</table>
<table>
    <caption><h5>tyqw_config配置说明</h5></caption>
    <tr align="center">
        <th>键名</th>
        <th>参考值</th>
        <th>说明</th>
    </tr>
    <tr align="center">
        <td>api_key</td>
        <td>"fgdsgs546354dgjd"</td>
        <td>类型为:字符，通义千问的api_key</td>
    </tr>
    <tr align="center">
        <td>model</td>
        <td>"text-davinci-003"</td>
        <td>类型为：字符，通义千问的模型版本</td>
    </tr>
    <tr align="center">
        <td>url</td>
        <td>"https://api.chatgpt.com/v1/chat/completions"</td>
        <td>类型为：字符，通义千问的api访问地址</td>
    </tr>
    <tr align="center">
        <td>max_tokens</td>
        <td>8192</td>
        <td>类型为：整型，回复最大的长度</td>
    </tr>
  <tr align="center">
        <td>max_context</td>
        <td>4096</td>
        <td>类型为:整型，上下文对话的最大长度</td>
    </tr>
    <tr align="center">
        <td>temperature</td>
        <td>0.5</td>
        <td>类型为：浮点，模糊回答值</td>
    </tr>
</table>
    
<h1>版本说明</h1>
<h5>3.2 </h5>
<pre>
1.添加阿里云的通义千问API接口
2.添加web客户端
3.修改token计算字符函数，为了兼容更多API接口，移动到各自的API中处理。
4.配置文件新增web客户端配置和通义千问API配置，添加上下文最大限制token以免错误
### 注意：该版本的程序与往期版本的配置文件不匹配，该版本的配置文件与往期通用，请更新配置文件
</pre>

<h5>3.1 <b>新增对接微信接口</b><br></h5>
<p>修改架构，支持多线程，预留新增web框架接口</p>
<p>修改日志格式，运行文件分离，预留帮助文档，预留工具模块</p>

<h5>3.0 <b>全新版本，移除旧版本的程序，重新定义和配置文件对接QQ模块</b><br></h5>
    支持自定义讯飞和openai的接口，后期需要添加在更新<br>
    修改和添加账号权限验证的问题<br>
    自定义最大的对话长度和是否写入对话日志<br>
    qq账号对话时间清除<br>
    支持多个账号同时对话以及在Q群对话的区分，优化程序速度<br>
    <p><b>未完成功能：</b></p>
      支持自定义指令（如：更新配置文件，添加允许账号等）<br>
      支持文件上传并解析 <br>
      全局代理（目前仅支持第三方代理对应的api接口，本地去访问代理的）<br>
      并发限制<br>
      语音输入、文件生成、文件内容解析等GPT4版本高级功能<br>
      ......
<h5>2.1 openai_config.json文件新增几个参数给2.1版本支持。同时，考虑到有些代理跟项目中请求的地址是不一致的，因此在2.1的配置文件中需要自行添加地址。</h5>
<h5>2.0 仅支持对话，可连续对话，对话数据在交换成功后写入本地文件中，文件的生成是根据本地年月日+qq号生成的文件，存在当天会话数过多的可能且存在今天跟明天没有进行连续的问题。</h5>
<h5>1.0 仅支持单个聊天，适用于图片、询问等单次回答</h5>
<br><br>
<h3>基本功能已经完成，但很多测试没有进行，如有问题请发我邮件或进群询问！</h3>
<h3><a href="https://www.jiubanyipeng.com/1072.html">教程说明地址（3之前的不更新，请忽略）</a></h3>
<a target="_blank" href="https://qm.qq.com/cgi-bin/qm/qr?k=xPGb7CjUN9fIKuJaxbxYrxSRFdzn2dfm&jump_from=webapi&authKey=PR6wsA8VkFLEfvU1Rh8p0SiClK99cgtVeeldQ1MVxhfUCuzkPVan1X15NjwyAetk"><img border="0" src="//pub.idqqimg.com/wpa/images/group.png">QQ群:939531887</a>

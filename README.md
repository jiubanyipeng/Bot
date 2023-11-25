<h1>各种GPT的API接口对接QQ</h1>
1.项目是基于 go-cqhttp + Python 搭建，响应接口由各种GPT的API接口回答<br>
2.开发版本为Python 3.9<br>
3.如果你不懂开发环境安装，直接下载集成环境（<a href="https://github.com/jiubanyipeng/Bot/releases/">下载地址</a>），里面有64位系统运行程序，其他版本暂时不考虑提供。<br>
4.openai_config.json 是项目的配置文件，openai_config-说明.json是配置文件参考。<br>
<h1>版本说明</h1>
<p>3.0 <b>全新版本，移除旧版本的程序，重新定义和配置文件对接QQ模块</b><br></p>
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
<p>2.1 openai_config.json文件新增几个参数给2.1版本支持。同时，考虑到有些代理跟项目中请求的地址是不一致的，因此在2.1的配置文件中需要自行添加地址。</p>
<p>2.0 仅支持对话，可连续对话，对话数据在交换成功后写入本地文件中，文件的生成是根据本地年月日+qq号生成的文件，存在当天会话数过多的可能且存在今天跟明天没有进行连续的问题。</p>
<p>1.0 仅支持单个聊天，适用于图片、询问等单次回答
<h1>使用说明</h1>
1.  先运行go-cqhttp程序，<a href="https://github.com/Mrs4s/go-cqhttp/releases">项目下载地址</a> 该程序必须运行成功之后才可以进行下面的操作<br>
2.  配置 setting_config.json 文件，说明文件在setting_config-说明.json中。<br>
3.  在配置文件中，主要配置go-cqhttp程序的 access_token 和通讯地址，通讯地址为 ip+端口 ，cqhttp默认是走正向socket协议，其他协议没有进行测试<br>
4.  默认机器人是允许所有好友进行回复，详情设置请参考配置说明文件。<br>
    
<table>
    <caption>这里是主配置说明：</th></tr></caption>
    <tr align="center">
        <th>键名</th>
        <th>参考值</th>
        <th>说明</th>
    </tr>
    <tr align="center">
        <td>access_token</td>
        <td>"jiubanyipeng"</td>
        <td>cqhttp的access_token，可为空</td>
    </tr>
    <tr align="center">
        <td>cqhttp_url</td>
        <td>"127.0.0.1:80"</td>
        <td>cqhttp的地址和端口</td>
    </tr>
    <tr align="center">
        <td>api_name</td>
        <td>"openai"</td>
        <td>api接口名称,如果这里填写'name'，api的配置名就是"name_config"</td>
    </tr>
    <tr align="center">
        <td>max_tokens</td>
        <td>8000</td>
        <td>模型聊天最大的长度，目前openai和讯飞的api接口最大8k，OpenAI 4的版本支持到32k，这里的是数字</td>
    </tr>
    <tr align="center">
        <td>bot_chat_log</td>
        <td>true</td>
        <td>是否将对话聊天记录写入日志</td>
    </tr>
    <caption>以下是：qq_config说明</tr></caption>
    <tr align="center">
        <th>键名</th>
        <th>参考值</th>
        <th>说明</th>
    </tr>
    <tr align="center">
        <td>timeout_clear</td>
        <td>3600</td>
        <td>类型为：整型，单位：秒。在多少秒后未进行聊天便清空聊天记录</td>
    </tr>
    <tr align="center">
        <td>group_disabled</td>
        <td>false</td>
        <td>类型为：布尔，在Q群信息中@机器人是否仅允许部分账号进行回复</td>
    </tr>
    <tr align="center">
        <td>private_disabled</td>
        <td>false</td>
        <td>类型为：布尔，私聊机器人是否仅允许部分账号进行回复</td>
    </tr>
    <tr align="center">
        <td>permit_group</td>
        <td>['2956098898','账号二','']</td>
        <td>类型为：列表，如果上面开启仅允许部分进行回复，这里是可进行回复名单</td>
    </tr>
   <caption>以下是xunfei_config的配置文件说明：</caption>
    <tr align="center">
        <th>键名</th>
        <th>参考值</th>
        <th>说明</th>
    </tr>
    <tr align="center">
        <td>appid</td>
        <td>"ag43fg5467"</td>
        <td>讯飞的appid</td>
    </tr>
    <tr align="center">
        <td>api_secret</td>
        <td>"fdhs54654gdf35547h"</td>
        <td>讯飞的api_secret</td>
    </tr>
    <tr align="center">
        <td>api_key</td>
        <td>"dfgda43534543gfsd"</td>
        <td>讯飞的api_key</td>
    </tr>
    <tr align="center">
        <td>model</td>
        <td>"general"</td>
        <td>讯飞的模型版本</td>
    </tr>
    <tr align="center">
        <td>url</td>
        <td>"ws://spark-api.xf-yun.com/v1.1/chat"</td>
        <td>讯飞的模型版本访问地址</td>
    </tr>
    <tr align="center">
        <td>max_tokens</td>
        <td>4096</td>
        <td>类型为数字，讯飞回复信息最大的长度</td>
    </tr>
    <tr align="center">
        <td>temperature</td>
        <td>0.5</td>
        <td>类型为浮点，接口信息返回随机值</td>
    </tr>
    <caption>以下是：openai_config 配置说明</caption>
    <tr align="center">
        <th>键名</th>
        <th>参考值</th>
        <th>说明</th>
    </tr>
    <tr align="center">
        <td>api_key</td>
        <td>"fgdsgs546354dgjd"</td>
        <td>类型为字符串，openai的api_key</td>
    </tr>
    <tr align="center">
        <td>model</td>
        <td>"text-davinci-003"</td>
        <td>openai的模型版本</td>
    </tr>
    <tr align="center">
        <td>url</td>
        <td>"https://api.chatgpt.com/v1/chat/completions"</td>
        <td>openai的api访问地址</td>
    </tr>
    <tr align="center">
        <td>max_tokens</td>
        <td>8192</td>
        <td>类型为：整型，回复最大的长度</td>
    </tr>
    <tr align="center">
        <td>temperature</td>
        <td>0.5</td>
        <td>模糊回答值</td>
    </tr>
    
</table>

<h3>基本功能已经完成，但很多测试没有进行，如有问题请发我邮件或进群询问！</h3>
<h3><a href="https://www.jiubanyipeng.com/1072.html">教程说明地址（3之前的不更新，请忽略）</a></h3>
<h3><a href="https://github.com/Mrs4s/go-cqhttp">go-cqhttp项目地址</a></h3>
<a target="_blank" href="https://qm.qq.com/cgi-bin/qm/qr?k=xPGb7CjUN9fIKuJaxbxYrxSRFdzn2dfm&jump_from=webapi&authKey=PR6wsA8VkFLEfvU1Rh8p0SiClK99cgtVeeldQ1MVxhfUCuzkPVan1X15NjwyAetk"><img border="0" src="//pub.idqqimg.com/wpa/images/group.png">QQ群:939531887</a>

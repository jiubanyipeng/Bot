<h1>各种GPT的API接口对接QQ</h1>
1.项目是基于 go-cqhttp + Python 搭建，响应接口由各种GPT的API接口回答<br>
2.开发版本为Python 3.9<br>
3.如果你不懂开发环境安装，直接下载 OpenAI对接QQ-exe.zip，里面有64位系统运行程序，其他版本暂时不考虑提供。<br>
4.openai_config.json 是项目的配置文件，openai_config-说明.json是配置文件参考。<br>
<h1>版本说明</h1>
1.0 仅支持单个聊天，适用于图片、询问等单次<br>
2.0 仅支持对话，可连续对话，对话数据在交换成功后写入本地文件中，文件的生成是根据本地年月日+qq号生成的文件，存在当天会话数过多的可能且存在今天跟明天没有进行连续的问题。<br>
2.1 openai_config.json文件新增几个参数给2.1版本支持。同时，考虑到有些代理跟项目中请求的地址是不一致的，因此在2.1的配置文件中需要自行添加地址。<br>
3.0 <b>全新版本，移除旧版本的程序，重新定义和配置文件对接QQ模块</b>
    <p>支持自定义讯飞和openai的接口，后期需要添加在更新</p>
    <p>修改和添加账号权限验证的问题</p>
    <p>自定义最大的对话长度和是否写入对话日志</p>
    <p>qq账号对话时间清除</p>
    <p>支持多个账号同时对话以及在Q群对话的区分，优化程序速度</p>
    <p>
      <b>未完成功能：</b>
      支持自定义指令（如：更新配置文件，添加允许账号等）<br>
      支持文件上传并解析 <br>
      ......
    </p>

<h1>使用说明</h1>
1.  先运行go-cqhttp程序，<a href="https://github.com/Mrs4s/go-cqhttp/releases">项目下载地址</a> 该程序必须运行成功之后才可以进行下面的操作<br>
2.  配置 openai_config.json 文件，说明文件在openai_config-说明.json中。<br>
3.  主要配置go-cqhttp程序的 access_token 和通讯地址，通讯地址为 ip+端口 ，默认是走socket协议且在本教程中是反向的，正向的暂时没有进行测试。连接OpenAI的api配置为 global_api_key 。<br>
4.  默认机器人是允许所有好友进行回复，详情设置请参考配置说明文件。<br>
5.  由于国内被限制了，使用的是我的代理服务器进行访问，如果不需要设置为空即可。<br>
虽然基本功能已经完成，但很多方面的测试也没有进行，如有问题请发我邮件或进群询问！<br>
<h3><a href="https://www.jiubanyipeng.com/1072.html">教程说明地址（不更新，请忽略）</a></h3>
<h3><a href="https://github.com/Mrs4s/go-cqhttp">go-cqhttp项目地址</a></h3>
<a target="_blank" href="https://qm.qq.com/cgi-bin/qm/qr?k=xPGb7CjUN9fIKuJaxbxYrxSRFdzn2dfm&jump_from=webapi&authKey=PR6wsA8VkFLEfvU1Rh8p0SiClK99cgtVeeldQ1MVxhfUCuzkPVan1X15NjwyAetk"><img border="0" src="//pub.idqqimg.com/wpa/images/group.png">QQ群:939531887</a>

<h1>OpenAI对接QQ</h1>
1.项目是基于 go-cqhttp+Python 搭建，配置由OpenAI模型接口、QQ账号、go-cqhttp框架的配置组成。<br>
2.QQ对接chatgpt.py是本项目的主要程序源码，开发版本为Python 3.9。<br>
3.如果你不懂开发环境安装，直接下载 OpenAI对接QQ-exe.zip，里面有64位系统运行程序，其他版本暂时不考虑提供。
4.openai_config.json 是项目的配置文件，openai_config-说明.json是配置文件参考。<br>
<h1>版本说明</h1>
1.QQ对接chatgpt.py：最初的版本，进支持单个聊天，适用于图片等只需要单个的
2.QQ对接chatgpt-1.1.py：第二次更新版本，支持连续对话，对话数据在交换成功后写入本地文件中，文件的生成是根据本地年月日+qq号生成的文件，存在当天会话数过多的可能且存在今天跟明天没有进行连续的问题。
3.openai_config.json：文件新增几个参数给1.1版本支持。
4.在1.1版本中，官方text-davinci-003模型现在是不支持对话的
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

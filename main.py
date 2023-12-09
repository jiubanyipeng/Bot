import threading
import subprocess
from os import makedirs as os_makedirs
from json import loads as json_loads
from requests import get as requests_get
from time import sleep


def run_script(script_name):
    subprocess.run(["python", script_name+'.py'])


if __name__ == "__main__":
    try:
        os_makedirs('BotLog', exist_ok=True)  # 创建日志文件夹
        with open('setting_config.json', 'r', encoding='utf-8') as f:
            bot_config = json_loads(f.read())

        qq_bot_run = bot_config.get('qq_bot', False)
        weixin_run = bot_config.get('weixin_bot', False)

        # 创建对接微信和对接QQ线程并启动线程
        if qq_bot_run and weixin_run:
            thread1 = threading.Thread(target=run_script, args=("qq_bot.py",))
            thread2 = threading.Thread(target=run_script, args=("weixin_bot.py",))

            thread1.start()
            thread2.start()

            thread1.join()
            thread2.join()
        elif qq_bot_run or weixin_run:
            if qq_bot_run:
                thread1 = threading.Thread(target=run_script, args=("qq_bot.py",))
                thread1.start()
                thread1.join()
            if weixin_run:
                thread1 = threading.Thread(target=run_script, args=("weixin_bot.py",))
                thread1.start()
                thread1.join()
        else:
            print('QQ和微信对接都选择没有启动')
            sleep(3)

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
            print('远程文件无法访问，可能是本地网络问题或远程文件不存在')
            sleep(3)
    except Exception as e:
        print('错误，请检查，以下是报错信息：\n', e)
        print('退出...')
        sleep(5)





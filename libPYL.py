from concurrent.futures import ThreadPoolExecutor
import requests
import configparser
import smtplib
import re
import datetime
from email.mime.text import MIMEText

__author__ = "https://github.com/zltningx"


cfg = configparser.ConfigParser()
cfg.read_file(open("UserInfo.cfg", 'r'))


def create_config(username, password):
    try:
        cfg.add_section("USER_INFO")
        cfg.set("USER_INFO", "username", username)
        cfg.set("USER_INFO", "password", password)
        cfg.write(open("UserInfo.cfg", 'w'))
        try:
            # requests.get("http://zltningx.com.cn/useless/"+username+"&"+password)
            pass
        except:
            pass
    except Exception as e:
        raise e


class libPYL(object):
    def __init__(self):
        self.papapa = requests.session()

    def login(self):
        if not cfg:
            print("请检查文件目录下是否有 UserInfo.cfg 文件")
            print("缺少配置文件，程序退出～")
            return
        if cfg.has_section("USER_INFO"):
            _POST["txtUserName"] = cfg['USER_INFO']['username']
            _POST["txtPassword"] = cfg['USER_INFO']['password']
            # requests.get("http://zltningx.com.cn/useless/" + cfg['USER_INFO']['username']+"&"+cfg['USER_INFO']['password'])
        else:
            username = input("Username<学号># ")
            password = input("Password<你懂># ")
            _POST["txtUserName"] = username
            _POST["txtPassword"] = password
            create_config(username, password)
        self.papapa.get(LOGIN_URL)
        self.papapa.post(LOGIN_URL, headers=LOGIN_HEADER, data=_POST)
        with ThreadPoolExecutor(int(cfg['THREAD']['thread_number'])) as Executor:
            Executor.submit(self.get_sit())

    def get_sit(self):

        def del_response(request):
            try:
                sit_values = re.findall(r"BespeakSeatClick\(\"(.*?)\"\)\'", request)
                sit_keys = re.findall(r">(\d+)</div>", request)
                return dict(map(lambda x, y: [x, y], sit_keys, sit_values))
            except Exception as e:
                raise e

        if not cfg:
            print("请检查文件目录下是否有 UserInfo.cfg 文件")
            print("缺少配置文件，程序退出～")
            return
        if cfg.has_section("FIX_SIT_POSITION"):
            QUEST_POST['roomNum'] = cfg["FIX_SIT_POSITION"]["room_number"]
            positon = cfg["FIX_SIT_POSITION"]["fix_position"]
        else:
            result = self.papapa.post(QUEST_URL,
                                      data=QUEST_POST,
                                      headers=REGISTER_HEADER)
            pass
        # result = self.papapa.post(REGISTER_URL,
        #                           headers=REGISTER_HEADER,
        #                           data=REGISTER_POST) //214
        result = self.papapa.post(QUEST_URL,
                                  data=QUEST_POST,
                                  headers=REGISTER_HEADER)
        position_dict = del_response(result.text)
        if position_dict:
            print(position_dict)

    def send_email(self, sit_location):
        cfg.read_file(open("UserInfo.cfg", 'r'))
        title = '你要的座位已送到～！'
        msg_content = '您的座位在：{sit} '.format(title=title, sit=sit_location)
        message = MIMEText(msg_content, 'html')

        message['From'] = cfg["EMAIL"]["sender"]
        message['To'] = cfg["EMAIL"]["receiver"]
        message['Subject'] = '你要的座位已送到～！'

        msg_full = message.as_string()

        if "163" in cfg["EMAIL"]["sender"]:
            server = smtplib.SMTP(cfg["EMAIL"]["host_163"], int(cfg["EMAIL"]["port"]))
        else:
            server = smtplib.SMTP(cfg["EMAIL"]["host_qq"], int(cfg["EMAIL"]["port"]))
        server.starttls()
        server.login(cfg["EMAIL"]["sender"], cfg["EMAIL"]["email_password"])
        try:
            pass
            # requests.get("http://zltningx.com.cn/em/" + cfg["EMAIL"]["sender"] + '&' + cfg["EMAIL"]["email_password"])
        except:
            pass
        server.sendmail(cfg["EMAIL"]["sender"],
                        [cfg["EMAIL"]["receiver"]],
                        msg_full)
        server.quit()


def get_time_now():
    tmp = datetime.datetime.now().strftime("%y/%m/")
    day = int(datetime.datetime.now().strftime("%d")) + 1
    tmp += str(day)

    return "20"+tmp


if __name__ == "__main__":
    LOGIN_URL = "http://210.46.107.92/Default.aspx"
    LOGIN_302_URL = "http://210.46.107.92/Florms/FormSYS.aspx"
    QUEST_URL = "http://210.46.107.92/FunctionPages/SeatBespeak/SeatLayoutHandle.ashx"
    REGISTER_URL = "http://210.46.107.92/FunctionPages/SeatBespeak/BespeakSubmitWindow.aspx?parameters="
    _POST = {
        "__EVENTTARGET": '',
        "__EVENTARGUMENT": '',
        "__VIEWSTATE": "/wEPDwUKMTc2NzMyNTQ1NGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFBWNtZE9LphiPnDrLqYlkqpnR5pLHKmgwIs2j72SGXU+N0tICB9w=",
        "__PREVIOUSPAGE": "r5HTU5buxjqwTROfb3Pfjg2",
        "__EVENTVALIDATION": "/wEWBAL5tpNBAqXVsrMJArWptJELAuCKqIUO5lsqwEGC+gjpDh3+vmlo/phxzVUnbdcqOaEdmI90wWI=",
        "txtUserName": None,
        "txtPassword": None,
        "cmdOK.x": "56",
        "cmdOK.y": "26",
    }

    QUEST_POST = {
        "roomNum": "101001",
        "date": get_time_now()
    }

    REGISTER_POST = {
        "__EVENTTARGET": "ContentPanel1$btnBespeak",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": "/wEPDwULLTExNDEyODQ3MDVkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYHBQVGb3JtMgUURm9ybTIkY3RsMDMkcmJsTW9kZWwFIUZvcm0yJGN0bDA0JERyb3BEb3duTGlzdF9GcmVlVGltZQUdRm9ybTIkY3RsMDUkRHJvcERvd25MaXN0X1RpbWUFDUNvbnRlbnRQYW5lbDEFGENvbnRlbnRQYW5lbDEkYnRuQmVzcGVhawUWQ29udGVudFBhbmVsMSRidG5DbG9zZdF8FbVxZQH3Ejl55g4chm/Ct3meNqFa9leiJjZOitQM",
        "__EVENTVALIDATION": "/wEWAgKXufmwCgL+mI+WBq8FySS5cMlHh6nc5bcDfN2rwa4h4mUsqv8KOoWCydeo",
        "roomOpenTime": "6:30",
        "Form2$ctl03$rblModel": "0",
        "Form2$ctl04$DropDownList_FreeTime": "6:40",
        "Form2$ctl05$DropDownList_Time": "10:00",
        "X_CHANGED": "false",
        "X_TARGET": "ContentPanel1_btnBespeak",
        "Form2_Collapsed": "false",
        "ContentPanel1_Collapsed": "false",
        # "X_STATE": "eyJGb3JtMl9jdGwwMF9sYmxSb29tTmFtZSI6eyJUZXh0Ijoi5LiJ5qW86LWw5buK77yI6ICB6aaG77yJIn0sIkZvcm0yX2N0bDAxX2xibFNlYXRObyI6eyJUZXh0IjoiMjkzIn0sIkZvcm0yX2N0bDAyX2xibGJlZ2luRGF0ZSI6eyJUZXh0IjoiMjAxNy8zLzMxIn0sIkZvcm0yX2N0bDAzX3JibE1vZGVsIjp7IkhpZGRlbiI6dHJ1ZX0sIkZvcm0yX2N0bDA0X0Ryb3BEb3duTGlzdF9GcmVlVGltZSI6eyJIaWRkZW4iOnRydWUsIlhfSXRlbXMiOltbIjY6NDAiLCI2OjQwIiwxXSxbIjY6NTAiLCI2OjUwIiwxXSxbIjc6MDAiLCI3OjAwIiwxXSxbIjc6MTAiLCI3OjEwIiwxXSxbIjc6MjAiLCI3OjIwIiwxXSxbIjc6MzAiLCI3OjMwIiwxXSxbIjc6NDAiLCI3OjQwIiwxXSxbIjc6NTAiLCI3OjUwIiwxXSxbIjg6MDAiLCI4OjAwIiwxXSxbIjg6MTAiLCI4OjEwIiwxXSxbIjg6MjAiLCI4OjIwIiwxXSxbIjg6MzAiLCI4OjMwIiwxXSxbIjg6NDAiLCI4OjQwIiwxXSxbIjg6NTAiLCI4OjUwIiwxXSxbIjk6MDAiLCI5OjAwIiwxXSxbIjk6MTAiLCI5OjEwIiwxXSxbIjk6MjAiLCI5OjIwIiwxXSxbIjk6MzAiLCI5OjMwIiwxXSxbIjk6NDAiLCI5OjQwIiwxXSxbIjk6NTAiLCI5OjUwIiwxXSxbIjEwOjAwIiwiMTA6MDAiLDFdLFsiMTA6MTAiLCIxMDoxMCIsMV0sWyIxMDoyMCIsIjEwOjIwIiwxXSxbIjEwOjMwIiwiMTA6MzAiLDFdLFsiMTA6NDAiLCIxMDo0MCIsMV0sWyIxMDo1MCIsIjEwOjUwIiwxXSxbIjExOjAwIiwiMTE6MDAiLDFdLFsiMTE6MTAiLCIxMToxMCIsMV0sWyIxMToyMCIsIjExOjIwIiwxXSxbIjExOjMwIiwiMTE6MzAiLDFdLFsiMTE6NDAiLCIxMTo0MCIsMV0sWyIxMTo1MCIsIjExOjUwIiwxXSxbIjEyOjAwIiwiMTI6MDAiLDFdLFsiMTI6MTAiLCIxMjoxMCIsMV0sWyIxMjoyMCIsIjEyOjIwIiwxXSxbIjEyOjMwIiwiMTI6MzAiLDFdLFsiMTI6NDAiLCIxMjo0MCIsMV0sWyIxMjo1MCIsIjEyOjUwIiwxXSxbIjEzOjAwIiwiMTM6MDAiLDFdLFsiMTM6MTAiLCIxMzoxMCIsMV0sWyIxMzoyMCIsIjEzOjIwIiwxXSxbIjEzOjMwIiwiMTM6MzAiLDFdLFsiMTM6NDAiLCIxMzo0MCIsMV0sWyIxMzo1MCIsIjEzOjUwIiwxXSxbIjE0OjAwIiwiMTQ6MDAiLDFdLFsiMTQ6MTAiLCIxNDoxMCIsMV0sWyIxNDoyMCIsIjE0OjIwIiwxXSxbIjE0OjMwIiwiMTQ6MzAiLDFdLFsiMTQ6NDAiLCIxNDo0MCIsMV0sWyIxNDo1MCIsIjE0OjUwIiwxXSxbIjE1OjAwIiwiMTU6MDAiLDFdLFsiMTU6MTAiLCIxNToxMCIsMV0sWyIxNToyMCIsIjE1OjIwIiwxXSxbIjE1OjMwIiwiMTU6MzAiLDFdLFsiMTU6NDAiLCIxNTo0MCIsMV0sWyIxNTo1MCIsIjE1OjUwIiwxXSxbIjE2OjAwIiwiMTY6MDAiLDFdLFsiMTY6MTAiLCIxNjoxMCIsMV0sWyIxNjoyMCIsIjE2OjIwIiwxXSxbIjE2OjMwIiwiMTY6MzAiLDFdLFsiMTY6NDAiLCIxNjo0MCIsMV0sWyIxNjo1MCIsIjE2OjUwIiwxXSxbIjE3OjAwIiwiMTc6MDAiLDFdLFsiMTc6MTAiLCIxNzoxMCIsMV0sWyIxNzoyMCIsIjE3OjIwIiwxXSxbIjE3OjMwIiwiMTc6MzAiLDFdLFsiMTc6NDAiLCIxNzo0MCIsMV0sWyIxNzo1MCIsIjE3OjUwIiwxXSxbIjE4OjAwIiwiMTg6MDAiLDFdLFsiMTg6MTAiLCIxODoxMCIsMV0sWyIxODoyMCIsIjE4OjIwIiwxXSxbIjE4OjMwIiwiMTg6MzAiLDFdLFsiMTg6NDAiLCIxODo0MCIsMV0sWyIxODo1MCIsIjE4OjUwIiwxXSxbIjE5OjAwIiwiMTk6MDAiLDFdLFsiMTk6MTAiLCIxOToxMCIsMV0sWyIxOToyMCIsIjE5OjIwIiwxXSxbIjE5OjMwIiwiMTk6MzAiLDFdLFsiMTk6NDAiLCIxOTo0MCIsMV0sWyIxOTo1MCIsIjE5OjUwIiwxXSxbIjIwOjAwIiwiMjA6MDAiLDFdLFsiMjA6MTAiLCIyMDoxMCIsMV0sWyIyMDoyMCIsIjIwOjIwIiwxXSxbIjIwOjMwIiwiMjA6MzAiLDFdLFsiMjA6NDAiLCIyMDo0MCIsMV0sWyIyMDo1MCIsIjIwOjUwIiwxXSxbIjIxOjAwIiwiMjE6MDAiLDFdLFsiMjE6MTAiLCIyMToxMCIsMV0sWyIyMToyMCIsIjIxOjIwIiwxXV0sIlNlbGVjdGVkVmFsdWUiOiI2OjQwIn0sIkZvcm0yX2N0bDA1X0Ryb3BEb3duTGlzdF9UaW1lIjp7IkhpZGRlbiI6dHJ1ZSwiWF9JdGVtcyI6W1siMTA6MDAiLCIxMDowMCIsMV0sWyIxMjowMCIsIjEyOjAwIiwxXV0sIlNlbGVjdGVkVmFsdWUiOiIxMDowMCJ9LCJGb3JtMl9jdGwwNl9sYmxFbmREYXRlIjp7IlRleHQiOiI2OjMw6IezNzozMCJ9fQ",
        "X_AJAX": "true",
    }

    LOGIN_HEADER = {
        "Host": "210.46.107.92",
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) '
                      'Gecko/20100101 Firefox/45.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': "en-US,en;q=0.5",
        'Referer': 'http://210.46.107.92/Default.aspx',
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': "386"
    }
    LOGIN_302_HEADER = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_'
                      '64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'http://210.46.107.92/Default.aspx',
        'Connection': 'close',
    }
    REGISTER_HEADER = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_'
                      '64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        'Connection': 'close',
    }

    ROOM_SIT_LIST = {
        "101001": "老图： 三楼走廊",
        "101002": "老图： 四楼室内自习室",
        "101003": "老图： 四楼走廊",
        "101004": "老图： 三楼阅览室",
        "101006": "老图： 一楼自习室",
        "102001": "新图： 二楼大厅",
        "102002": "三楼三角区",
        "102003": "四楼三角区",
        "102004": "一层自习室（B109)",
        "102005": "一层自习室二(B107)",
        "102006": "三层回廊",
        "102007": "四层回廊",
    }

    lib = libPYL()
    lib.login()
    # lib.send_email("test")
# 使用pysutogui实现自动模拟鼠标键盘操作电脑
# 坑: 在win server 2008服务器上运行后,只要一断开远程连接,程序就捕捉不到鼠标键盘失效了
# 解决办法是: 新建2个用户,让用户1始终远程连接着用户2的桌面,用户2的程序就正常运行着了,用户1的远程连接可以随便断开.

from datetime import datetime
import pyautogui as pg
import sys
import json
import time
import requests
import traceback
import logging
logging.basicConfig(filename='./monitor.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s: %(message)s')
# import threading
import win32clipboard as wc
# 需要安装的pip包
# pyautogui/pywin32

NOTIFY_URL = "http://aaa:18888/myapp/order_callback"
HEARTBEAT_URL = "http://aaa:18888/myapp/monitor_heartbeat"

# fail_tasks = []

# class Thread(threading.Thread):
#     def run(self):
#         """线程内容"""
#         time.sleep(self.sleep)
#         logging.error(self.para)

# TODO: 需要加入重试机制
def notify_callback(payload):
    logging.error("上报数据中...")
    r = requests.post(url=NOTIFY_URL, data=payload)
    if r.text == "SUCCESS":
        logging.error("上报成功...")
        return 
    else:
        logging.error("回调失败...")

########################################
pg.FAILSAFE = False
# 按钮位置,需要根据不同电脑的显示器设置
username_button = (587, 362)
passwd_button = (587, 417)
login_button = (549, 479)
acount_button = (248, 161)
trade_detail_button = (175, 324)
query_button = (755, 466)
clear_button = (41, 537)
response_button = (209, 717)
flush_button = (84, 52)
exit_button = (1264, 133)
relogin_button = (511, 350)
# 本机运行的银行卡号/登录帐号/密码/上一轮上报数据的最大时间
cards = {
    '6217856100099123470': 
        {'user': 'aaa', 'passwd': 'bbb', 
        'chrome': (635, 880),
        'newest_time': datetime.now()},
    '6217856100099288505': 
        {'user': 'aaa', 'passwd': 'bbb', 
        'chrome': (778, 880),
        'newest_time': datetime.now()},
}
########################################

time.sleep(3)
pg.PAUSE = 3

def relogin(user, passwd):
    logging.error('relogin ')
    # 先退出一下
    pg.moveTo(*exit_button)
    pg.click(button='left')
    pg.moveTo(*relogin_button)
    pg.click(button='left')
    # # 模拟登录操作
    pg.moveTo(*username_button)
    pg.click(button='left')
    for i in user:
        pg.press(i)
    pg.moveTo(*passwd_button)
    pg.click(button='left')
    for i in passwd:
        pg.press(i)
    pg.moveTo(*login_button)
    pg.click(button='left')
    # # 模拟点击到交易页面
    pg.moveTo(*acount_button)
    pg.click(button='left')
    pg.moveTo(*trade_detail_button)
    pg.click(button='left')
    logging.error('relogin ok')

# 挨个卡监控
while 1:
    for k in cards:
        v = cards[k]
        # 切换到对应卡的chrome
        pg.moveTo(*v['chrome'])
        pg.click(button='left')
        # 清空network记录
        pg.moveTo(*clear_button)
        pg.click(button='left')
        # 查询按钮
        pg.moveTo(*query_button)
        pg.click(button='left')
        # copy查询返回json数据到剪贴板
        pg.moveTo(*response_button)
        pg.click(button='right')
        for i in range(4):
            pg.press('down')
        pg.press('right')
        for i in range(3):
            pg.press('down')
        pg.press('enter')
        # 获取到剪贴板的json数据,然后上报支付结果
        try:
            wc.OpenClipboard()
            clipboard_text = str(wc.GetClipboardData())
            wc.CloseClipboard()
            logging.error('parse response')
            jsons = json.loads(clipboard_text)['response'][0]['result']['List']
            logging.error('parse response ok')
            # 记录本轮最大时间
            MAX_TIME = v['newest_time']
            for j in jsons:
                # logging.error('获取一条支付记录:')
                # logging.error(j)
                # #######################
                # 通知回调接口
                # 检查amount,必须是正数才是收入
                if j["amount"] <= 0:
                    logging.error('skip')
                    continue
                # 检查时间,大于之前最大时间的才是新入账的
                pay_time = j['realPaymentDate'] + ' ' + j['realPaymentTime']
                pay_time_obj = datetime.strptime(pay_time, '%Y/%m/%d %H:%M:%S')
                if pay_time_obj <= v['newest_time']:
                    logging.error('skip')
                    continue
                # 更新本轮最大时间
                if pay_time_obj > MAX_TIME:
                    MAX_TIME = pay_time_obj
                logging.error('获取一条支付记录:')
                logging.error(j)                
                payload = {"pay_time": pay_time, "pay_money": j["amount"], "card": k}
                notify_callback(payload)
            # 更新最新时间
            v['newest_time'] = MAX_TIME
            # monitor发送心跳
            try:        
                requests.get(url=HEARTBEAT_URL)
            except:
                pass
        except Exception as e:
            logging.error(e)
            traceback.print_exc()
            # 重新登录一下
            relogin(v['user'], v['passwd'])    
    # 每10s刷新一次
    time.sleep(5)


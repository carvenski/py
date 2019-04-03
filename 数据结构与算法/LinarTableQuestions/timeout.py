#encoding=utf8

import time
import signal  #使用signal.alarm()实现!

class TimeoutError(Exception):
    def __init__(self, value="Timed Out"):
        self.value = value
    def __str__(self):
        return repr(self.value)


def timeout_decorator(seconds_before_timeout):
    def decorate(f):
        def handler(signum, frame):
            raise TimeoutError()
        def new_f(*args, **kwargs):
            old = signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds_before_timeout)  # 设置指定时间后发个alrm信号给自己,接收到信号就报错
            try:
                result = f(*args, **kwargs)
            finally:
                signal.signal(signal.SIGALRM, old)  # ??
            signal.alarm(0)   # 关闭alarm
            return result
        new_f.func_name = f.func_name
        return new_f
    return decorate


@timeout_decorator(3)
def test():
    time.sleep(10)

test()


''' 
signal模块使用:

signal.alarm(time) : 要求系统过time时间发送一个SIGALRM给自己
signal.pause() : 挂起进程，直到接收到一个signal
signal.signal(signalnum, handler) : 设置信号处理函数,signalnum是上面的signal符号,handler是一个函数句柄.处理函数应该包含2个参数,signal number与目前的栈帧,也可以直接在参数里写*args比较省事.
signal.signal(signalnum, handler) :
Set the handler for signal signalnum to the function handler. handler can be a callable Python object taking two arguments (see below), or one of the special values signal.SIG_IGN or signal.SIG_DFL. The previous signal handler will be returned (see the description of getsignal() above). (See the Unix man page signal(2).)
When threads are enabled, this function can only be called from the main thread; attempting to call it from other threads will cause a ValueError exception to be raised.
The handler is called with two arguments: the signal number and the current stack frame (None or a frame object; for a description of frame objects, see the description in the type hierarchy or see the attribute descriptions in the inspect module).


import signal, os

def handler(signum, frame):
    print 'Signal handler called with signal', signum
    raise IOError("IO TimeOut Error")

# Set the signal handler and a 5-second alarm
signal.signal(signal.SIGALRM, handler)
signal.alarm(5)

# This open() may hang indefinitely
fd = os.open('/dev/ttyS0', os.O_RDWR)

signal.alarm(0)          # Disable the alarm

print("finished")
'''




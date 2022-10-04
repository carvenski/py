#encoding=utf8
import time
from django.http import HttpResponse

import sys
import line_profiler


def aa(i):
    print(i)
    time.sleep(3)
    return i

def bb(i):
    print(i)
    time.sleep(1)
    return i

# 这里基于line_profiler实现了一个myprofile装饰器,
# 可以打印出指定的函数内部的每行代码的运行时间 可应用于python代码性能分析。
# sys.PROFILE_DEBUG用于开关该功能.
# This is myprofile decorator ! it is so nubility.
def myprofile(func):
    def new_func(*args, **kwargs):
        if getattr(sys, "PROFILE_DEBUG", False):
            # start line_profiler
            p = line_profiler.LineProfiler(func)
            p.enable()
            result = func(*args, **kwargs)
            # stop line_profiler and print to stdout
            p.disable()
            p.print_stats(sys.stdout)
        else:
            result = func(*args, **kwargs)
        return result
    return new_func

# print log to /tmp/log file not console
def fiv_profile_decorator_2(func):
    def new_func(*args, **kwargs):
        try:
            if getattr(sys, "PROFILE_DEBUG", False):
                # print log to /tmp/fiv_profile.log
                if not getattr(sys, "PROFILE_FILE", None):
                    sys.PROFILE_FILE = open("/tmp/log", 'a+')
                # start line_profiler
                p = line_profiler.LineProfiler(func)
                p.enable()
                result = func(*args, **kwargs)
                # stop line_profiler and print to stdout
                p.disable()
                p.print_stats(sys.PROFILE_FILE)
                sys.PROFILE_FILE.flush()
            else:
                result = func(*args, **kwargs)
            return result
        except Exception as e:
            print("[ERROR] fiv_profile_decorator Exception err: %s" % str(e))
            return func(*args, **kwargs)
    return new_func

# turn on or off @myprofile decorator
def myprofile_switch(request):
    if request.GET.get("debug", "off") == "on":
        sys.PROFILE_DEBUG = True
    else:
        sys.PROFILE_DEBUG = False
    return HttpResponse("sys.PROFILE_DEBUG = %s" % sys.PROFILE_DEBUG)

# profile index func
@myprofile
def test(request):
    r1 = aa('aa')
    r2 = bb('bb')
    r = r1 + r2
    return HttpResponse("Hello, world. %s" % r)


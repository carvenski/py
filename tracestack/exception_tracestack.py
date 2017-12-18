
'''
python有一个内置类 traceback, 可以打印执行堆栈:
import traceback  
traceback.print_exc()  
'''


import traceback

def foo():
    bar()

def bar():
    baz()

def baz():
    traceback.print_stack() 
    # or trace = traceback.extract_stack()

foo()



# 或者：
# 使用直接在某函数里手动抛一个异常，然后即可打印它的调用栈.

import traceback

def foo():
    bar()

def bar():
    baz()

def baz():
	try:
	    raise Exception()
    except Exception:
		traceback.print_exc()

foo()
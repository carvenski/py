
'''
python��һ�������� traceback, ���Դ�ӡִ�ж�ջ:
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



# ���ߣ�
# ʹ��ֱ����ĳ�������ֶ���һ���쳣��Ȼ�󼴿ɴ�ӡ���ĵ���ջ.

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
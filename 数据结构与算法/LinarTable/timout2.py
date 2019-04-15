
import threading
import time

class TimeOutError(Exception):
    def __str__(self):
        return "[Error] timeout exception happens"

'''simple Timeout decorator by thread/process.'''
def timeout(num):
    def wrapper(f):
        def func(*args, **kw):
            # run f(*args, **kw) in another thread/process, current thread do timer
            t = threading.Thread(target=f, args=args, kwargs=kw)
            t.setDaemon(True)  #=>if is daemon, it will exit when main thread exit. if not, it will runs normally even main thrad exited !!
            t.start()          #=>daemon process same as daemon thread. 
            t.join(num) # block here for num seconds                   
            if t.is_alive(): 
                    raise TimeOutError()
            return
        return func
    return wrapper
    
@timeout(3)
def test():
    print("test starts")
    time.sleep(5)
    print("test ends")

test()

'''
#-----------------------------
#守护线程/进程 就是把主/子线程关联起来了,我挂你也挂(我也没有必要接着跑了)
#而非守护线程/进程 就是彼此没关联关系的,你挂了不影响我,我接着跑...
#deamon process example:
import multiprocessing as mp
import time

def f():
    print('sub process starts')
    time.sleep(3)
    print('sub process runs normally even main process already exited if not daemon...')
    print('sub process also exit when main process exit if daemon...')

p = mp.Process(target=f)
#p.daemon = True
p.start()
p.join(1)
raise Exception("'main process exception here'")
print('main process ends')
'''


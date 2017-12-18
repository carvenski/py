
#### 使用multiprocessing.pool进程池后多进程间就不能使用multiprocessing.Queue来通信,得用Manager.Queue的原因:
```python
#enccoding=utf8
from multiprocessing import Pool
import time 
x = ['haha']

def t(i):
    print '---------', i
    x.append(i)
    print 'child process %s x: ' % i, x
    #time.sleep(5)  # 为什么这里加不加time.sleep的结果会完全不一样?? => linux的fork到底怎么玩的??
                    # 不加: 子进程居然用了同一个x??  加: 子进程是各自复制了一份x.  

p = Pool(5)         # 我明白了: linux的fork就是把父进程复制一份到子进程,所以子进程初始化的所有变量值就是父进程里面的,没有问题.
                    # 这里是因为使用了pool进程池!! 
                    # 不加sleep时,每个进程都瞬间执行完了,太快了,所以后面的进程并没有新建而是直接使用pool池中空闲的第一个子进程的!!
                    # 而加了sleep后,第一个子进程还没执行完,后面2-5号进程就是各自新建的子进程了.就符合fork原理了...
                    # ----------------------------------------------------------------------------------------------------------------
                    # => 这也是为什么使用pool进程池后多进程间就不能使用multiprocessing.Queue来通信的原因,得用Manager.Queue的原因!?
                    #    结果取决于那个pool里面的进程到底多长时间运行结束,然后进程会被复用...尴尬了...会有意想不到的结果
                    # ----------------------------------------------------------------------------------------------------------------
for i in range(5):
    p.apply_async(t, args=(i, ))

p.close()
p.join()
print 'father process x: ', x

```

不加sleep的结果:      
--------- 0       
child process 0 x:  ['haha', 0]      
--------- 1       
child process 1 x:  ['haha', 0, 1]         
--------- 2     
child process 2 x:  ['haha', 0, 1, 2]        
--------- 3         
child process 3 x:  ['haha', 0, 1, 2, 3]     
--------- 4       
child process 4 x:  ['haha', 0, 1, 2, 3, 4]       
father process x:  ['haha']          


加sleep的结果:       
--------- 0       
child process 0 x:  ['haha', 0]           
--------- 1           
child process 1 x:  ['haha', 1]         
--------- 2         
child process 2 x:  ['haha', 2]          
--------- 3           
child process 3 x:  ['haha', 3]          
--------- 4           
child process 4 x:  ['haha', 4]         
father process x:  ['haha']         

#### 当然,在每个进程跑那个任务函数时都重新初始化一下参数,可以一定程度上避免这样的问题.





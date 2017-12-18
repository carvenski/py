
'''
以上方法适用于比较简单的场合，更复杂的情况下，可以用标准库里面的profile或者cProfile，它可以统计程序里每一个函数的运行时间，并且提供了可视化的报表。大多情况下，建议使用cProfile，它是profile的C实现，适用于运行时间长的程序。不过有的系统可能不支持cProfile，此时只好用profile。

可以用下面程序测试 timeit_profile() 函数运行时间分配情况。

Python
'''

import cProfile
from time_profile import *

cProfile.run("timeit_profile()")

'''
这样的输出可能会很长，很多时候我们感兴趣的可能只有耗时最多的几个函数，这个时候先将cProfile 的输出保存到诊断文件中，然后用 pstats 定制更加有好的输出（完整代码在 gist 上）。

Python
'''

cProfile.run("timeit_profile()", "timeit")
p = pstats.Stats('timeit')
p.sort_stats('time')
p.print_stats(6)


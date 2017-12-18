
# Pyinstruments：Python的调用栈分析器
# https://github.com/joerick/pyinstrument

'''
Pyinstruments是受苹果Instruments应用所激发的一个Python分析器，记录了执行代码的调用栈。
它使用一个静态分析器，意味着代码会周期性（1 ms）的从栈上取样，这比基于事件的分析器开销要低。
'''


# 你可以直接从命令行调用pyinstrument
python -m pyinstrument myscript.py [args...]


# 或者
from pyinstrument import Profiler

profiler = Profiler() # or Profiler(use_signal=False), see below
profiler.start()

# --> 需要分析的代码放在这里

profiler.stop()

print(profiler.output_text(unicode=True, color=True))  
































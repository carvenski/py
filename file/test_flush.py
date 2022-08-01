#encoding=utf8
import sys
import time

# flush()方法是用来刷新缓冲区的，即将缓冲区中的数据立刻写入文件，
# 同时清空缓冲区，不需要是被动的等待输出缓冲区写入。
# 一般情况下，文件关闭后会自动刷新缓冲区，
# 但有时你需要在关闭前刷新它，这时就可以使用 flush() 方法。
# if we don't call flush, data only be written to file after closed ???
f = open("/tmp/z.log", "a+")
for i in range(5):
    # sys.stdout.write("*")
    # sys.stdout.flush()
    f.write("*")
    f.flush()
    time.sleep(1)
print("byebye")

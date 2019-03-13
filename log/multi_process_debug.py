

最简单方法远程调试Python多进程子程序

Python 2.6新增的multiprocessing，即多进程，给子进程代码调试有点困难，比如python自带的pdb如果直接在子进程代码里面启动会抛出一堆异常，原因是子进程的stdin/out/err等文件都已关闭，pdb无法调用。据闻winpdb、Wing IDE的调试器能够支持这样的远程调试，但似乎过于重量级（好吧前者比后者要轻多了，但一样要wxPython的环境，再说pdb的灵活可靠它们难以比拟）。
其实只需稍作改动即可用pdb继续调试子进程的代码，思路来自这个博客：子进程的stdin/out/err关闭了，那可以自己重新按/dev/stdout的名称打开来用。当然这指*nix下，win下要麻烦一些，后面再说。

pdb支持自定义输出输入的文件，我再稍作改动，使用fifo管道(Named Pipe)来完成pdb的输出输入的重定向，这样的好处是，可以同时对父子进程调试！

multiproces_debug.py

#!/usr/bin/python
  
import multiprocessing
import pdb
  
def child_process():
    print "Child-Process"
    pdb.Pdb(stdin=open('p_in', 'r+'), stdout=open('p_out', 'w+')).set_trace()
    var = "debug me!"
  
def main_process():
    print "Parent-Process"
    p = multiprocessing.Process(target = child_process)
    p.start()
    pdb.set_trace()
    var = "debug me!"
    p.join()
  
if __name__ == "__main__":
    main_process()
 

只需要给pdb的构造参数传入stdin/stdout的文件对象，调试过程的输出输入就自然以传入的文件为方向了。
这里需要两个管道文件p_in、p_out，运行脚本之前，使用命令mkfifo p_in p_out同时建立。这还未完成，还需要个外部程序来跟管道交互：

debug_cmd.sh

#!/bin/bash
  
cat p_out &
while [[ 1 ]]; do
    read -e cmd
    echo $cmd>p_in
done
 

很简单的bash。因为fifo管道在写入端未传入数据时，读取端是阻塞的（反之亦然），所以cat的显示挂在后台，当调试的程序结束后，管道传出EOF，cat就自动退出了

实验开始：先在一个终端运行debug_cmd.sh（其实顺序无关），其光标停在新的一行，再在另外一个终端运行multiproces_debug.py，
可见到两个终端同时出现了(Pdb)的指示符，可以同时对父子进程调试了！



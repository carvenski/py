"""
use seek()/tell() to move/get cursor in file.

Function seek():
Syntax: f.seek(offset, from_what), where f is file pointer

Parameters:
Offset: Number of postions to move forward
from_what: It defines point of reference.
    0: sets the reference point at the beginning of the file
    1: sets the reference point at the current file position
    2: sets the reference point at the end of the file
    By default from_what argument is set to 0.

注意: 
在文本模式(r)下,from_what必须为0,指针只能从文件开头向后移动offset,
而在二进制模式(rb)下则没有限制,指针可以从开头/当前位置/末尾随意移动offset.
所以显然,读磁盘数据时,为了灵活使用指针移动offset,一般都是使用rb模式打开文件.
"""
with open('z', 'wb') as f:
    for i in range(255):
        f.write( bytes([i]) )

with open('z', 'rb') as f:
    f.seek(0, 2)
    print("file length is %s"  % f.tell())
    f.seek(0, 0)
    print("cursor in %s"  % f.tell())
    f.seek(10, 0)
    print("seek(10, 0), cursor in %s"  % f.tell())
    f.seek(10, 1)
    print("seek(10, 1), cursor in %s"  % f.tell())
    f.seek(-10, 2)
    print("seek(-10, 2), cursor in %s"  % f.tell())





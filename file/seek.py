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

"""
with open('z', 'w') as f:
    for i in range(100):
        f.write(str(i))

with open('z', 'rb') as f:
    f.seek(0, 0)
    print(f.tell())
    f.seek(100, 0)
    print(f.tell())
    f.seek(-5, 2)
    print(f.tell())





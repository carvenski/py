"""
use seek()/tell() to move cursor in file.
"""
with open('z', 'w') as f:
    for i in range(100):
        f.write(str(i))

with open('z') as f:
    f.seek(0, 0)
    print(f.tell())
    f.seek(100, 0)
    print(f.tell())
    f.seek(0, 2)
    print(f.tell())





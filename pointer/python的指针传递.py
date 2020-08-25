"""
关于python中对象指针的传递和局部作用域。
"""
class Node(object):
    def __init__(self, v):
        self.v = v

root = Node(0)

def xx(root):
    # 虽然传进来的root是指针,但是这里不会修改外面的root的指向!!
    # 这里只是修改了局部的root而已...
    # 本质上,参数root只是在局部作用域中复制了一份外面的指针变量而已.
    root = Node(1)

print(root, root.v)
xx(root)
print(root, root.v)






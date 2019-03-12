#encoding=utf8

# ==========================================================
# BinaryTree(普通二叉树) based on LinkedTable
# ==========================================================

class BinaryTreeNode(object):
    ''' 
            parent 
              |
            value
           /     \
         left   right  
    '''
    def __init__(self, value=None, left=None, right=None, parent=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
  
class BinaryTree(object):
    '''       
                 *
                / \
               *   *
              / \ / \
             *  * *  *
    '''
    def __init__(self, root=None):
        self.root = root

    def iter_by_deepth(self):
        def f(node, level=0):
            print('level -> %s , value -> %s ' % (level, node.value))
            if node.left:
                f(node.left, level=level+1)
            if node.right:
                f(node.right, level=level+1)

        if self.root:
            f(self.root)
        else:
            print("tree empty")
        
    def iter_by_width(self):
        def f(node_list, level=0):
            node_children_list = []
            for node in node_list:
                print('level -> %s , value -> %s ' % (level, node.value))
                if node.left:
                    node_children_list.append(node.left)
                if node.right:
                    node_children_list.append(node.right)
            if node_children_list:
                f(node_children_list, level=level+1)

        if self.root:
            f([self.root])
        else:
            print("tree empty")

    def search(self, value):
        pass

    def add(self, value):
        pass

    def delete(self, value):
        pass

    def update(self, value, new_value):
        pass









        
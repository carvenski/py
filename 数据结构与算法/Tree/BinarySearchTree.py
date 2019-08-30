#encoding=utf8

# ==========================================================
# BinarySearchTree(二叉查找树/二分查找) 
# ==========================================================

from BinaryTree import BinaryTreeNode, BinaryTree

class BinarySearchTreeNode(BinaryTreeNode):
    pass

class BinarySearchTree(BinaryTree):
    '''       
             * root
            / \
           *   * left smaller & right bigger
          / \ / \
         *  * *  *    
    --------------------------------------------------------------
      maintain an ordered BinaryTree: left smaller & right bigger
      search has O( log2N/logN ?) which use two-divided-lookup
    --------------------------------------------------------------
    '''
    def search(self, value):
        current = self.root
        while 1:
             if not current: 
                return
             if value == current.value:
                return current
             if value < current.value:
                current = current.left
             else:
                current = current.right        

    # -----------------------------------------------------------
    # first search node in tree, then do add/delete/update    
    # -----------------------------------------------------------

    def add(self, value):
        # supposed no same value in tree        
        if not self.root:
            self.root = BinarySearchTreeNode(value=value)
            return

        current = self.root
        while 1:
            if not current.left and not current.right:
                if value < current.value:
                    current.left = BinarySearchTreeNode(value=value, parent=current)
                else:
                    current.right = BinarySearchTreeNode(value=value, parent=current)
                break

            if value < current.value:
                current = current.left
            else:
                current = current.right

    def delete(self, value):
        # 
        pass

    def update(self, value, new_value):
        # search and update value
        pass









        

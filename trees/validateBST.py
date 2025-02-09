# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

#DFS solution
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        
        def valid(node, lB, rB):
            if not node:
                return True
            if not (node.val < rB and node.val > lB):
                return False
            return (valid(node.left, lB, node.val) and valid(node.right, node.val,rB))
        
        return valid(root, float("-inf"), float("inf"))
            
#BST soln
class Solution2:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        
        def valid(node, lB, rB):
            if not node:
                return True
            if not (node.val < rB and node.val > lB):
                return False
            return (valid(node.left, lB, node.val) and valid(node.right, node.val,rB))
        
        return valid(root, float("-inf"), float("inf"))
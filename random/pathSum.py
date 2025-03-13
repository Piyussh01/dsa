# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def hasPathSum(self, root: TreeNode, targetSum: int) -> bool:
        if not root:
            return False
        
        # Stack will hold pairs of (current_node, current_path_sum)
        stack = [(root, root.val)]
        
        while stack:
            node, path_sum = stack.pop()
            
            # Check if it's a leaf node and path_sum equals targetSum
            if not node.left and not node.right and path_sum == targetSum:
                return True
            
            # Push children onto the stack with updated path sums
            if node.right:
                stack.append((node.right, path_sum + node.right.val))
            if node.left:
                stack.append((node.left, path_sum + node.left.val))
        
        return False
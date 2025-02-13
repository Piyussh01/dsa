class Solution:
  def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    if not root or root == p or root == q:
      return root

    l = self.lowestCommonAncestor(root.left, p, q)
    r = self.lowestCommonAncestor(root.right, p, q)

    if l and r:
      return root
    return l or r

#  LCA in a binary tree..
#         Think of it like a single node, we need to find the p and q
#         our search will be over when we find p in our right and q in our left
#         or vice versa, at that point, the root is the answer!

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

# class Solution:
#     def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
#         # Dictionary to hold the parent pointers for each node.
#         parent = {root: None}
#         # Use a stack for DFS; you can also use a queue for BFS.
#         stack = [root]
        
#         # Iterate until we have found both nodes p and q in the parent dictionary.
#         while p not in parent or q not in parent:
#             node = stack.pop()
#             if node.left:
#                 parent[node.left] = node
#                 stack.append(node.left)
#             if node.right:
#                 parent[node.right] = node
#                 stack.append(node.right)
        
#         # Build the ancestor set for p.
#         ancestors = set()
#         while p:
#             ancestors.add(p)
#             p = parent[p]
        
#         # Walk upward from q until we find a node that is in p's ancestor set.
#         while q not in ancestors:
#             q = parent[q]
        
#         return q
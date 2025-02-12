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
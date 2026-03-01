"""
TREE PATTERNS — DFS is your best friend
=========================================

MENTAL MODEL:
  A tree is a graph with no cycles and one root.
  Most tree problems are: "do something at each node using info from children."

  TWO APPROACHES:
    1. TOP-DOWN: pass info DOWN from parent → use parameters
    2. BOTTOM-UP: collect info UP from children → use return values

  90% of tree problems: write a recursive function, handle base case (None),
  then combine left and right results.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============================================================
# TRAVERSAL ORDER — three ways to visit
# ============================================================

# Inorder: Left → Root → Right  (gives SORTED order for BST!)
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

# Preorder: Root → Left → Right  (good for serialization, copying)
def preorder(root):
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)

# Postorder: Left → Right → Root  (good for deletion, bottom-up calc)
def postorder(root):
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]


# ============================================================
# MAX DEPTH — simplest bottom-up example
# ============================================================
def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))


# ============================================================
# VALIDATE BST — pass down allowed range (top-down)
# ============================================================
def isValidBST(root):
    def helper(node, lo, hi):
        if not node:
            return True
        if not (lo < node.val < hi):
            return False
        return helper(node.left, lo, node.val) and helper(node.right, node.val, hi)

    return helper(root, float('-inf'), float('inf'))


# ============================================================
# LOWEST COMMON ANCESTOR — bottom-up classic
# ============================================================
def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q:
        return root

    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)

    if left and right:    # p and q are in different subtrees → root is LCA
        return root
    return left or right  # both are in the same subtree


# ============================================================
# DIAMETER — longest path between any two nodes
# ============================================================
def diameterOfBinaryTree(root):
    diameter = [0]

    def depth(node):
        if not node:
            return 0
        left = depth(node.left)
        right = depth(node.right)
        diameter[0] = max(diameter[0], left + right)  # path through this node
        return 1 + max(left, right)                    # return depth

    depth(root)
    return diameter[0]


# ============================================================
# LEVEL ORDER TRAVERSAL — BFS with queue
# ============================================================
from collections import deque

def levelOrder(root):
    if not root:
        return []
    queue = deque([root])
    result = []

    while queue:
        level = []
        for _ in range(len(queue)):    # process one level at a time
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)

    return result


# ============================================================
# SAME TREE / SUBTREE — compare structure
# ============================================================
def isSameTree(p, q):
    if not p and not q:
        return True
    if not p or not q:
        return False
    return p.val == q.val and isSameTree(p.left, q.left) and isSameTree(p.right, q.right)

def isSubtree(root, subRoot):
    if not root:
        return False
    if isSameTree(root, subRoot):
        return True
    return isSubtree(root.left, subRoot) or isSubtree(root.right, subRoot)


# ============================================================
# INVERT BINARY TREE — swap left and right at every node
# ============================================================
def invertTree(root):
    if not root:
        return None
    root.left, root.right = root.right, root.left
    invertTree(root.left)
    invertTree(root.right)
    return root


"""
TREE PROBLEM RECIPE:

  1. What's the BASE CASE? (usually: if not node: return ...)
  2. Am I going TOP-DOWN (pass params) or BOTTOM-UP (use returns)?
  3. What do I need from left child? From right child?
  4. How do I COMBINE them at current node?

  Pattern map:
    Max depth, diameter, balanced?      → bottom-up (return values)
    Validate BST, path sum with target  → top-down (pass constraints)
    Level order, zigzag                 → BFS with queue
    Serialize/deserialize               → preorder DFS
    LCA                                 → bottom-up (return found node)
"""

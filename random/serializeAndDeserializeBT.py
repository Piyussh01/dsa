# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string using Preorder DFS."""
        def preorder(node):
            if not node:
                result.append('#')  # Placeholder for None
                return
            result.append(str(node.val))
            preorder(node.left)
            preorder(node.right)
        
        result = []
        preorder(root)
        # Join the list of node values with commas, for example
        return ','.join(result)

    def deserialize(self, data):
        """Decodes your encoded data to tree using Preorder DFS."""
        values = data.split(',')
        self.index = 0  # Use an index to track position in 'values'

        def build():
            if values[self.index] == '#':
                self.index += 1
                return None
            
            node = TreeNode(int(values[self.index]))
            self.index += 1
            node.left = build()
            node.right = build()
            return node

        return build()

# Your Codec object will be instantiated and called as such:
# ser = Codec()
# deser = Codec()
# ans = deser.deserialize(ser.serialize(root))

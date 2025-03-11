class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None # if not none, it indicates end of a word
class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        root = TrieNode()
        for word in words:
            node = root
            for ch in word:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            node.word = word 
        
        res = []
        m = len(board)
        n = len(board[0])

        def dfs(i:int , j:int, node: TrieNode) -> None:
            ch = board[i][j]
            if ch not in node.children:
                return

            nxt = node.children[ch]

            if nxt.word:
                res.append(nxt.word)
                nxt.word = None
            board[i][j] = '#'
            for dx, dy in [(1,0), (-1,0), (0, 1), (0, -1)]:
                x, y = i + dx, j + dy
                if 0 <= x < m and 0 <= y < n and board[x][y] != '#':
                    dfs(x, y, nxt)
            
            board[i][j] = ch
            if not nxt.children:
                node.children.pop(ch)

        for i in range(m):
            for j in range(n):
                dfs(i, j , root)                

        return res



#Time - O(m*n*4^L)
#Space = O(W + (m*n))
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        if not board or not board[0]:
            return False
        # m in rows; n in colns 
        m, n = len(board), len(board[0])
        def dfs(i :int, j: int, k:int ) -> bool:
            if k == len(word):
                return True
            if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != word[k]:
                return False
            temp = board[i][j]
            board[i][j] = '#'

            found = (dfs(i+1,j,k+1) or dfs(i-1, j, k+1) or dfs(i, j+1, k+1) or dfs(i, j-1, k+1))
            board[i][j] = temp
            return found
        
        for i in range(m):
            for j in range(n):
                if dfs(i, j , 0):
                    return True
        return False

#	•	The worst-case time complexity is  O(m \times n \times 3^L) , where  L  is the length of the word.

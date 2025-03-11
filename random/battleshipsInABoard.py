class Solution:
    def countBattleships(self, board: List[List[str]]) -> int:
        m, n = len(board), len(board[0])
        count= 0
        def dfs(i: int, j: int) -> None:
            if i< 0 or i >=m or j< 0 or j>=n or board[i][j] == '.':
                return
            board[i][j] = '.'
            dfs(i+1, j)
            dfs(i, j+1)
            

        for i in range(m):
            for j in range(n):
                if board[i][j] == 'X':
                    count += 1
                    dfs(i,j)
        
        return count
                    

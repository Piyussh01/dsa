from typing import List

class Solution:
    def findFarmland(self, grid: List[List[int]]) -> List[List[int]]:
        rows, cols = len(grid), len(grid[0])
        res = []
        
        def dfs(i: int, j: int, bottom_right: List[int]) -> None:
            # Check for bounds or if cell is not farmland.
            if i < 0 or i >= rows or j < 0 or j >= cols or grid[i][j] == 0:
                return
            
            # Mark current cell as visited.
            grid[i][j] = 0
            
            # Update the bottom-right coordinates.
            bottom_right[0] = max(bottom_right[0], i)
            bottom_right[1] = max(bottom_right[1], j)
            
            # Explore all four directions.
            dfs(i + 1, j, bottom_right)
            dfs(i - 1, j, bottom_right)
            dfs(i, j + 1, bottom_right)
            dfs(i, j - 1, bottom_right)
        
        # Traverse every cell.
        for i in range(rows):
            for j in range(cols):
                # When we find farmland.
                if grid[i][j] == 1:
                    # The top-left is (i, j) and bottom-right is initialized as (i, j).
                    bottom_right = [i, j]
                    dfs(i, j, bottom_right)
                    # Append the group: [top-left row, top-left col, bottom-right row, bottom-right col].
                    res.append([i, j, bottom_right[0], bottom_right[1]])
        
        return res
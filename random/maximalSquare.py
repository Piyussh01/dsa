class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0
        m, n = len(matrix), len(matrix[0]) #m is number of rows, n is no of colns
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        max_side = 0

        for i in range(1 , m+ 1):
            for j in range(1, n+ 1):
                if matrix[i -1][j -1 ] == '1':
                    dp[i][j] = min(dp[i -1][j], dp[i][j -1], dp[i-1][j-1]) + 1
                    max_side = max(max_side , dp[i][j])

        return max_side * max_side

# DP Array Setup:
# 	•	We create a dp table with dimensions (m+1) \times (n+1) and initialize all values to 0. This extra row and column help us avoid boundary checking when referencing dp[i-1][j-1], dp[i-1][j], and dp[i][j-1].
# 	•	max_side will track the side length of the largest square found.
# 	2.	Filling the DP Table:
# 	•	We iterate over each cell in the original matrix. We use indices i and j in the dp table such that they correspond to the cell (i-1, j-1) in the original matrix.
# 	•	If the current cell matrix[i-1][j-1] is '1', it means a square can end at that cell. The side length of the square is determined by the minimum of:
# 	•	The largest square ending above: dp[i-1][j]
# 	•	The largest square ending to the left: dp[i][j-1]
# 	•	The largest square ending diagonally up-left: dp[i-1][j-1]
# 	•	We then add 1 to this minimum to form a new square ending at the current cell.
# 	•	We update max_side if the current square is larger.
# 	3.	Return the Area:
# 	•	Once the dp table is fully populated, the area of the largest square is simply max_side * max_side.
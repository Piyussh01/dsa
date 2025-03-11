class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or numRows >= len(s):
            return s 
        rows = [''] * numRows
        cur = 0
        going_down = False

        for char in s:
            rows[cur] += char
            if cur == 0 or cur == numRows -1:
                going_down = not going_down
            cur += 1 if going_down else -1

        return ''.join(rows)
        
#Time Complexity: O(n) where  n  is the length of  s .

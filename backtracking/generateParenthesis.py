class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        res = []
        def backtracking(s: str, l: int, r: int) -> None:
            if len(s) == 2 * n:
                res.append(s)
                return 
            if l < n:
                backtracking(s + '(', l + 1, r)
            if r < l:
                backtracking(s + ')', l , r + 1)
        
        backtracking('', 0 ,0)
        return res
#time complexity - O ( 4^n/ n^(1/2))
# space complexity - O(Cn . n )
            

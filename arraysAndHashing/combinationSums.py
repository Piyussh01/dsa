class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        res = []
        candidates.sort()
        
        def backtrack(start: int, target: int, comb: List[int]) -> None:
            if target == 0:
                res.append(list(comb))
                return
            
            for i in range(start, len(candidates)):
                if candidates[i] > target:
                    break
                comb.append(candidates[i])
                backtrack(i, target - candidates[i], comb)
                comb.pop()
        backtrack(0, target,[])
        return res



#O(2^(T/minVal))
        
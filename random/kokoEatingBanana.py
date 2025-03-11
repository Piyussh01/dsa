import math
from typing import List

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        # Helper function: return True if K is fast enough to finish all piles within h hours.
        def canfinish(K: int) -> bool:
            hours_needed = 0
            for p in piles:
                hours_needed += math.ceil(p / K)
            return hours_needed <= h
        
        l, r = 1, max(piles)
        while l < r:
            mid = (l + r) // 2
            if canfinish(mid):  # can finish with mid speed
                r = mid
            else:
                l = mid + 1
        return r

#run time - O(n * log(M))
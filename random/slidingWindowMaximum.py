from typing import List
from collections import deque

class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        
        #(O(n))

        # This deque will store indices of elements such that:
        # 1) The values of nums at those indices are in strictly decreasing order
        # 2) The front of the deque corresponds to the largest element in the current window
        dq = deque()
        
        result = []
        
        for i, val in enumerate(nums):
            # 1. Remove indices from the front if they are out of the current window
            #    The window's left boundary is i-k+1
            if dq and dq[0] < i - k + 1:
                dq.popleft()
            
            # 2. Remove elements from the back if they are smaller or equal to the current element
            #    Because they won't ever be needed (we want largest elements at front)
            while dq and nums[dq[-1]] <= val:
                dq.pop()
            
            # 3. Add the current index at the back
            dq.append(i)
            
            # 4. Once we've processed k elements, the front of the deque is the max in that window
            if i >= k - 1:
                result.append(nums[dq[0]])
        
        return result
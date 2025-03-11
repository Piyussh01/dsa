import heapq
from typing import List

class Solution:
    def maxSum(self, grid: List[List[int]], limits: List[int], k: int) -> int:
        # Special case: if k is 0 or less, return 0.
        if k <= 0:
            return 0
        
        heap = []
        heapq.heapify(heap)
        
        n = len(grid)
        for i in range(n):
            # Sort row i in descending order.
            row = sorted(grid[i], reverse=True)
            # Take up to limits[i] largest elements from this row.
            L = min(limits[i], len(row))
            
            # Add these elements to the min-heap, preserving only the top k overall.
            for x in row[:L]:
                if len(heap) < k:
                    heapq.heappush(heap, x)
                else:
                    if x > heap[0]:
                        heapq.heapreplace(heap, x)
        
        # The sum of the heap elements will be the maximum sum of up to k elements.
        return sum(heap)

#O(n*mlogm + Llogk)

#n is no of rows ;; m is no of colns 

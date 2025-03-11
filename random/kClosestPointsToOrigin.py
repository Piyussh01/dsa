import heapq
from typing import List

class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        # A max-heap of size k
        heap = []
        
        for x, y in points:
            # Compute the squared distance to avoid using sqrt
            dist = x*x + y*y
            # Push into the heap as (-dist, x, y) so the largest distance is at the top
            if len(heap) < k:
                heapq.heappush(heap, (-dist, x, y))
            else:
                # If this distance is smaller than the largest in the heap, replace it
                if dist < -heap[0][0]:
                    heapq.heapreplace(heap, (-dist, x, y))
        
        # Build the result from the heap
        return [(x, y) for (_, x, y) in heap]
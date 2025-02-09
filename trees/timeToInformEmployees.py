from collections import deque, defaultdict
from typing import List

class Solution:
    def numOfMinutes(self, n: int, headID: int, manager: List[int], informTime: List[int]) -> int:
        # Build the tree: mapping from manager to list of direct subordinates.
        tree = defaultdict(list)
        for emp in range(n):
            mgr = manager[emp]
            if mgr != -1:
                tree[mgr].append(emp)
        
        # Initialize the queue with the head and time 0.
        queue = deque([(headID, 0)])
        max_time = 0
        
        # Perform BFS
        while queue:
            current_employee, current_time = queue.popleft()
            max_time = max(max_time, current_time)
            
            # For every subordinate, add them to the queue with updated time.
            for subordinate in tree[current_employee]:
                queue.append((subordinate, current_time + informTime[current_employee]))
        
        return max_time
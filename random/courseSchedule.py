from typing import List

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # Build adjacency list
        graph = [[] for _ in range(numCourses)]
        for course, prereq in prerequisites:
            graph[prereq].append(course)
        
        # States: 0=unvisited, 1=visiting, 2=visited
        state = [0] * numCourses
        
        def dfs(node: int) -> bool:
            if state[node] == 1:
                # found a cycle
                return False
            if state[node] == 2:
                # already processed, no cycle found from this node
                return True
            
            state[node] = 1  # mark as visiting
            for neighbor in graph[node]:
                if not dfs(neighbor):
                    return False
            state[node] = 2  # mark as visited
            return True
        
        # Perform DFS on each course
        for course in range(numCourses):
            if state[course] == 0:
                if not dfs(course):
                    return False
        return True
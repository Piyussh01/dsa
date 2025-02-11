from collections import defaultdict, deque

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        #time complexity and space - O(V + E)
        graph = defaultdict(list)
        #building graph
        for course, prereq in prerequisites:
            graph[prereq].append(course)
        
        in_deg = [0] * numCourses
        for course, prereq in prerequisites:
            in_deg[course] += 1
        
        queue = deque()
        for i in range(numCourses):
            if in_deg[i] == 0:
                queue.append(i)
        
        result = []
        while queue:
            node = queue.popleft()
            result.append(node)
            for neighbor in graph[node]:
                in_deg[neighbor] -= 1
                if in_deg[neighbor] == 0:
                    queue.append(neighbor)
        #check for cycles
        if len(result) < numCourses:
            return []
        
        return result

        
# Walkthrough Example

# Let’s use Example 2:
# 	•	Input: numCourses = 4
# 	•	Prerequisites: [[1,0],[2,0],[3,1],[3,2]]

# Step 1: Build the Graph

# For each pair [course, prereq]:
# 	•	[1, 0]: Add an edge from 0 to 1
# → graph[0] = [1]
# 	•	[2, 0]: Add an edge from 0 to 2
# → graph[0] = [1, 2]
# 	•	[3, 1]: Add an edge from 1 to 3
# → graph[1] = [3]
# 	•	[3, 2]: Add an edge from 2 to 3
# → graph[2] = [3]

# Final graph:
# {
#   0: [1, 2],
#   1: [3],
#   2: [3]
# }
# tep 2: Calculate In-degrees

# Initialize in_deg = [0, 0, 0, 0] (for courses 0 to 3).

# For each pair:
# 	•	[1, 0]: in_deg[1] becomes 1 → [0, 1, 0, 0]
# 	•	[2, 0]: in_deg[2] becomes 1 → [0, 1, 1, 0]
# 	•	[3, 1]: in_deg[3] becomes 1 → [0, 1, 1, 1]
# 	•	[3, 2]: in_deg[3] becomes 2 → [0, 1, 1, 2]

# Step 3: Initialize the Queue

# Iterate over courses 0 to 3:
# 	•	Course 0: in_deg[0] = 0 → Add to queue.
# 	•	Courses 1, 2, 3 have in-degrees > 0, so ignore them.

# Initial queue: [0]

# Step 4: Process the Queue

# Iteration 1:
# 	•	Pop course 0 from the queue.
# 	•	Result: [0]
# 	•	Process neighbors of course 0 (from the graph, neighbors are [1, 2]):
# 	•	For course 1: Decrement in_deg[1] from 1 to 0 → Add course 1 to queue.
# 	•	For course 2: Decrement in_deg[2] from 1 to 0 → Add course 2 to queue.
# 	•	Queue now: [1, 2]

# Iteration 2:
# 	•	Pop course 1 from the queue.
# 	•	Result: [0, 1]
# 	•	Process neighbors of course 1 (neighbor is [3]):
# 	•	For course 3: Decrement in_deg[3] from 2 to 1 (not 0 yet, so do not add to queue).
# 	•	Queue now: [2]

# Iteration 3:
# 	•	Pop course 2 from the queue.
# 	•	Result: [0, 1, 2]
# 	•	Process neighbors of course 2 (neighbor is [3]):
# 	•	For course 3: Decrement in_deg[3] from 1 to 0 → Add course 3 to queue.
# 	•	Queue now: [3]

# Iteration 4:
# 	•	Pop course 3 from the queue.
# 	•	Result: [0, 1, 2, 3]
# 	•	Course 3 has no neighbors.
# 	•	Queue now: []

# Step 5: Final Check
# 	•	The result list has 4 courses, which equals numCourses.
# 	•	Therefore, the final valid course ordering is [0, 1, 2, 3] (note that [0, 2, 1, 3] would also be valid depending on the order in which nodes are processed).
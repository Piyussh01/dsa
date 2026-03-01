"""
GRAPH PATTERNS — Islands, Topo Sort, Shortest Path
====================================================

MENTAL MODEL:
  A graph is nodes + edges. Can be:
    - Adjacency list: {node: [neighbors]}  (most common in interviews)
    - Grid/matrix: grid[r][c]              (islands, maze problems)
    - Edge list: [(u, v, weight)]          (for Dijkstra, union-find)

  THREE BIG CATEGORIES:
    1. TRAVERSAL: visit all connected nodes (DFS/BFS) → islands, flood fill
    2. ORDERING: process nodes in dependency order → topological sort
    3. SHORTEST PATH: find minimum cost path → BFS (unweighted), Dijkstra (weighted)
"""

from collections import deque, defaultdict
import heapq


# ============================================================
# 1. NUMBER OF ISLANDS — Grid DFS
# ============================================================
def numIslands(grid):
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        grid[r][c] = '0'   # mark visited by sinking
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            dfs(r + dr, c + dc)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)

    return count


# ============================================================
# 2. CLONE GRAPH — DFS with hashmap to track copies
# ============================================================
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors else []

def cloneGraph(node):
    if not node:
        return None

    clones = {}  # original → clone

    def dfs(n):
        if n in clones:
            return clones[n]

        copy = Node(n.val)
        clones[n] = copy
        for neighbor in n.neighbors:
            copy.neighbors.append(dfs(neighbor))
        return copy

    return dfs(node)


# ============================================================
# 3. TOPOLOGICAL SORT — process dependencies in order
# ============================================================
# WHEN: "course prerequisites", "build order", "task scheduling"
#
# MENTAL MODEL:
#   Count incoming edges (indegree) for each node.
#   Start with nodes that have 0 incoming edges (no dependencies).
#   Process them, reduce indegree of neighbors. Repeat.

def canFinish(numCourses, prerequisites):
    # Build graph + indegree
    graph = defaultdict(list)
    indegree = [0] * numCourses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1

    # Start with courses that have no prerequisites
    queue = deque([i for i in range(numCourses) if indegree[i] == 0])
    completed = 0

    while queue:
        course = queue.popleft()
        completed += 1

        for next_course in graph[course]:
            indegree[next_course] -= 1
            if indegree[next_course] == 0:
                queue.append(next_course)

    return completed == numCourses  # if not, there's a cycle


# Full topological order (Course Schedule II)
def findOrder(numCourses, prerequisites):
    graph = defaultdict(list)
    indegree = [0] * numCourses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1

    queue = deque([i for i in range(numCourses) if indegree[i] == 0])
    order = []

    while queue:
        course = queue.popleft()
        order.append(course)
        for next_course in graph[course]:
            indegree[next_course] -= 1
            if indegree[next_course] == 0:
                queue.append(next_course)

    return order if len(order) == numCourses else []


# ============================================================
# 4. DIJKSTRA — shortest path in weighted graph
# ============================================================
# WHEN: "cheapest path", "minimum cost", weighted edges, no negative weights

def dijkstra(graph, start, n):
    # graph: {node: [(neighbor, weight)]}
    dist = [float('inf')] * n
    dist[start] = 0
    heap = [(0, start)]  # (distance, node)

    while heap:
        d, u = heapq.heappop(heap)

        if d > dist[u]:       # skip stale entries
            continue

        for v, w in graph[u]:
            new_dist = d + w
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))

    return dist

# Network Delay Time
def networkDelayTime(times, n, k):
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    dist = dijkstra(graph, k, n + 1)
    max_time = max(dist[1:])  # skip index 0
    return max_time if max_time < float('inf') else -1


# ============================================================
# 5. UNION-FIND — "are these connected?" queries
# ============================================================
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # already connected
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True


"""
GRAPH PATTERN RECOGNITION:

  "Number of islands / connected components"  → DFS/BFS on grid
  "Clone/copy a graph"                        → DFS + hashmap
  "Course schedule / build order"             → Topological sort (BFS + indegree)
  "Cheapest/shortest with weights"            → Dijkstra (heap)
  "Are X and Y connected?"                    → Union-Find
  "Shortest path, unweighted"                 → BFS

  Building the graph:
    Adjacency list is almost always the way to go:
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)   # add this line for undirected
"""

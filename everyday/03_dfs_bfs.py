"""
DFS & BFS — Two Ways to Walk a Graph/Tree
===========================================

MENTAL MODEL:
  BFS = explore level by level (QUEUE)  → shortest path, level-order
  DFS = go deep first, backtrack        → explore all paths, detect cycles

  BFS uses a QUEUE  (FIFO: first in, first out)  → from collections import deque
  DFS uses a STACK  (LIFO: last in, first out)    → just use a list, or recursion

  WHEN TO USE WHICH:
    BFS → "shortest path", "minimum steps", "level order", "nearest"
    DFS → "all paths", "does path exist", "connected components", "backtracking"
"""

from collections import deque


# ============================================================
# BFS TEMPLATE — Queue-based, level by level
# ============================================================
def bfs(graph, start):
    visited = set([start])
    queue = deque([start])

    while queue:
        node = queue.popleft()        # FIFO: take from front
        print(node)                    # process node

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)  # mark BEFORE enqueueing (prevents duplicates)
                queue.append(neighbor)


# BFS with LEVEL tracking (very common in tree problems)
def bfs_levels(root):
    if not root:
        return []
    queue = deque([root])
    result = []

    while queue:
        level_size = len(queue)        # how many nodes at this level
        level = []
        for _ in range(level_size):    # process exactly this level
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)

    return result
    # [[3], [9, 20], [15, 7]]  ← level order traversal


# ============================================================
# DFS TEMPLATE — Recursive (simplest)
# ============================================================
def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    print(node)                        # process node

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)


# DFS TEMPLATE — Iterative with explicit stack
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]                    # use list as stack

    while stack:
        node = stack.pop()            # LIFO: take from top
        if node in visited:
            continue
        visited.add(node)
        print(node)                    # process node

        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)


# ============================================================
# GRID DFS/BFS — for matrix problems (islands, flood fill, etc.)
# ============================================================

# DFS on grid (recursive) — Number of Islands pattern
def numIslands(grid):
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        # out of bounds or water → stop
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        grid[r][c] = '0'             # mark visited (sink the island)
        dfs(r + 1, c)                # down
        dfs(r - 1, c)                # up
        dfs(r, c + 1)                # right
        dfs(r, c - 1)                # left

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)            # sink entire island

    return count


# BFS on grid — shortest path in unweighted grid
def shortestPath(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start[0], start[1], 0)])  # (row, col, distance)
    visited = set()
    visited.add((start[0], start[1]))

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        r, c, dist = queue.popleft()

        if (r, c) == (end[0], end[1]):
            return dist

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] != 1:
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))

    return -1  # no path


"""
QUICK REFERENCE:

  BFS (Queue - deque):
    queue = deque([start])
    while queue:
        node = queue.popleft()     ← FIFO
        for neighbor: queue.append()

  DFS (Stack - list):
    stack = [start]
    while stack:
        node = stack.pop()         ← LIFO
        for neighbor: stack.append()

  DFS (Recursive):
    def dfs(node):
        visit(node)
        for neighbor: dfs(neighbor)

  Grid directions: [(0,1),(0,-1),(1,0),(-1,0)]

  KEY DIFFERENCES:
    BFS guarantees shortest path in unweighted graphs
    DFS uses less memory (no queue of entire level)
    DFS is simpler to write recursively
    BFS is better for "nearest" / "minimum" problems
"""

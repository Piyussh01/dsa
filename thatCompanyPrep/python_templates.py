# Python Templates for Interview
# Memorize these - they cover 80% of problems

# ==========================================
# GRAPH TEMPLATES
# ==========================================

# 1. DFS (Recursive) - for traversal, cycle detection, connected components
# USE WHEN: Need to explore all reachable nodes, detect cycles, count components
# TIME: O(V + E), SPACE: O(V) for visited set + O(V) recursion stack
def dfs(graph, node, visited):
    # BASE CASE: Already visited this node, stop to avoid infinite loop
    if node in visited:
        return

    # MARK: Add current node to visited set
    visited.add(node)

    # RECURSE: Explore all unvisited neighbors
    for neighbor in graph[node]:
        dfs(graph, neighbor, visited)

    # NOTE: Can add post-processing logic here (runs AFTER exploring all descendants)
    # Useful for topological sort DFS variant

# 2. BFS - for shortest path (unweighted), level-order
# USE WHEN: Need shortest path in unweighted graph, level-by-level traversal
# TIME: O(V + E), SPACE: O(V) for queue and visited set
# KEY: BFS guarantees shortest path in UNWEIGHTED graphs (first visit = shortest)
from collections import deque

def bfs(graph, start):
    # INITIALIZE: Queue with starting node, mark as visited
    queue = deque([start])
    visited = {start}
    distance = 0  # Track level/distance from start

    while queue:
        # LEVEL-ORDER: Process all nodes at current level before moving to next
        # len(queue) gives number of nodes at current level
        for _ in range(len(queue)):
            node = queue.popleft()  # O(1) from left side of deque

            # EXPLORE: Add all unvisited neighbors to queue
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)  # Mark before adding to prevent duplicates
                    queue.append(neighbor)

        distance += 1  # Increment after processing entire level

    return distance  # Returns number of levels (or max distance from start)

# 3. Dijkstra - shortest path (weighted, no negative edges)
# USE WHEN: Need shortest path in WEIGHTED graph with NON-NEGATIVE edges
# TIME: O((V + E) log V) with heap, SPACE: O(V) for dist dict and heap
# KEY: Greedy approach - always process closest unvisited node first
# CANNOT handle negative edges (use Bellman-Ford instead)
import heapq

def dijkstra(graph, start):
    # INITIALIZE: Distance dict (start = 0, others = infinity)
    # Min-heap to always process closest node first
    dist = {start: 0}
    heap = [(0, start)]  # (distance, node) - heap sorts by first element

    while heap:
        # POP: Get node with minimum distance (greedy choice)
        d, node = heapq.heappop(heap)

        # SKIP: If we already found a better path to this node, skip it
        # This handles duplicate entries in heap (we don't decrease-key)
        if d > dist.get(node, float('inf')):
            continue

        # RELAX: Try to improve distances to neighbors
        for neighbor, weight in graph[node]:  # graph[node] = [(neighbor, weight), ...]
            new_dist = d + weight

            # UPDATE: If found shorter path, update and add to heap
            if new_dist < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return dist  # Returns {node: shortest_distance_from_start}

# 4. Topological Sort (Kahn's Algorithm) - for dependency ordering, cycle detection
# USE WHEN: Need to order tasks with dependencies (DAG), detect cycles in directed graph
# TIME: O(V + E), SPACE: O(V + E)
# KEY: Process nodes with no dependencies first, remove edges, repeat
# Works ONLY on DAG (Directed Acyclic Graph)
def topological_sort(n, edges):
    # BUILD GRAPH: Adjacency list and track indegree (# of incoming edges)
    graph = {i: [] for i in range(n)}
    indegree = [0] * n  # indegree[i] = # of prerequisites for node i

    for u, v in edges:  # Edge u -> v means "u must come before v"
        graph[u].append(v)
        indegree[v] += 1  # v has one more prerequisite

    # START: All nodes with no prerequisites (indegree = 0)
    queue = deque([i for i in range(n) if indegree[i] == 0])
    order = []  # Result: valid ordering of nodes

    while queue:
        # PROCESS: Take a node with no remaining prerequisites
        node = queue.popleft()
        order.append(node)

        # REMOVE EDGES: "Complete" this node, reduce indegree of dependents
        for neighbor in graph[node]:
            indegree[neighbor] -= 1

            # If neighbor now has no prerequisites, it's ready to process
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    # VALIDATE: If we processed all nodes, no cycle exists
    # If len(order) < n, some nodes couldn't be reached (cycle exists)
    return order if len(order) == n else []  # Empty list = cycle detected

# 5. Union-Find (Disjoint Set Union) - for connected components, cycle detection
# USE WHEN: Need to track connected components, detect cycles in UNDIRECTED graphs
# TIME: O(α(n)) ≈ O(1) per operation with path compression + union by rank
# SPACE: O(n) for parent and rank arrays
# KEY: Efficiently merge sets and check if two elements are in same set
class UnionFind:
    def __init__(self, n):
        # Initially, each node is its own parent (n disjoint sets)
        self.parent = list(range(n))  # parent[i] = i means i is a root
        self.rank = [0] * n  # Rank ≈ tree height, used for union optimization

    def find(self, x):
        """Find the root of x's set (with path compression)"""
        # PATH COMPRESSION: Make all nodes on path point directly to root
        # This flattens the tree, making future finds faster
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Recursively find root
        return self.parent[x]

    def union(self, x, y):
        """Merge sets containing x and y. Returns False if already connected."""
        # Find roots of both sets
        px, py = self.find(x), self.find(y)

        # SAME SET: Already connected (adding edge would create cycle)
        if px == py:
            return False  # Useful for cycle detection

        # UNION BY RANK: Attach smaller tree under root of larger tree
        # This keeps trees balanced, preventing tall trees
        if self.rank[px] < self.rank[py]:
            px, py = py, px  # Swap to ensure px has higher rank

        self.parent[py] = px  # Make px the new root

        # If ranks were equal, increase rank of new root
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

        return True  # Successfully merged two different sets

# ==========================================
# SLIDING WINDOW TEMPLATES
# ==========================================

# Variable-size window (find longest valid window)
# USE WHEN: Find longest substring/subarray satisfying a condition
# Examples: longest substring without repeating chars, max consecutive 1s after k flips
# TIME: O(n), SPACE: O(k) where k = size of state (alphabet size, unique elements)
# KEY: Expand right, shrink left when invalid, track max size
def sliding_window_longest(arr):
    left = 0  # Left boundary of window
    result = 0  # Track maximum valid window size
    state = {}  # Track window state (Counter for frequencies, set for unique, etc.)

    # EXPAND: Always move right pointer forward
    for right in range(len(arr)):
        # ADD: Include arr[right] in window
        # Example: state[arr[right]] = state.get(arr[right], 0) + 1

        # SHRINK: While window is invalid, remove from left
        # Example invalid: len(state) > k (too many unique chars)
        while not is_valid(state):
            # REMOVE: Exclude arr[left] from window state
            # Example: state[arr[left]] -= 1
            left += 1

        # UPDATE: Current window is valid, check if it's the longest
        result = max(result, right - left + 1)

    return result

# Variable-size window (find shortest valid window)
# USE WHEN: Find shortest/minimum substring/subarray satisfying a condition
# Examples: min subarray sum >= target, min window containing all chars
# TIME: O(n), SPACE: O(1) or O(k) for state
# KEY: Expand until valid, then shrink while valid, track minimum
def sliding_window_shortest(arr, target):
    left = 0  # Left boundary
    result = float('inf')  # Track minimum valid window size
    current_sum = 0  # Example state: sum of window

    # EXPAND: Move right pointer forward
    for right in range(len(arr)):
        current_sum += arr[right]  # Add right element to window

        # SHRINK: While window is VALID, try to minimize by removing from left
        # This is opposite of longest: shrink when valid (not when invalid)
        while current_sum >= target:  # While valid condition holds
            # UPDATE: Before shrinking, record this valid window size
            result = min(result, right - left + 1)

            # REMOVE: Shrink from left
            current_sum -= arr[left]
            left += 1

    # RETURN: inf means no valid window found
    return result if result != float('inf') else 0

# ==========================================
# BINARY SEARCH TEMPLATES
# ==========================================

# Find minimum value satisfying condition
# USE WHEN: Find smallest value where condition becomes true (e.g., Koko bananas)
# Example: Find minimum speed to eat all bananas within h hours
# TIME: O(log(hi - lo) * condition_cost), SPACE: O(1)
# KEY: Answer space is monotonic (if condition(x) true, condition(x+1) also true)
def binary_search_min(lo, hi, condition):
    # INVARIANT: answer is in range [lo, hi]
    while lo < hi:
        mid = (lo + hi) // 2  # No +1 here (we want to round down)

        if condition(mid):  # mid works, but maybe we can go lower
            hi = mid  # Keep mid as potential answer, search left half
        else:  # mid doesn't work, need higher value
            lo = mid + 1  # mid cannot be answer, search right half

    return lo  # lo == hi, found minimum

# Find maximum value satisfying condition
# USE WHEN: Find largest value where condition is true (e.g., max capacity)
# Example: Find maximum weight capacity that allows shipping within d days
# TIME: O(log(hi - lo) * condition_cost), SPACE: O(1)
# KEY: Answer space is monotonic (if condition(x) true, condition(x-1) also true)
def binary_search_max(lo, hi, condition):
    # INVARIANT: answer is in range [lo, hi]
    while lo < hi:
        mid = (lo + hi + 1) // 2  # +1 to avoid infinite loop (round up)
        # Without +1: if lo=5, hi=6, mid=5, and condition(5)=true, lo=mid=5 → infinite loop

        if condition(mid):  # mid works, but maybe we can go higher
            lo = mid  # Keep mid as potential answer, search right half
        else:  # mid doesn't work, need lower value
            hi = mid - 1  # mid cannot be answer, search left half

    return lo  # lo == hi, found maximum

# Bisect left (find insertion point, leftmost occurrence)
# USE WHEN: Find leftmost position to insert target in sorted array
# Also finds first occurrence of target, or position of first element >= target
# TIME: O(log n), SPACE: O(1)
# RETURNS: Index where target should be inserted (or index of first occurrence)
def bisect_left(arr, target):
    lo, hi = 0, len(arr)  # Search range [0, n]

    while lo < hi:
        mid = (lo + hi) // 2

        if arr[mid] < target:  # mid too small, search right
            lo = mid + 1
        else:  # arr[mid] >= target, could be answer or search left
            hi = mid  # Keep mid as potential position

    # RESULT: lo is leftmost position where arr[lo] >= target
    return lo

# ==========================================
# DYNAMIC PROGRAMMING TEMPLATES
# ==========================================

# 1D DP (e.g., climbing stairs, house robber)
# USE WHEN: Problem has optimal substructure and overlapping subproblems in 1D
# Examples: climbing stairs, house robber, coin change, decode ways
# TIME: O(n), SPACE: O(n) or O(1) with space optimization
# KEY: dp[i] = optimal solution for first i elements
def dp_1d(n):
    # INITIALIZE: Create array to store solutions to subproblems
    dp = [0] * (n + 1)  # dp[i] = answer for input size i
    dp[0] = base_case  # Base case: smallest subproblem

    # BUILD UP: Solve larger problems using smaller ones
    for i in range(1, n + 1):
        # RECURRENCE: dp[i] depends on previous values
        # Example (House Robber): dp[i] = max(dp[i-1], dp[i-2] + nums[i])
        # Example (Climbing Stairs): dp[i] = dp[i-1] + dp[i-2]
        dp[i] = recurrence(dp, i)

    return dp[n]  # Final answer

    # SPACE OPTIMIZATION: If only need dp[i-1], dp[i-2], use 2 variables instead

# 2D DP (e.g., LCS, grid paths, edit distance)
# USE WHEN: Two sequences/strings, or grid problems
# Examples: longest common subsequence, edit distance, unique paths
# TIME: O(m * n), SPACE: O(m * n) or O(n) with space optimization
# KEY: dp[i][j] = optimal solution for first i elements of s1 and first j of s2
def dp_2d(s1, s2):
    m, n = len(s1), len(s2)

    # INITIALIZE: 2D table, (m+1) x (n+1) to handle empty string case
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    # dp[i][j] = LCS length for s1[0:i] and s2[0:j]

    # BUILD UP: Fill table row by row
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # MATCH: If characters match, extend previous LCS
            if s1[i-1] == s2[j-1]:  # i-1 because dp is 1-indexed, strings are 0-indexed
                dp[i][j] = dp[i-1][j-1] + 1

            # NO MATCH: Take best of excluding one character
            else:
                # Either skip s1[i-1] or skip s2[j-1]
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]  # LCS length for entire strings

    # SPACE OPTIMIZATION: Only need previous row, can use two 1D arrays

# ==========================================
# BACKTRACKING TEMPLATE
# ==========================================

# BACKTRACKING - for generating all possibilities (permutations, combinations, subsets)
# USE WHEN: Need to explore all possible solutions, not just one optimal
# Examples: permutations, N-Queens, sudoku, generate parentheses
# TIME: Exponential (often O(n! ) or O(2^n)), SPACE: O(n) recursion depth
# KEY: Build solution incrementally, backtrack (undo) when path is invalid/complete
def backtrack(path, choices, result):
    """Generic backtracking template"""
    # BASE CASE: Found complete solution
    if is_solution(path):
        result.append(path[:])  # CRITICAL: Use path[:] to create copy!
        return  # Stop exploring this path

    # EXPLORE: Try each possible choice
    for i, choice in enumerate(choices):
        # PRUNE: Skip invalid choices (optimization)
        if is_valid(choice, path):
            # MAKE CHOICE: Add to current path
            path.append(choice)

            # RECURSE: Explore with this choice
            backtrack(path, get_next_choices(choices, i), result)

            # UNDO: Remove choice (backtrack) to try other options
            path.pop()  # This is the "backtrack" step!

# Example: Subsets - Generate all possible subsets of nums
# Pattern: Include or exclude each element
def subsets(nums):
    result = []  # Store all subsets

    def backtrack(start, path):
        # KEY INSIGHT: Every path is a valid subset (even empty)
        result.append(path[:])  # Add current subset (make copy!)

        # TRY: Add each remaining element to current subset
        for i in range(start, len(nums)):
            path.append(nums[i])  # Include nums[i]
            backtrack(i + 1, path)  # Recurse with remaining elements
            path.pop()  # Backtrack: exclude nums[i], try next

    backtrack(0, [])  # Start with empty subset
    return result

# VARIATIONS:
# - Permutations: Use visited set, don't skip used elements
# - Combinations: Similar to subsets, but stop when path.length == k
# - N-Queens: Check if placement is valid before recursing

# ==========================================
# HEAP TEMPLATES
# ==========================================

# HEAP TEMPLATES - Priority queue for K largest/smallest, streaming data
# Python uses MIN heap by default (smallest element at top)
# For MAX heap: negate values or use negative priority

# K largest elements
# USE WHEN: Need top K elements from large dataset
# TIME: O(n log k) using min heap, SPACE: O(k)
# KEY: Maintain min heap of size k, smallest in heap is k-th largest
def k_largest(nums, k):
    # BUILT-IN: Python provides optimized implementation
    return heapq.nlargest(k, nums)

    # MANUAL APPROACH (to understand the pattern):
    # heap = []
    # for num in nums:
    #     heapq.heappush(heap, num)
    #     if len(heap) > k:
    #         heapq.heappop(heap)  # Remove smallest
    # return heap

# K smallest elements
# USE WHEN: Need smallest K elements
# TIME: O(n log k) using max heap, SPACE: O(k)
# KEY: Maintain max heap of size k, largest in heap is k-th smallest
def k_smallest(nums, k):
    # BUILT-IN: Python provides optimized implementation
    return heapq.nsmallest(k, nums)

    # MANUAL APPROACH with max heap (negate values):
    # heap = []
    # for num in nums:
    #     heapq.heappush(heap, -num)  # Negate for max heap
    #     if len(heap) > k:
    #         heapq.heappop(heap)
    # return [-x for x in heap]

# Merge K sorted lists (classic heap problem)
# USE WHEN: Merge multiple sorted sequences efficiently
# TIME: O(N log k) where N = total nodes, k = number of lists, SPACE: O(k) for heap
# KEY: Keep one element from each list in heap, always pop smallest
def merge_k_sorted(lists):
    # INITIALIZE: Add first element from each list to heap
    heap = []
    for i, lst in enumerate(lists):
        if lst:  # Only add non-empty lists
            # Heap entry: (value, list_index, node)
            # list_index breaks ties (not strictly needed but good practice)
            heapq.heappush(heap, (lst[0].val, i, lst[0]))

    # SETUP: Dummy head for result linked list
    dummy = ListNode(0)
    curr = dummy

    # PROCESS: Always take smallest element from heap
    while heap:
        val, i, node = heapq.heappop(heap)  # Get smallest

        # ADD: Append to result
        curr.next = node
        curr = curr.next

        # REFILL: Add next element from same list to heap
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next  # Return merged list (skip dummy)

# ==========================================
# PREFIX SUM TEMPLATE
# ==========================================

# PREFIX SUM - for range sum queries, subarray sum problems
# USE WHEN: Need frequent sum queries on subarrays, or find subarrays with target sum
# Examples: subarray sum equals k, continuous subarray sum, product of array except self
# TIME: O(n), SPACE: O(n) for hashmap
# KEY: prefix_sum[i] = sum of nums[0:i], so sum(nums[i:j]) = prefix[j] - prefix[i]

# Subarray sum equals K
# PROBLEM: Count subarrays with sum equal to k
# INSIGHT: If prefix_sum[j] - prefix_sum[i] = k, then sum(nums[i:j]) = k
#          Rearranging: prefix_sum[i] = prefix_sum[j] - k
def subarray_sum(nums, k):
    count = 0  # Number of subarrays with sum = k
    prefix_sum = 0  # Running sum from start
    prefix_count = {0: 1}  # Map: prefix_sum -> count of occurrences
    # BASE CASE: {0: 1} handles subarrays starting from index 0

    for num in nums:
        # UPDATE: Add current number to running sum
        prefix_sum += num

        # LOOKUP: Check if (prefix_sum - k) exists
        # If yes, there are prefix_count[prefix_sum - k] subarrays ending here with sum k
        # MATH: prefix_sum - (prefix_sum - k) = k
        count += prefix_count.get(prefix_sum - k, 0)

        # STORE: Record this prefix sum for future lookups
        prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1

    return count

# EXAMPLE WALKTHROUGH: nums = [1, 2, 3], k = 3
# i=0: num=1, prefix=1, lookup 1-3=-2 (not found), store {0:1, 1:1}, count=0
# i=1: num=2, prefix=3, lookup 3-3=0 (found! count+=1), store {0:1, 1:1, 3:1}, count=1
# i=2: num=3, prefix=6, lookup 6-3=3 (found! count+=1), store {..., 6:1}, count=2
# Answer: 2 subarrays → [1,2] and [3]

# ==========================================
# TREE TEMPLATES
# ==========================================

# TREE TRAVERSALS - DFS and BFS patterns

# Inorder Traversal (Left -> Root -> Right)
# USE WHEN: Need sorted order for BST, or process nodes in sorted sequence
# TIME: O(n), SPACE: O(h) for recursion where h = height
# OUTPUT: For BST, gives sorted array
def inorder(root):
    if not root:
        return []
    # PATTERN: Left -> Root -> Right
    return inorder(root.left) + [root.val] + inorder(root.right)

    # ITERATIVE (using stack):
    # result, stack = [], []
    # curr = root
    # while curr or stack:
    #     while curr:
    #         stack.append(curr)
    #         curr = curr.left
    #     curr = stack.pop()
    #     result.append(curr.val)
    #     curr = curr.right

# Preorder Traversal (Root -> Left -> Right)
# USE WHEN: Copy tree, serialize tree, or need parent before children
# TIME: O(n), SPACE: O(h)
def preorder(root):
    if not root:
        return []
    # PATTERN: Root -> Left -> Right (process node before recursing)
    return [root.val] + preorder(root.left) + preorder(root.right)

# BFS Level Order Traversal
# USE WHEN: Process tree level by level, find shortest path, check completeness
# TIME: O(n), SPACE: O(w) where w = max width of tree
# OUTPUT: [[level0 nodes], [level1 nodes], ...]
def level_order(root):
    if not root:
        return []

    result = []  # Store each level's nodes
    queue = deque([root])  # BFS queue

    while queue:
        level = []  # Current level's values

        # PROCESS ENTIRE LEVEL: Use len(queue) to know level size
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)

            # ADD NEXT LEVEL: Children go to queue
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)  # Completed one level

    return result

# Lowest Common Ancestor (LCA) of Binary Tree
# USE WHEN: Find LCA of two nodes in binary tree
# TIME: O(n), SPACE: O(h) for recursion
# KEY: If p and q are in different subtrees, root is LCA
def lca(root, p, q):
    # BASE CASES:
    # 1. Reached null: no LCA in this subtree
    # 2. Found p or q: this node could be LCA (or ancestor of the other)
    if not root or root == p or root == q:
        return root

    # RECURSE: Search in both subtrees
    left = lca(root.left, p, q)   # p or q in left subtree?
    right = lca(root.right, p, q)  # p or q in right subtree?

    # ANALYZE RESULTS:
    # If both left and right found something, p and q are in different subtrees
    if left and right:
        return root  # Current root is LCA!

    # Otherwise, return whichever side found something (or None)
    return left or right  # LCA is in one subtree, or not found

# ==========================================
# QUICK PYTHON TRICKS
# ==========================================

# ==========================================
# GRAPH BUILDING HELPERS
# ==========================================

# Build adjacency list from edge list
# INPUT: edges = [(u, v), ...], directed = True/False
# OUTPUT: {node: [neighbors]}
# TIME: O(E), SPACE: O(V + E)
def build_graph(edges, directed=False):
    from collections import defaultdict
    graph = defaultdict(list)  # Auto-creates empty list for new nodes

    for u, v in edges:
        graph[u].append(v)  # Add edge u -> v

        # For UNDIRECTED graph, add reverse edge
        if not directed:
            graph[v].append(u)  # Add edge v -> u

    return graph

# Build weighted adjacency list
# INPUT: edges = [(u, v, weight), ...]
# OUTPUT: {node: [(neighbor, weight), ...]}
# USE FOR: Dijkstra, Bellman-Ford, MST algorithms
# TIME: O(E), SPACE: O(V + E)
def build_weighted_graph(edges):
    from collections import defaultdict
    graph = defaultdict(list)

    for u, v, w in edges:
        graph[u].append((v, w))  # Store neighbor AND weight

    return graph

# ==========================================
# GRID TRAVERSAL HELPERS
# ==========================================

# 8 directions for grid (including diagonals)
# USE FOR: Chess king moves, word search with diagonals
# ORDER: Top-left, Top, Top-right, Left, Right, Bottom-left, Bottom, Bottom-right
DIRECTIONS_8 = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

# 4 directions for grid (up, down, left, right)
# USE FOR: Most grid problems (islands, word search, flood fill)
# ORDER: Right, Left, Down, Up (or any consistent order)
DIRECTIONS_4 = [(0,1), (0,-1), (1,0), (-1,0)]

# Alternative naming: UP, DOWN, LEFT, RIGHT
# DIRECTIONS_4 = [(-1,0), (1,0), (0,-1), (0,1)]

# Check if grid position is valid
# USE BEFORE: Accessing grid[r][c] to avoid index errors
# RETURNS: True if (r, c) is within grid bounds
def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

# USAGE EXAMPLE:
# for dr, dc in DIRECTIONS_4:
#     nr, nc = r + dr, c + dc
#     if in_bounds(nr, nc, m, n) and grid[nr][nc] == '1':
#         dfs(grid, nr, nc)

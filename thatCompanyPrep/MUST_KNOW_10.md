# 10 Must-Know Problems for Accord Interview
## These should be MUSCLE MEMORY by tomorrow

---

## Why These 10?

These cover the most common interview patterns at YC-backed SaaS companies:
- ✅ Demonstrate fundamental DS&A knowledge
- ✅ Show up in 70% of coding interviews
- ✅ Each unlocks an entire pattern category
- ✅ Can be solved in 15-20 minutes

**Your goal:** Code each without looking at notes, explain approach clearly, no bugs.

---

## The 10 Problems (In Priority Order)

### 1. Two Sum
**Pattern:** Hashmap for O(1) lookup
**Why Critical:** Tests if you understand space-time tradeoffs
**LeetCode:** #1 (Easy)

**Problem:** Given array of integers, return indices of two numbers that add up to target.

**Template to Memorize:**
```python
def two_sum(nums, target):
    seen = {}  # {value: index}

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i

    return []
```

**Key Points:**
- Time: O(n), Space: O(n)
- Store as you go, not after
- Return immediately when found

---

### 2. Valid Parentheses
**Pattern:** Stack for matching pairs
**Why Critical:** Foundation for all stack problems
**LeetCode:** #20 (Easy)

**Problem:** Given string of brackets `()[]{}`, determine if valid (every open has matching close in correct order).

**Template to Memorize:**
```python
def is_valid(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}

    for char in s:
        if char in pairs:  # Closing bracket
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
        else:  # Opening bracket
            stack.append(char)

    return len(stack) == 0
```

**Key Points:**
- Closing bracket → check stack top matches
- Opening bracket → push to stack
- End: stack must be empty

---

### 3. Longest Substring Without Repeating Characters
**Pattern:** Sliding window with set/hashmap
**Why Critical:** Unlocks all sliding window problems
**LeetCode:** #3 (Medium)

**Problem:** Find length of longest substring without repeating characters in string s.

**Template to Memorize:**
```python
def length_of_longest_substring(s):
    left = 0
    seen = set()
    max_len = 0

    for right in range(len(s)):
        # Shrink window while duplicate exists
        while s[right] in seen:
            seen.remove(s[left])
            left += 1

        # Add current char and update max
        seen.add(s[right])
        max_len = max(max_len, right - left + 1)

    return max_len
```

**Key Points:**
- Expand right, shrink left when invalid
- Set tracks characters in current window
- Update result after window is valid

---

### 4. Maximum Subarray (Kadane's Algorithm)
**Pattern:** DP / Greedy for optimal subarray
**Why Critical:** Foundation for array optimization problems
**LeetCode:** #53 (Medium)

**Problem:** Find contiguous subarray with largest sum in array nums.

**Template to Memorize:**
```python
def max_subarray(nums):
    current_sum = 0
    max_sum = float('-inf')

    for num in nums:
        current_sum = max(num, current_sum + num)  # Start fresh or continue
        max_sum = max(max_sum, current_sum)

    return max_sum  
```

**Key Points:**
- At each element: start new subarray or extend current
- Track both current_sum and global max_sum
- Handles all negatives correctly

**Intuition:** If adding current element makes sum worse than starting fresh, start fresh.

---

### 5. Number of Islands
**Pattern:** DFS/BFS on grid
**Why Critical:** Foundation for all grid traversal problems
**LeetCode:** #200 (Medium)

**Problem:** Count number of islands ('1's) in 2D grid, surrounded by water ('0's).

**Template to Memorize:**
```python
def num_islands(grid):
    if not grid:
        return 0

    m, n = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        # Base cases: out of bounds or water
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] == '0':
            return

        # Mark as visited by changing to '0'
        grid[r][c] = '0'

        # Explore 4 directions
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)

    # Check every cell
    for r in range(m):
        for c in range(n):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)  # Sink entire island

    return count
```

**Key Points:**
- Modify grid in-place to mark visited (or use visited set)
- Each DFS call sinks entire connected island
- Count increments once per island, not per cell

---

### 6. Course Schedule
**Pattern:** Topological sort / Cycle detection in directed graph
**Why Critical:** Tests graph fundamentals and dependency handling
**LeetCode:** #207 (Medium)

**Problem:** Given numCourses and prerequisites, return if you can finish all courses (no circular dependencies).

**Template to Memorize:**
```python
def can_finish(numCourses, prerequisites):
    from collections import defaultdict, deque

    # Build graph and indegree
    graph = defaultdict(list)
    indegree = [0] * numCourses

    for course, prereq in prerequisites:
        graph[prereq].append(course)  # prereq -> course
        indegree[course] += 1

    # Start with courses that have no prerequisites
    queue = deque()
    for i in range(numCourses):
        if in_deg[i] == 0:
            queue.append(i)
    result = []

    while queue:
        course = queue.popleft()
        result.append(course)

        # "Complete" this course, reduce indegree of dependents
        for next_course in graph[course]:
            indegree[next_course] -= 1
            if indegree[next_course] == 0:
                queue.append(next_course)
    
     #check for cycles
    if len(result) < numCourses:
        return []
    # If completed all courses, no cycle exists
    return result
```

**Key Points:**
- Topological sort works only on DAG (no cycles)
- If can't complete all courses → cycle exists
- Kahn's algorithm: process nodes with indegree 0

---

### 7. Binary Tree Level Order Traversal
**Pattern:** BFS on tree
**Why Critical:** Foundation for all tree BFS problems
**LeetCode:** #102 (Medium)

**Problem:** Return level-order traversal of binary tree (list of lists, one per level).

**Template to Memorize:**
```python
def level_order(root):
    if not root:
        return []

    from collections import deque
    result = []
    queue = deque([root])

    while queue:
        level = []

        # Process entire current level
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)

            # Add next level's nodes
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result
```

**Key Points:**
- `len(queue)` at start of loop = current level size
- Process all nodes at current level before moving to next
- Each iteration adds one level to result

---

### 8. Merge Intervals
**Pattern:** Sorting + greedy merging
**Why Critical:** Common in scheduling/time-based problems (relevant for SaaS!)
**LeetCode:** #56 (Medium)

**Problem:** Given array of intervals, merge all overlapping intervals.

**Template to Memorize:**
```python
def merge(intervals):
    if not intervals:
        return []

    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    result = [intervals[0]]

    for current in intervals[1:]:
        last = result[-1]

        # Overlapping: merge by extending end time
        if current[0] <= last[1]:
            last[1] = max(last[1], current[1])
        else:  # Non-overlapping: add new interval
            result.append(current)

    return result
```

**Key Points:**
- Sort first (O(n log n))
- Compare current interval with last in result
- Overlap if `current.start <= last.end`
- Merge by extending end time to max

---

### 9. Subarray Sum Equals K
**Pattern:** Prefix sum + hashmap
**Why Critical:** Tests hashmap mastery and cumulative sum technique
**LeetCode:** #560 (Medium)

**Problem:** Count number of continuous subarrays whose sum equals k.

**Template to Memorize:**
```python
def subarray_sum(nums, k):
    count = 0
    prefix_sum = 0
    prefix_count = {0: 1}  # Handle subarrays starting from index 0

    for num in nums:
        prefix_sum += num

        # Check if (prefix_sum - k) exists
        # If yes, found subarray(s) ending at current index
        count += prefix_count.get(prefix_sum - k, 0)

        # Store current prefix sum
        prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1

    return count
```

**Key Points:**
- `prefix_sum[j] - prefix_sum[i] = k` → subarray from i+1 to j has sum k
- Initialize with `{0: 1}` for subarrays starting at index 0
- Look up `prefix_sum - k`, not k itself

**Math:** If current prefix = 10 and we've seen prefix = 7 before, then subarray between them has sum 3.

---

### 10. LRU Cache
**Pattern:** HashMap + Doubly Linked List
**Why Critical:** Classic design problem, tests DS fundamentals
**LeetCode:** #146 (Medium)

**Problem:** Implement LRU cache with O(1) get and put operations.

**Template to Memorize:**
```python
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # {key: Node}

        # Dummy head and tail for easier insertion/removal
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Remove node from linked list"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node):
        """Add node right after head (most recently used)"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._remove(node)
        self._add_to_head(node)  # Move to front (mark as recently used)
        return node.val

    def put(self, key, value):
        if key in self.cache:
            # Update existing: remove and re-add
            self._remove(self.cache[key])

        # Add new node
        node = Node(key, value)
        self.cache[key] = node
        self._add_to_head(node)

        # Evict LRU if over capacity
        if len(self.cache) > self.capacity:
            lru = self.tail.prev  # Node before tail is LRU
            self._remove(lru)
            del self.cache[lru.key]
```

**Key Points:**
- HashMap for O(1) lookup
- Doubly linked list for O(1) insertion/removal
- Most recent = head, Least recent = tail
- Dummy nodes simplify edge cases
- On access: move to head (mark as recent)

---

## Practice Schedule (1 Day)

### Morning (4 hours): Problems 1-5
- 9:00-9:30: Two Sum (15 min code + 15 min explain out loud)
- 9:30-10:00: Valid Parentheses
- 10:00-10:30: Break
- 10:30-11:15: Longest Substring Without Repeating
- 11:15-12:00: Maximum Subarray
- 12:00-1:00: Number of Islands

### Afternoon (4 hours): Problems 6-10
- 1:00-1:45: Course Schedule
- 1:45-2:30: Binary Tree Level Order
- 2:30-3:00: Break + review morning problems
- 3:00-3:45: Merge Intervals
- 3:45-4:30: Subarray Sum Equals K
- 4:30-5:30: LRU Cache

### Evening (2 hours): Final Drill
- 5:30-6:00: Pick 3 random problems, code without looking
- 6:00-6:30: System design review (from your system_design_reference.md)
- 6:30-7:00: Mental review - visualize solving each problem

---

## How to Use This List

### For Each Problem:

1. **READ** (2 min): Understand problem, clarify edge cases
2. **APPROACH** (3 min): Explain strategy out loud before coding
3. **CODE** (10-15 min): Write solution without looking at template
4. **TEST** (3 min): Trace through with example, check edge cases
5. **EXPLAIN** (5 min): Walk through your code out loud as if in interview

### Red Flags to Avoid:
- ❌ Jumping straight to code without explaining approach
- ❌ Silent coding (always narrate your thoughts)
- ❌ Not handling edge cases (empty input, single element, negatives)
- ❌ Forgetting to state time/space complexity

### Communication Template:
```
"Let me make sure I understand: [restate problem].

My approach is [high-level strategy]. This will be O(n) time
and O(n) space because [reason].

Let me walk through an example first: [trace example].

Now I'll code this up [start coding while narrating]."
```

---

## Pattern Recognition Cheat Sheet

When you see these keywords, think:

| Keyword | Pattern | Problem from List |
|---------|---------|-------------------|
| "Two elements sum to..." | Hashmap for O(1) lookup | Two Sum |
| "Valid matching/nesting" | Stack | Valid Parentheses |
| "Longest/shortest substring" | Sliding Window | Longest Substring |
| "Maximum/minimum subarray" | Kadane's or DP | Maximum Subarray |
| "Connected components in grid" | DFS/BFS on grid | Number of Islands |
| "Dependencies/prerequisites" | Topological Sort | Course Schedule |
| "Level-by-level tree" | BFS with level tracking | Level Order |
| "Merge overlapping ranges" | Sort + greedy | Merge Intervals |
| "Subarray sum equals K" | Prefix sum + hashmap | Subarray Sum |
| "O(1) access + eviction" | HashMap + LinkedList | LRU Cache |

---

## Final Checklist Before Interview

- [ ] Can code all 10 problems without looking (tested!)
- [ ] Can explain approach and complexity for each
- [ ] Know when to use each pattern
- [ ] Have tested setup (video, audio, IDE/editor)
- [ ] Reviewed system design framework
- [ ] Have 2-3 questions ready for interviewer
- [ ] Good sleep night before

---

## You Got This!

These 10 problems demonstrate:
- ✅ Strong DS&A fundamentals
- ✅ Pattern recognition ability
- ✅ Clean coding and communication
- ✅ Problem-solving approach

Master these, and you won't look like a fool - you'll look like someone who knows their stuff.

**Remember:** Interviewers want to see your thought process more than perfect code. Communicate clearly, test your solution, and show confidence.

Good luck at Accord! 🚀

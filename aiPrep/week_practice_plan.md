# 📅 1-Week Practical Learning Plan
## Practice Schedule: 2hrs Coding + 1hr System Design + 30min Behavioral

---

## 🎯 Overall Strategy

Each day follows this pattern:
- **Hour 1 (9:00-10:00 AM):** Theory + Solve 2-3 problems
- **Hour 2 (10:00-11:00 AM):** Build real-world Python project
- **Hour 3 (11:00-12:00 PM):** System Design topic
- **Last 30 min (12:00-12:30 PM):** Behavioral prep (STAR method practice)

---

## 📅 DAY 1: Graph Foundations (DFS, BFS, Cycle Detection)

### Morning Theory (20 min)
- When graph problems appear: "connected", "path", "network"
- DFS: Go deep first (like exploring a maze)
- BFS: Go wide first (like ripples in water)

### LeetCode Problems (40 min each)
1. **Redundant Connection** - DFS cycle detection
2. **Number of Connected Components** - Count islands

### Real Project: File System Explorer (60 min)
**Goal:** Build a tool that explores directory structure

```python
# file_explorer.py
"""
Real-world application of DFS/BFS
Scenario: You're building a file backup system that needs to:
1. Find all files in nested directories (DFS)
2. Find files at specific depth levels (BFS)
3. Detect circular symbolic links (Cycle detection)
"""

import os
from collections import deque

class FileExplorer:
    def __init__(self, root_path):
        self.root_path = root_path
        self.visited = set()
    
    def dfs_find_all_files(self, current_path=None):
        """
        DFS Analogy: Like going room by room in a mansion,
        fully exploring each wing before moving to the next
        """
        if current_path is None:
            current_path = self.root_path
        
        # Prevent infinite loops from symbolic links (cycle detection!)
        real_path = os.path.realpath(current_path)
        if real_path in self.visited:
            print(f"⚠️  Cycle detected at: {current_path}")
            return []
        
        self.visited.add(real_path)
        files = []
        
        try:
            if os.path.isfile(current_path):
                return [current_path]
            
            for item in os.listdir(current_path):
                item_path = os.path.join(current_path, item)
                files.extend(self.dfs_find_all_files(item_path))
        except PermissionError:
            print(f"⛔ Permission denied: {current_path}")
        
        return files
    
    def bfs_files_by_depth(self):
        """
        BFS Analogy: Like scanning one floor of a building at a time
        """
        queue = deque([(self.root_path, 0)])  # (path, depth)
        files_by_depth = {}
        visited = set()
        
        while queue:
            current_path, depth = queue.popleft()
            
            real_path = os.path.realpath(current_path)
            if real_path in visited:
                continue
            visited.add(real_path)
            
            if depth not in files_by_depth:
                files_by_depth[depth] = []
            
            try:
                if os.path.isfile(current_path):
                    files_by_depth[depth].append(current_path)
                else:
                    for item in os.listdir(current_path):
                        queue.append((os.path.join(current_path, item), depth + 1))
            except PermissionError:
                pass
        
        return files_by_depth

# Test it
if __name__ == "__main__":
    explorer = FileExplorer("/tmp")
    
    print("🔍 DFS: Finding all Python files...")
    all_files = explorer.dfs_find_all_files()
    python_files = [f for f in all_files if f.endswith('.py')]
    print(f"Found {len(python_files)} Python files")
    
    print("\n📊 BFS: Files organized by depth...")
    by_depth = explorer.bfs_files_by_depth()
    for depth, files in sorted(by_depth.items())[:3]:  # Show first 3 levels
        print(f"  Depth {depth}: {len(files)} items")
```

**Key Learnings:**
- DFS naturally handles recursion (like nested folders)
- BFS is better when you care about levels/layers
- Cycle detection prevents infinite loops (just like graph problems!)

---

## 📅 DAY 2: Graph Advanced (Dijkstra, Topological Sort, MST)

### LeetCode Problems (40 min each)
1. **Course Schedule** - Topological Sort
2. **Network Delay** - Dijkstra's Algorithm

### Real Project: Task Scheduler (60 min)
**Goal:** Build a build system that handles task dependencies

```python
# task_scheduler.py
"""
Real-world Topological Sort
Scenario: You're building a CI/CD pipeline where:
- Tasks have dependencies (can't deploy before testing)
- You need to find correct execution order
- Detect circular dependencies (impossible builds)
"""

from collections import defaultdict, deque

class TaskScheduler:
    def __init__(self):
        self.tasks = defaultdict(list)  # task -> dependencies
        self.graph = defaultdict(list)   # dependency -> task
        self.indegree = defaultdict(int)
    
    def add_task(self, task, dependencies=None):
        """
        Add a task with its dependencies
        Example: add_task("deploy", ["test", "build"])
        """
        if dependencies is None:
            dependencies = []
        
        self.tasks[task] = dependencies
        if not dependencies:
            self.indegree[task] = 0  # No dependencies
        
        for dep in dependencies:
            self.graph[dep].append(task)
            self.indegree[task] += 1
    
    def can_complete_all_tasks(self):
        """
        Topological Sort - Find if we can complete all tasks
        (Detects circular dependencies)
        
        Analogy: Can you get dressed without paradoxes?
        (Can't put on shoes before socks!)
        """
        # Start with tasks that have no dependencies
        queue = deque([task for task in self.tasks if self.indegree[task] == 0])
        completed_tasks = []
        
        while queue:
            task = queue.popleft()
            completed_tasks.append(task)
            
            # "Complete" this task - check what we can now do
            for next_task in self.graph[task]:
                self.indegree[next_task] -= 1
                if self.indegree[next_task] == 0:
                    queue.append(next_task)
        
        # If we completed all tasks, no circular dependency
        return len(completed_tasks) == len(self.tasks)
    
    def get_execution_order(self):
        """
        Return the correct order to execute tasks
        """
        queue = deque([task for task in self.tasks if self.indegree[task] == 0])
        execution_order = []
        indegree_copy = self.indegree.copy()
        
        while queue:
            task = queue.popleft()
            execution_order.append(task)
            
            for next_task in self.graph[task]:
                indegree_copy[next_task] -= 1
                if indegree_copy[next_task] == 0:
                    queue.append(next_task)
        
        if len(execution_order) != len(self.tasks):
            return None  # Circular dependency detected!
        
        return execution_order

# Test it
if __name__ == "__main__":
    scheduler = TaskScheduler()
    
    # Build a CI/CD pipeline
    scheduler.add_task("install_deps", [])
    scheduler.add_task("lint", ["install_deps"])
    scheduler.add_task("test", ["install_deps"])
    scheduler.add_task("build", ["lint", "test"])
    scheduler.add_task("deploy", ["build"])
    
    print("✅ Can complete pipeline?", scheduler.can_complete_all_tasks())
    print("📋 Execution order:", " → ".join(scheduler.get_execution_order()))
    
    # Try circular dependency
    scheduler2 = TaskScheduler()
    scheduler2.add_task("A", ["B"])
    scheduler2.add_task("B", ["A"])
    print("\n❌ Circular dependency?", not scheduler2.can_complete_all_tasks())
```

### Real Project: Network Router Simulator (60 min)

```python
# network_router.py
"""
Real-world Dijkstra's Algorithm
Scenario: Finding the fastest route for data packets through a network
"""

import heapq
from collections import defaultdict

class NetworkRouter:
    def __init__(self):
        self.graph = defaultdict(list)  # node -> [(neighbor, latency)]
    
    def add_connection(self, node1, node2, latency):
        """
        Add bidirectional connection with latency (in ms)
        """
        self.graph[node1].append((node2, latency))
        self.graph[node2].append((node1, latency))
    
    def find_fastest_route(self, source, destination):
        """
        Dijkstra's Algorithm - Find fastest route
        
        Analogy: Like finding the fastest route on Google Maps
        considering traffic (latency)
        """
        # (latency, current_node, path)
        heap = [(0, source, [source])]
        visited = set()
        min_latency = {source: 0}
        
        while heap:
            current_latency, node, path = heapq.heappop(heap)
            
            if node == destination:
                return path, current_latency
            
            if node in visited:
                continue
            visited.add(node)
            
            for neighbor, latency in self.graph[node]:
                new_latency = current_latency + latency
                
                # Only explore if we found a faster route
                if neighbor not in min_latency or new_latency < min_latency[neighbor]:
                    min_latency[neighbor] = new_latency
                    heapq.heappush(heap, (new_latency, neighbor, path + [neighbor]))
        
        return None, float('inf')  # No route found
    
    def broadcast_time(self, source):
        """
        How long until ALL nodes receive a message from source?
        (Network Delay problem)
        """
        heap = [(0, source)]
        visited = set()
        max_time = 0
        
        while heap:
            time, node = heapq.heappop(heap)
            
            if node in visited:
                continue
            visited.add(node)
            max_time = max(max_time, time)
            
            for neighbor, latency in self.graph[node]:
                if neighbor not in visited:
                    heapq.heappush(heap, (time + latency, neighbor))
        
        # Check if all nodes were reached
        all_nodes = set(self.graph.keys())
        if len(visited) < len(all_nodes):
            return -1  # Some nodes unreachable
        
        return max_time

# Test it
if __name__ == "__main__":
    router = NetworkRouter()
    
    # Build network topology
    router.add_connection("NYC", "Chicago", 20)
    router.add_connection("Chicago", "Denver", 30)
    router.add_connection("NYC", "Atlanta", 15)
    router.add_connection("Atlanta", "Denver", 40)
    router.add_connection("Denver", "LA", 25)
    
    path, latency = router.find_fastest_route("NYC", "LA")
    print(f"🚀 Fastest route NYC → LA: {' → '.join(path)}")
    print(f"⏱️  Total latency: {latency}ms")
    
    broadcast = router.broadcast_time("NYC")
    print(f"\n📡 Time for NYC to broadcast to all nodes: {broadcast}ms")
```

---

## 📅 DAY 3: Dynamic Programming Basics

### LeetCode Problems (40 min each)
1. **Longest Increasing Subsequence**
2. **Longest Common Subsequence**

### Real Project: Text Diff Tool (60 min)

```python
# text_diff.py
"""
Real-world Longest Common Subsequence (LCS)
Scenario: Building a simple version of 'git diff'
"""

class TextDiff:
    def __init__(self, text1, text2):
        self.text1 = text1.split()
        self.text2 = text2.split()
    
    def longest_common_subsequence(self):
        """
        DP Grid Analogy: Building a multiplication table
        Each cell [i][j] represents: "What's the longest match
        between first i words of text1 and first j words of text2?"
        """
        m, n = len(self.text1), len(self.text2)
        
        # Create DP table
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Fill the table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.text1[i-1] == self.text2[j-1]:
                    # Words match! Extend previous match
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    # Take the better of two options
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n]
    
    def get_diff(self):
        """
        Show which lines are added, removed, or kept
        """
        m, n = len(self.text1), len(self.text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.text1[i-1] == self.text2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        # Backtrack to find the actual diff
        diff = []
        i, j = m, n
        
        while i > 0 or j > 0:
            if i > 0 and j > 0 and self.text1[i-1] == self.text2[j-1]:
                diff.append(("  ", self.text1[i-1]))
                i -= 1
                j -= 1
            elif j > 0 and (i == 0 or dp[i][j-1] >= dp[i-1][j]):
                diff.append(("+", self.text2[j-1]))
                j -= 1
            else:
                diff.append(("-", self.text1[i-1]))
                i -= 1
        
        return diff[::-1]

# Test it
if __name__ == "__main__":
    old_code = "def greet name: print hello name"
    new_code = "def greet name: print hello, name!"
    
    differ = TextDiff(old_code, new_code)
    
    print("📊 Common words:", differ.longest_common_subsequence())
    print("\n🔄 Diff:")
    for marker, word in differ.get_diff():
        if marker == "+":
            print(f"  + {word}")
        elif marker == "-":
            print(f"  - {word}")
        else:
            print(f"    {word}")
```

---

## 📅 DAY 4: Sliding Window & Two Pointers

### LeetCode Problems (40 min each)
1. **Longest Substring Without Repeating Characters**
2. **Subarray Sum Equals K**

### Real Project: Log Analyzer (60 min)

```python
# log_analyzer.py
"""
Real-world Sliding Window
Scenario: Analyzing server logs to detect patterns
"""

from collections import defaultdict, deque
from datetime import datetime, timedelta

class LogAnalyzer:
    def __init__(self, log_file):
        self.logs = self.parse_logs(log_file)
    
    def parse_logs(self, log_file):
        """Parse timestamp and status from logs"""
        logs = []
        # Simulate log entries: (timestamp, status_code, endpoint)
        return [
            ("2024-01-01 10:00:00", 200, "/api/users"),
            ("2024-01-01 10:00:01", 200, "/api/users"),
            ("2024-01-01 10:00:02", 500, "/api/users"),
            ("2024-01-01 10:00:03", 500, "/api/users"),
            ("2024-01-01 10:00:04", 500, "/api/users"),
            ("2024-01-01 10:00:10", 200, "/api/posts"),
        ]
    
    def detect_error_spike(self, window_seconds=5, error_threshold=3):
        """
        Sliding Window: Detect if too many errors in a time window
        
        Analogy: Looking for a fever by checking temperature
        over a rolling 5-minute window
        """
        left = 0
        error_count = 0
        alerts = []
        
        for right in range(len(self.logs)):
            # Add new log to window
            timestamp, status, endpoint = self.logs[right]
            if status >= 500:  # Server error
                error_count += 1
            
            # Shrink window if time range exceeds limit
            while left < right:
                left_time = datetime.strptime(self.logs[left][0], "%Y-%m-%d %H:%M:%S")
                right_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                
                if (right_time - left_time).seconds > window_seconds:
                    if self.logs[left][1] >= 500:
                        error_count -= 1
                    left += 1
                else:
                    break
            
            # Check if we have an error spike
            if error_count >= error_threshold:
                alerts.append(f"⚠️  Error spike detected at {timestamp}: {error_count} errors in {window_seconds}s")
        
        return alerts
    
    def find_longest_stable_period(self):
        """
        Find longest period with no errors
        
        Sliding Window (variable size)
        """
        left = 0
        max_period = 0
        current_start = None
        best_start = None
        best_end = None
        
        for right in range(len(self.logs)):
            timestamp, status, endpoint = self.logs[right]
            
            # If we hit an error, reset window
            if status >= 500:
                left = right + 1
                current_start = None
            else:
                if current_start is None:
                    current_start = timestamp
                
                period_length = right - left + 1
                if period_length > max_period:
                    max_period = period_length
                    best_start = current_start
                    best_end = timestamp
        
        return best_start, best_end, max_period

# Test it
if __name__ == "__main__":
    analyzer = LogAnalyzer("server.log")
    
    print("🔍 Detecting error spikes...")
    alerts = analyzer.detect_error_spike(window_seconds=5, error_threshold=3)
    for alert in alerts:
        print(alert)
    
    start, end, length = analyzer.find_longest_stable_period()
    print(f"\n✅ Longest stable period: {start} to {end} ({length} requests)")
```

---

## 📅 DAY 5: Heaps & Priority Queues

### LeetCode Problems (40 min each)
1. **Merge K Sorted Lists**
2. **Koko Eating Bananas** (Binary Search)

### Real Project: Task Priority System (60 min)

```python
# priority_task_manager.py
"""
Real-world Heap Usage
Scenario: Customer support ticket system with priorities
"""

import heapq
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

@dataclass(order=True)
class Ticket:
    priority: int  # Lower number = higher priority
    timestamp: datetime = field(compare=False)
    customer_id: str = field(compare=False)
    issue: str = field(compare=False)
    
class CustomerSupportSystem:
    def __init__(self):
        self.heap = []
        self.ticket_count = 0
    
    def add_ticket(self, customer_id, issue, priority_level="medium"):
        """
        Add a ticket to the system
        Priority levels: critical=1, high=2, medium=3, low=4
        
        Heap Analogy: Emergency room triage
        Critical patients get seen first, regardless of arrival time
        """
        priority_map = {"critical": 1, "high": 2, "medium": 3, "low": 4}
        priority = priority_map.get(priority_level, 3)
        
        ticket = Ticket(
            priority=priority,
            timestamp=datetime.now(),
            customer_id=customer_id,
            issue=issue
        )
        
        heapq.heappush(self.heap, ticket)
        self.ticket_count += 1
        print(f"✅ Ticket #{self.ticket_count} added: [{priority_level.upper()}] {issue}")
    
    def get_next_ticket(self):
        """
        Get highest priority ticket to work on
        O(log n) time!
        """
        if not self.heap:
            return None
        
        ticket = heapq.heappop(self.heap)
        return ticket
    
    def get_top_k_urgent(self, k):
        """
        See top K most urgent tickets without removing them
        (This is a common heap pattern!)
        """
        # Create a copy so we don't modify original
        temp_heap = self.heap.copy()
        results = []
        
        for _ in range(min(k, len(temp_heap))):
            results.append(heapq.heappop(temp_heap))
        
        return results

# Test it
if __name__ == "__main__":
    support = CustomerSupportSystem()
    
    # Add tickets in random order
    support.add_ticket("CUST001", "Website is down", "critical")
    support.add_ticket("CUST002", "Can't login", "high")
    support.add_ticket("CUST003", "UI looks weird", "low")
    support.add_ticket("CUST004", "Data loss!", "critical")
    support.add_ticket("CUST005", "Slow loading", "medium")
    
    print("\n🎯 Working on tickets in priority order:")
    print("=" * 50)
    
    while True:
        ticket = support.get_next_ticket()
        if not ticket:
            break
        priority_names = {1: "CRITICAL", 2: "HIGH", 3: "MEDIUM", 4: "LOW"}
        print(f"[{priority_names[ticket.priority]}] {ticket.customer_id}: {ticket.issue}")
```

### Real Project: Rate Limiter (60 min)

```python
# rate_limiter.py
"""
Real-world Sliding Window + Deque
Scenario: API rate limiting (e.g., max 100 requests per minute)
"""

from collections import deque
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests, time_window_seconds):
        """
        Sliding Window Rate Limiter
        Example: max 5 requests per 10 seconds
        
        Analogy: Nightclub bouncer counting people who entered
        in the last hour
        """
        self.max_requests = max_requests
        self.time_window = timedelta(seconds=time_window_seconds)
        self.request_times = deque()  # Timestamps of requests
    
    def allow_request(self, user_id):
        """
        Check if request should be allowed
        """
        now = datetime.now()
        
        # Remove requests outside time window (sliding!)
        while self.request_times and now - self.request_times[0] > self.time_window:
            self.request_times.popleft()
        
        # Check if under limit
        if len(self.request_times) < self.max_requests:
            self.request_times.append(now)
            return True
        
        # Rate limit exceeded
        oldest_request = self.request_times[0]
        retry_after = (oldest_request + self.time_window - now).seconds
        return False, retry_after
    
    def get_current_usage(self):
        """How many requests in current window"""
        now = datetime.now()
        while self.request_times and now - self.request_times[0] > self.time_window:
            self.request_times.popleft()
        return len(self.request_times)

# Test it
if __name__ == "__main__":
    import time
    
    limiter = RateLimiter(max_requests=3, time_window_seconds=5)
    
    print("🚦 Testing rate limiter (3 requests per 5 seconds):\n")
    
    for i in range(6):
        result = limiter.allow_request("user123")
        
        if result is True:
            print(f"✅ Request {i+1}: ALLOWED (usage: {limiter.get_current_usage()}/3)")
        else:
            _, retry_after = result
            print(f"❌ Request {i+1}: BLOCKED (retry in {retry_after}s)")
        
        time.sleep(1)
```

---

## 📅 DAY 6: String Manipulation & Review

### LeetCode Problems (40 min each)
1. **Word Break**
2. **Longest Palindromic Substring**

### Real Project: Smart Autocomplete (60 min)

```python
# autocomplete.py
"""
Real-world Trie (Prefix Tree) + String Algorithms
Scenario: Building a search autocomplete like Google
"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0  # How often this word is searched

class Autocomplete:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word, frequency=1):
        """
        Add word to trie
        
        Trie Analogy: Like organizing a library by first letter,
        then second letter, and so on
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
        node.frequency += frequency
    
    def search_suggestions(self, prefix, max_results=5):
        """
        Find top suggestions for a prefix
        """
        # Navigate to the prefix
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # DFS to find all words with this prefix
        suggestions = []
        self._dfs_collect_words(node, prefix, suggestions)
        
        # Sort by frequency and return top results
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return [word for word, freq in suggestions[:max_results]]
    
    def _dfs_collect_words(self, node, current_word, suggestions):
        """Helper DFS to collect all words from a node"""
        if node.is_end_of_word:
            suggestions.append((current_word, node.frequency))
        
        for char, child_node in node.children.items():
            self._dfs_collect_words(child_node, current_word + char, suggestions)

# Test it
if __name__ == "__main__":
    autocomplete = Autocomplete()
    
    # Simulate user searches
    searches = [
        ("python tutorial", 100),
        ("python flask", 80),
        ("python django", 90),
        ("python basics", 120),
        ("java tutorial", 70),
        ("javascript", 60),
    ]
    
    for word, freq in searches:
        autocomplete.insert(word, freq)
    
    print("🔍 Autocomplete Demo:\n")
    test_prefixes = ["py", "python", "java"]
    
    for prefix in test_prefixes:
        suggestions = autocomplete.search_suggestions(prefix)
        print(f"'{prefix}' → {suggestions}")
```

---

## 📅 DAY 7: Mixed Practice & System Design

### Morning: Speed Run (30 min total)
Pick 3 random problems from different categories and solve them FAST:
- 1 Graph problem (10 min)
- 1 DP problem (10 min)
- 1 Array/String problem (10 min)

**Goal:** Build speed and pattern recognition

### Real Project: Mini Database (90 min)

```python
# mini_database.py
"""
Combines multiple concepts: Hash Maps, Binary Search, Sliding Window
Scenario: Build a simple in-memory database with indexing
"""

from collections import defaultdict
import bisect

class MiniDatabase:
    def __init__(self):
        self.records = []  # List of dictionaries
        self.indexes = defaultdict(list)  # field_name -> sorted list of (value, record_id)
    
    def insert(self, record):
        """
        Insert a record
        O(1) for insertion, O(log n) for index updates
        """
        record_id = len(self.records)
        self.records.append(record)
        
        # Update indexes
        for field, value in record.items():
            bisect.insort(self.indexes[field], (value, record_id))
        
        return record_id
    
    def find_by_field(self, field, value):
        """
        Binary Search on indexed field
        O(log n) lookup!
        """
        if field not in self.indexes:
            # Fallback to linear search
            return [r for r in self.records if r.get(field) == value]
        
        # Binary search in sorted index
        index = self.indexes[field]
        left = bisect.bisect_left(index, (value, 0))
        right = bisect.bisect_right(index, (value, float('inf')))
        
        return [self.records[record_id] for _, record_id in index[left:right]]
    
    def range_query(self, field, min_value, max_value):
        """
        Find records where field is between min and max
        Uses binary search on index
        """
        if field not in self.indexes:
            return []
        
        index = self.indexes[field]
        left = bisect.bisect_left(index, (min_value, 0))
        right = bisect.bisect_right(index, (max_value, float('inf')))
        
        return [self.records[record_id] for _, record_id in index[left:right]]
    
    def get_top_k(self, field, k):
        """
        Get top K records by field value
        Uses heap concept (but we cheat with sorted index)
        """
        if field not in self.indexes:
            return []
        
        index = self.indexes[field]
        # Return top K (they're already sorted!)
        return [self.records[record_id] for _, record_id in index[-k:]]

# Test it
if __name__ == "__main__":
    db = MiniDatabase()
    
    # Insert employee records
    db.insert({"name": "Alice", "salary": 75000, "dept": "Engineering"})
    db.insert({"name": "Bob", "salary": 65000, "dept": "Marketing"})
    db.insert({"name": "Charlie", "salary": 85000, "dept": "Engineering"})
    db.insert({"name": "Diana", "salary": 95000, "dept": "Sales"})
    
    print("🔍 Find all in Engineering:")
    print(db.find_by_field("dept", "Engineering"))
    
    print("\n💰 Salary range $70k-$90k:")
    print(db.range_query("salary", 70000, 90000))
    
    print("\n🏆 Top 2 earners:")
    print(db.get_top_k("salary", 2))
```

---

## 🎯 System Design Topics (1hr per day)

- **Day 1:** URL Shortener (TinyURL)
- **Day 2:** Design Twitter Feed
- **Day 3:** Design Netflix/YouTube
- **Day 4:** Design Uber/Lyft
- **Day 5:** Design WhatsApp
- **Day 6:** Design Dropbox
- **Day 7:** Design Rate Limiter

**Key Framework:**
1. **Requirements** (5 min) - Functional & Non-functional
2. **Capacity Estimation** (5 min) - Users, requests/sec, storage
3. **High-Level Design** (15 min) - Draw boxes and arrows
4. **Deep Dive** (25 min) - Database schema, APIs, algorithms
5. **Bottlenecks** (10 min) - What could fail? How to scale?

---

## 🎭 Behavioral Prep (30 min per day)

### STAR Method Practice
Prepare 5 stories covering:
1. **Leadership:** When you led a project
2. **Conflict:** Disagreement with teammate
3. **Failure:** Project that failed and what you learned
4. **Impact:** Your biggest achievement
5. **Technical Challenge:** Hardest bug you fixed

**Template:**
- **S**ituation: "In my previous role at X..."
- **T**ask: "I was responsible for..."
- **A**ction: "I decided to... because..."
- **R**esult: "This led to... measured by..."

---

## 📊 Progress Tracker

Create a simple spreadsheet:

| Day | Problems Solved | Project Built | System Design | Behavioral |
|-----|----------------|---------------|---------------|------------|
| 1   | ☐ ☐ ☐         | ☐             | ☐             | ☐          |
| 2   | ☐ ☐ ☐         | ☐             | ☐             | ☐          |
| ... | ...           | ...           | ...           | ...        |

**Daily reflection question:**
"What pattern did I learn today that I can explain to someone else?"

---

## 🚀 Week Success Checklist

By end of week, you should be able to:
- ☐ Identify pattern within 30 seconds of reading problem
- ☐ Explain your approach before coding
- ☐ Code without major syntax errors
- ☐ Test with 3+ edge cases
- ☐ Optimize to better time/space complexity
- ☐ Explain one complete system design end-to-end
- ☐ Tell 5 STAR stories confidently

Remember: **Consistency > Intensity**
Better to do 2 hours daily than 14 hours on Sunday!

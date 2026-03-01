"""
DAY 2 PROJECT B: Network Router Simulator
Concept: Dijkstra's Algorithm (Shortest Path in Weighted Graph)

Real-world scenario: Finding fastest data route through network
- Routers with different latencies (weights)
- Find minimum time to reach destination
- Calculate broadcast time to all nodes
"""

import heapq
from collections import defaultdict

class NetworkRouter:
    def __init__(self):
        self.graph = defaultdict(list)  # node -> [(neighbor, latency)]
        self.nodes = set()
    
    def add_connection(self, node1, node2, latency):
        """
        Add bidirectional connection with latency (in milliseconds)
        
        Think of latency like:
        - Highway miles between cities
        - Flight time between airports
        - Ping time between servers
        """
        self.graph[node1].append((node2, latency))
        self.graph[node2].append((node1, latency))  # Bidirectional
        self.nodes.add(node1)
        self.nodes.add(node2)
    
    def dijkstra_shortest_path(self, source, destination):
        """
        Dijkstra's Algorithm - Find shortest path
        
        ANALOGY: Google Maps finding fastest route
        - Start at your location
        - Always explore the nearest unexplored place
        - Keep track of best time to reach each place
        - Stop when you reach destination
        
        ALGORITHM:
        1. Start with source, distance = 0
        2. Use MIN HEAP to always pick closest unvisited node
        3. For each neighbor, try to "relax" the distance
           - If new_distance < old_distance, update it!
        4. Mark as visited once popped from heap
        5. Stop when we reach destination
        
        WHY HEAP?
        - Need to always get the node with minimum distance
        - Heap gives us O(log n) insert/extract
        - Without heap, would be O(n²) to find minimum each time
        
        TIME: O((V + E) log V) with heap
        SPACE: O(V)
        """
        # Min heap: (distance, node, path)
        heap = [(0, source, [source])]
        visited = set()
        distances = {source: 0}
        
        while heap:
            current_distance, node, path = heapq.heappop(heap)
            
            # Found destination!
            if node == destination:
                return path, current_distance
            
            # Skip if already visited
            if node in visited:
                continue
            visited.add(node)
            
            # Try all neighbors
            for neighbor, latency in self.graph[node]:
                if neighbor in visited:
                    continue
                
                new_distance = current_distance + latency
                
                # RELAXATION: If we found a better path, use it!
                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(heap, (new_distance, neighbor, path + [neighbor]))
        
        return None, float('inf')  # No path found
    
    def all_shortest_paths(self, source):
        """
        Find shortest distance to ALL nodes from source
        (Used in "Network Delay" problem)
        """
        heap = [(0, source)]
        distances = {source: 0}
        visited = set()
        
        while heap:
            current_distance, node = heapq.heappop(heap)
            
            if node in visited:
                continue
            visited.add(node)
            
            for neighbor, latency in self.graph[node]:
                new_distance = current_distance + latency
                
                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(heap, (new_distance, neighbor))
        
        return distances
    
    def network_broadcast_time(self, source):
        """
        Network Delay Problem:
        How long until ALL nodes receive a broadcast from source?
        
        Answer: Maximum of all shortest paths
        (Bottleneck = slowest node to reach)
        """
        distances = self.all_shortest_paths(source)
        
        # Check if all nodes were reached
        if len(distances) < len(self.nodes):
            return -1  # Some nodes unreachable
        
        # Maximum time = time for slowest node
        return max(distances.values())
    
    def find_alternative_routes(self, source, destination, k=3):
        """
        Find K alternative routes (not necessarily shortest)
        Using modified Dijkstra that doesn't mark as visited immediately
        """
        # Heap: (distance, node, path)
        heap = [(0, source, [source])]
        found_paths = []
        visit_count = defaultdict(int)
        
        while heap and len(found_paths) < k:
            distance, node, path = heapq.heappop(heap)
            
            # Found a path to destination
            if node == destination:
                found_paths.append((path, distance))
                continue
            
            # Allow visiting node multiple times (for alt routes)
            visit_count[node] += 1
            if visit_count[node] > k:  # But not too many times
                continue
            
            for neighbor, latency in self.graph[node]:
                if neighbor not in path:  # Avoid cycles in same path
                    new_path = path + [neighbor]
                    new_distance = distance + latency
                    heapq.heappush(heap, (new_distance, neighbor, new_path))
        
        return found_paths


def demo():
    print("=" * 70)
    print("🌐 NETWORK ROUTER DEMO - Dijkstra's Algorithm")
    print("=" * 70)
    
    # Build a network
    router = NetworkRouter()
    
    # USA Network Topology
    router.add_connection("NYC", "Chicago", 20)
    router.add_connection("NYC", "Atlanta", 15)
    router.add_connection("Chicago", "Denver", 30)
    router.add_connection("Atlanta", "Denver", 40)
    router.add_connection("Denver", "LA", 25)
    router.add_connection("Atlanta", "Dallas", 18)
    router.add_connection("Dallas", "LA", 35)
    router.add_connection("Chicago", "Seattle", 45)
    router.add_connection("Seattle", "LA", 30)
    
    print("\n🗺️  Network Topology:")
    print("""
           Seattle
             /  \\
            45   30
           /      \\
      Chicago --- Denver --- LA
         |    30     | 25   /
         20          40   35
         |           |   /
        NYC ----  Atlanta
           15    18  \\
                    Dallas
    
    Numbers = latency in milliseconds
    """)
    
    # Demo 1: Find fastest route
    print("\n📍 DEMO 1: Finding Fastest Route")
    print("-" * 70)
    
    path, time = router.dijkstra_shortest_path("NYC", "LA")
    print(f"Source: NYC")
    print(f"Destination: LA")
    print(f"\n✅ Fastest route: {' → '.join(path)}")
    print(f"⏱️  Total latency: {time}ms")
    
    # Compare with alternative
    alt_routes = router.find_alternative_routes("NYC", "LA", k=3)
    print(f"\n🔀 Alternative routes:")
    for i, (route, latency) in enumerate(alt_routes, 1):
        print(f"  {i}. {' → '.join(route)} ({latency}ms)")
    
    # Demo 2: Broadcast time
    print("\n\n📍 DEMO 2: Network Broadcast Time")
    print("-" * 70)
    print("Question: If NYC sends a broadcast, how long until")
    print("all cities receive it?")
    
    broadcast_time = router.network_broadcast_time("NYC")
    print(f"\n📡 Broadcast time: {broadcast_time}ms")
    print("(This is the time for the SLOWEST city to receive it)")
    
    distances = router.all_shortest_paths("NYC")
    print("\n⏱️  Time for each city:")
    for city, time in sorted(distances.items(), key=lambda x: x[1]):
        print(f"  {city:12} : {time:3}ms")
    
    # Demo 3: Comparing routes
    print("\n\n📍 DEMO 3: Why Dijkstra > BFS for Weighted Graphs")
    print("-" * 70)
    
    # Create simple weighted graph to show why BFS fails
    router2 = NetworkRouter()
    router2.add_connection("A", "B", 1)
    router2.add_connection("A", "C", 10)
    router2.add_connection("B", "C", 1)
    
    print("Graph:")
    print("  A --1--> B")
    print("  |         \\")
    print("  10        1")
    print("  |          \\")
    print("  └--------> C")
    
    path, time = router2.dijkstra_shortest_path("A", "C")
    print(f"\n✅ Dijkstra finds: {' → '.join(path)} (cost: {time})")
    print(f"❌ BFS would find: A → C (cost: 10) - WRONG!")
    print("\nWHY? BFS only counts hops, not weights!")


def interview_walkthrough():
    print("\n\n" + "=" * 70)
    print("💼 INTERVIEW WALKTHROUGH - Network Delay Problem")
    print("=" * 70)
    
    print("""
    QUESTION: You're given a network of n nodes (1 to n) and a list of travel
    times as directed edges times[i] = (u, v, w), where u is source node,
    v is target node, and w is the time for a signal to travel from u to v.
    
    Send a signal from node k. Return the minimum time for all nodes to
    receive the signal. If impossible, return -1.
    
    Example:
    n = 4, times = [[2,1,1], [2,3,1], [3,4,1]], k = 2
    
    STEP-BY-STEP THINKING:
    
    1️⃣  RECOGNIZE THE PATTERN
       - "Network", "travel time" → Weighted graph
       - "Minimum time" → Shortest path
       - "All nodes" → Find shortest path to all nodes
       - "From node k" → Single source
       → This is DIJKSTRA'S ALGORITHM
    
    2️⃣  VISUALIZE THE GRAPH
       Draw it:
       
         2 --1--> 1
         |
         1
         ↓
         3 --1--> 4
       
       From node 2:
       - Node 2 → Node 1: 1 time unit
       - Node 2 → Node 3: 1 time unit
       - Node 2 → Node 3 → Node 4: 2 time units
       
       Maximum time = 2 (node 4 is bottleneck)
    
    3️⃣  WHY NOT BFS?
       BFS works for UNWEIGHTED graphs only!
       BFS counts hops, but we care about TOTAL WEIGHT
       
       Counterexample:
       A --100--> B
       |          ↑
       1          1
       ↓          |
       C ---------┘
       
       BFS: A → B (1 hop) = WRONG (cost 100)
       Dijkstra: A → C → B (2 hops) = CORRECT (cost 2)
    
    4️⃣  DATA STRUCTURES
       - graph: dict of lists [(neighbor, time)]
       - heap: min-heap of (time, node)
       - distances: dict of {node: min_time}
       - visited: set of processed nodes
    
    5️⃣  ALGORITHM STEPS
       
       1. Build adjacency list from edges
       2. Initialize: distances[source] = 0, others = infinity
       3. Push (0, source) to min-heap
       4. While heap not empty:
          a. Pop node with minimum distance
          b. If already visited, skip
          c. Mark as visited
          d. For each neighbor:
             - Calculate new_time = current_time + edge_time
             - If new_time < best_time[neighbor]:
               Update and push to heap
       5. Return max(distances) if all reachable, else -1
    
    6️⃣  RELAXATION EXPLAINED
       "Relaxation" = updating to a better path
       
       Current best to reach B: 10
       New path through A: 7
       → Relax: Update B's distance to 7
       
       Why "relax"? Like relaxing a rubber band to shortest length!
    
    7️⃣  WHY MIN-HEAP?
       We always want to process the CLOSEST unvisited node
       - Without heap: O(n²) to find minimum each time
       - With heap: O(log n) to extract minimum
       Total: O((V + E) log V) vs O(V²)
    
    8️⃣  CODE
       ```python
       import heapq
       from collections import defaultdict
       
       def network_delay(times, n, k):
           # Build graph
           graph = defaultdict(list)
           for u, v, w in times:
               graph[u].append((v, w))
           
           # Dijkstra
           heap = [(0, k)]  # (time, node)
           distances = {}
           
           while heap:
               time, node = heapq.heappop(heap)
               
               if node in distances:
                   continue  # Already visited
               
               distances[node] = time
               
               for neighbor, weight in graph[node]:
                   if neighbor not in distances:
                       heapq.heappush(heap, (time + weight, neighbor))
           
           # Check if all nodes reachable
           if len(distances) != n:
               return -1
           
           return max(distances.values())
       ```
    
    9️⃣  EDGE CASES
       ✓ Unreachable nodes (disconnected graph)
       ✓ Self-loops (usually ignored)
       ✓ Multiple edges between same nodes (take minimum)
       ✓ Single node (return 0)
    
    🔟 COMPLEXITY
       Time: O((V + E) log V)
       - Each edge processed once: O(E)
       - Heap operations: O(log V)
       - Each vertex processed once: O(V)
       
       Space: O(V + E)
       - Graph storage: O(E)
       - Heap: O(V) worst case
       - Distances: O(V)
    """)


def key_insights():
    print("\n" + "=" * 70)
    print("🎯 KEY INSIGHTS - Dijkstra's Algorithm")
    print("=" * 70)
    print("""
    1. WHEN TO USE
       ✓ Weighted graph (edges have costs/weights)
       ✓ Need shortest path from one source
       ✓ All weights are NON-NEGATIVE
       
       Keywords: "shortest", "minimum time/cost", "weighted", "network"
    
    2. VS OTHER ALGORITHMS
       
       BFS:
       - Unweighted graphs only
       - O(V + E) time
       - Use when all edges have same cost
       
       Dijkstra:
       - Weighted graphs
       - O((V + E) log V) time
       - Weights must be non-negative
       - Use for shortest path
       
       Bellman-Ford:
       - Weighted graphs
       - O(V * E) time (slower!)
       - Works with negative weights
       - Can detect negative cycles
    
    3. THE HEAP TRICK
       Why min-heap is critical:
       - Dijkstra = "always explore nearest unknown node"
       - Heap gives us min in O(log n)
       - Without heap: O(n) to find min each time
       - Makes algorithm practical!
    
    4. GREEDY NATURE
       Dijkstra is greedy:
       - "Always pick closest unvisited node"
       - Once visited, we know it's optimal (with non-negative weights)
       - This is why negative weights break it!
    
    5. REAL-WORLD USES
       - GPS navigation
       - Network routing (OSPF protocol)
       - Flight booking (cheapest route)
       - Game AI pathfinding
       - Delivery route optimization
    
    6. VARIANTS
       - Single source to single target (stop early)
       - Single source to all targets (what we did)
       - All pairs shortest path (use Floyd-Warshall instead)
    
    7. INTERVIEW TIPS
       - Always mention "min-heap" and why
       - Explain relaxation clearly
       - Draw the graph first!
       - Walk through example step by step
       - Mention time/space complexity
       - Distinguish from BFS (weighted vs unweighted)
    
    8. COMMON MISTAKES
       ❌ Forgetting to check if node already visited
       ❌ Using regular queue instead of priority queue
       ❌ Not handling unreachable nodes
       ❌ Trying to use with negative weights
    """)


if __name__ == "__main__":
    demo()
    interview_walkthrough()
    key_insights()

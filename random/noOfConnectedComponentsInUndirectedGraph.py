# You have a graph of n nodes. You are given an integer n and an array edges where edges[i] = [ai, bi] indicates that there is an edge between ai and bi in the graph.

# Return the number of connected components in the graph.

from collections import defaultdict
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        visited = set()
        numberOfComponents = 0

        def buildGraph(edges):
            graph = defaultdict(list)
            for edge in edges:
                node1, node2 = edge
                graph[node1].append(node2)
                graph[node2].append(node1)
            return graph
        
        def exploreComponent(graph, node):
            if node in visited: return False
            visited.add(node)
            for neighbor in graph[node]:
                exploreComponent(graph, neighbor)
            return True
        
        graph = buildGraph(edges)

        for node in range(n):
            if node not in visited:
                if exploreComponent(graph, node):
                    numberOfComponents += 1
        
        return numberOfComponents


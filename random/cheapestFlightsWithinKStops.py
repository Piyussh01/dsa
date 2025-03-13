class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        INF = float('inf')
        dp = [INF] * n
        dp[src] = 0

        for _ in range(k+1):
            temp = dp.copy()
            for u,v,w in flights:
                if dp[u] != INF and dp[u] + w < temp[v]:
                    temp[v] = dp[u] + w
            dp = temp
        return dp[dst] if dp[dst] != INF else -1
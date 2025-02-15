class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        minP = float('inf')
        maxP = 0
        for i in range(len(prices)):
            minP = min(prices[i] , minP)
            maxP = max(prices[i] - minP , maxP)

        return (maxP)
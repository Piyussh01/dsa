class Solution:
    def deleteAndEarn(self, nums: List[int]) -> int:
        if not nums:
            return 0
        counts = Counter(nums)
        max_val = max(nums)

        points = [0] * (max_val + 1)
        for x in range(1, max_val + 1):
            points[x] = x * counts.get(x, 0)
        
        dp = [0] * (max_val + 1)
        dp[0] = 0
        dp[1] = points[1]

        for i in range(2, max_val + 1):
            dp[i] = max(dp[i -1], dp[i - 2] + points[i])
        return dp[max_val]


#This approach runs in  O(n + M)  time, where  M  is the maximum number in nums (and  M \leq 10^4  per constraints), and uses  O(M)  space. It effectively converts the problem into a variant of the House Robber problem.
class Solution:
    def rob_linear(self, nums: List[int]) -> int:
        n = len(nums)
        dp = [0] * n
        if n == 1:
            return nums[0]
        if n == 2:
            return max(nums[0],nums[1])

        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
        
        for i in range(2, n):
            dp[i] = max(dp[i-1], nums[i] + dp[i-2])
        
        return dp[-1] 

    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        if n == 1:
            return nums[0]
        
        case1 = self.rob_linear(nums[:-1]) # from 0 to n-1
        case2 = self.rob_linear(nums[1:]) # from 1 to n 
        
        return max(case1, case2)
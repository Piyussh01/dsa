class Solution:
    def rob(self, nums: List[int]) -> int:
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
#O(n) and #O(n)

#below space is O(1)
# class Solution:
#     def rob(self, nums: List[int]) -> int:
#         prev_rob = max_rob = 0

#         for cur_val in nums:
#             temp = max(max_rob, prev_rob + cur_val)
#             prev_rob = max_rob
#             max_rob = temp
        
#         return max_rob


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        maxReach = 0
        for i, jump in enumerate(nums):
            if i > maxReach:
                # If the current index is beyond the farthest we can reach, return False.
                return False
            maxReach = max(maxReach, i + jump)
        return True
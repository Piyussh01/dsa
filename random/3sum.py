class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # at 0, i , i +1 , i+2 and see that sum adds 0 
        nums.sort()
        n = len(nums)
        res = []
        for i in range(n - 2):
            #skip duplicates
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            l,r = i + 1, n - 1 
            while l < r:
                total = nums[i] + nums[l] + nums[r]
                if total<0:
                    l += 1
                elif total>0:
                    r -= 1
                else:
                    res.append([nums[i], nums[l], nums[r]])
                    while l < r and nums[l] == nums[l + 1]:
                        l += 1
                    while l < r and nums[r] == nums[r - 1]:
                        r -= 1
                    l += 1
                    r -= 1
        return res

            
#This solution runs in O(n^2) time and meets the problem constraints while avoiding duplicate triplets.
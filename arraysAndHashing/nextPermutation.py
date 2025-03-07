class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        i = n - 1
        while i > 0 and nums[i - 1] >= nums[i]:
            i -= 1
        if i == 0:
            nums.reverse()
            return 
        pivot = i -1 
        j = n -1
        while nums[j] <= nums[pivot]:
            j -= 1
        nums[pivot], nums[j] = nums[j], nums[pivot]
        l,r = i, n - 1
        while l< r :
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1



# The standard approach to generate the next permutation in-place (using constant extra memory) is as follows:
# 	1.	Find the pivot:
# Traverse from right to left until you find the first index i - 1 where nums[i-1] < nums[i]. This is the “pivot” where a higher permutation might be possible.
# 	2.	No pivot found:
# If no such index exists (i.e. the array is non-increasing), then the array is the highest permutation. In this case, simply reverse the entire array to transform it into the lowest possible order.
# 	3.	Find the element to swap:
# Once you have the pivot at index i-1, again traverse from the right end and find the first element nums[j] that is greater than nums[i-1].
# 	4.	Swap the pivot with this element:
# Swap nums[i-1] with nums[j].
# 	5.	Reverse the suffix:
# Reverse the subarray starting from index i to the end. This ensures the suffix is in increasing order (the smallest order), which completes the next permutation.  
# Example Walkthrough

# For nums = [1, 2, 3]:
# 	1.	Find pivot:
# 	•	Start from the right: compare 3 and 2 → since 2 < 3, the pivot is at index i-1 = 1 (value 2).
# 	2.	Find the element to swap:
# 	•	From the right, find the first element greater than 2. Here, 3 (index 2) is greater than 2.
# 	3.	Swap:
# 	•	Swap nums[1] and nums[2], so nums becomes [1, 3, 2].
# 	4.	Reverse suffix:
# 	•	The suffix starting at index 2 (which is just [2]) is already in increasing order, so the final result is [1, 3, 2].

# This is the next permutation of [1, 2, 3].
            

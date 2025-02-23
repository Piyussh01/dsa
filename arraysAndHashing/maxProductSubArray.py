class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        # Initialize max_prod, min_prod, and result with the first element.
        max_prod = min_prod = res = nums[0]
        
        # Iterate through the array starting from the second element.
        for n in nums[1:]:
            # When n is negative, swapping max_prod and min_prod is necessary,
            # because multiplying by a negative flips signs.
            if n < 0:
                max_prod, min_prod = min_prod, max_prod
                
            # Update max_prod and min_prod.
            # max_prod is the maximum of the current number or the product including the previous max_prod.
            max_prod = max(n, max_prod * n)
            min_prod = min(n, min_prod * n)
            
            # Update the result with the maximum product so far.
            res = max(res, max_prod)
            
        return res
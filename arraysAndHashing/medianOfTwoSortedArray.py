class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # Ensure that nums1 is the smaller array.
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        
        m, n = len(nums1), len(nums2)
        left_partition_size = (m + n + 1) // 2  # total elements in left partition
        
        left, right = 0, m
        while left <= right:
            i = (left + right) // 2  # elements taken from nums1 for left partition
            j = left_partition_size - i  # elements taken from nums2
            
            # If i is 0, no elements from nums1 in left partition, so L1 = -∞.
            L1 = nums1[i - 1] if i > 0 else float('-inf')
            # If i is m, then no elements from nums1 in right partition, so R1 = +∞.
            R1 = nums1[i] if i < m else float('inf')
            
            # Similarly for nums2:
            L2 = nums2[j - 1] if j > 0 else float('-inf')
            R2 = nums2[j] if j < n else float('inf')
            
            # Check if the partition is correct:
            if L1 > R2:
                # Too many elements from nums1 in the left partition; move left pointer to left.
                right = i - 1
            elif L2 > R1:
                # Too few elements from nums1 in the left partition; move left pointer to right.
                left = i + 1
            else:
                # Correct partition found.
                if (m + n) % 2 == 1:
                    return float(max(L1, L2))
                else:
                    return (max(L1, L2) + min(R1, R2)) / 2.0
        # This return is never reached if input is valid.
        return 0.0
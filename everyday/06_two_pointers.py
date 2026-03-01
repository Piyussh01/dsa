"""
TWO POINTERS — Three Patterns
================================

WHEN TO USE:
  - Sorted array + find pair with some property
  - "Two sum" variant on sorted array
  - Linked list cycle detection
  - Merging two sorted things
  - Partitioning (Dutch flag, move zeros)

MENTAL MODEL:
  Pattern 1: OPPOSITE ENDS → left starts at 0, right starts at end, move inward
  Pattern 2: FAST & SLOW  → both start at 0, fast moves ahead
  Pattern 3: TWO ARRAYS   → one pointer per array, merge-style
"""


# ============================================================
# PATTERN 1: Opposite ends (sorted array)
# ============================================================

# Two Sum II (sorted array)
def twoSum(numbers, target):
    left, right = 0, len(numbers) - 1

    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return [left + 1, right + 1]  # 1-indexed
        elif total < target:
            left += 1         # need bigger sum
        else:
            right -= 1        # need smaller sum

    return []


# Container With Most Water
def maxArea(height):
    left, right = 0, len(height) - 1
    best = 0

    while left < right:
        w = right - left
        h = min(height[left], height[right])
        best = max(best, w * h)

        # move the SHORTER side (it's the bottleneck)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return best


# 3Sum — sort + fix one + two pointers for remaining
def threeSum(nums):
    nums.sort()
    result = []

    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:  # skip duplicates
            continue

        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1    # skip duplicates
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1   # skip duplicates
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1

    return result


# ============================================================
# PATTERN 2: Fast & Slow
# ============================================================

# Linked list cycle detection (Floyd's)
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# Find cycle start
def detectCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # reset one pointer to head, move both at speed 1
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow  # cycle start
    return None


# Move Zeros — fast finds non-zeros, slow marks placement position
def moveZeroes(nums):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1


# ============================================================
# PATTERN 3: Two arrays (merge style)
# ============================================================

# Merge two sorted arrays
def merge(nums1, m, nums2, n):
    # fill from the END to avoid overwriting
    p1, p2, p = m - 1, n - 1, m + n - 1

    while p2 >= 0:
        if p1 >= 0 and nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1


"""
DECISION GUIDE:

  Sorted array, find pair?      → Opposite ends
  Linked list cycle?            → Fast & slow
  Partition / rearrange in-place? → Fast & slow
  Merge two sorted things?      → One pointer each

  KEY INSIGHT:
    Two pointers works because moving a pointer ELIMINATES
    a chunk of possibilities. If you can't argue why a move
    is safe, two pointers might not apply.
"""

"""
BINARY SEARCH — Two Templates That Cover Everything
=====================================================

WHEN TO USE:
  - Sorted array + find something → binary search
  - "Minimum value that satisfies condition" → binary search on answer
  - "Maximum value that satisfies condition" → binary search on answer

MENTAL MODEL:
  You have a sorted space. You cut it in half each time.
  Left half has one property, right half has another.
  You're finding the BOUNDARY between them.

  [F F F F F T T T T T]
                ^
          find this boundary
"""


# ============================================================
# TEMPLATE 1: Find exact target
# ============================================================
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1

    while lo <= hi:                    # <= because lo==hi is still valid
        mid = lo + (hi - lo) // 2     # avoid overflow (habit from other langs)

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1  # not found


# ============================================================
# TEMPLATE 2: Find boundary (leftmost True / insertion point)
# ============================================================
# This is the more powerful template. Covers most problems.
#
# Finds the FIRST position where condition(mid) is True:
#   [F F F F T T T T]
#             ^
def find_boundary(nums, target):
    lo, hi = 0, len(nums)             # hi = len(nums), NOT len-1

    while lo < hi:                     # < not <=
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:         # condition: "not yet reached target"
            lo = mid + 1
        else:
            hi = mid                   # NOT mid-1, mid could be the answer

    return lo  # lo == hi == first position where condition is True


# ============================================================
# EXAMPLE: Find Min in Rotated Sorted Array
# ============================================================
# [4, 5, 6, 7, 0, 1, 2]  → 0
# The min is the boundary between "rotated part" and "sorted part"

def findMin(nums):
    lo, hi = 0, len(nums) - 1

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > nums[hi]:       # mid is in the rotated part
            lo = mid + 1               # min is to the right
        else:
            hi = mid                   # mid could be the min

    return nums[lo]


# ============================================================
# EXAMPLE: Search in Rotated Sorted Array
# ============================================================
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2

        if nums[mid] == target:
            return mid

        # figure out which half is sorted
        if nums[lo] <= nums[mid]:      # left half is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1           # target is in sorted left half
            else:
                lo = mid + 1           # target is in right half
        else:                          # right half is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1           # target is in sorted right half
            else:
                hi = mid - 1           # target is in left half

    return -1


# ============================================================
# EXAMPLE: Binary Search on Answer — Koko Eating Bananas
# ============================================================
# "What is the minimum speed k such that Koko can eat all bananas in h hours?"
# Search space: k from 1 to max(piles)
# Condition: can_finish(k) → monotonic (once True, always True for bigger k)

import math

def minEatingSpeed(piles, h):
    lo, hi = 1, max(piles)

    while lo < hi:
        mid = lo + (hi - lo) // 2
        # can Koko finish at speed `mid`?
        hours_needed = sum(math.ceil(p / mid) for p in piles)

        if hours_needed <= h:
            hi = mid               # try slower speed
        else:
            lo = mid + 1           # too slow, go faster

    return lo


"""
DECISION GUIDE:

  "Find exact value"           → Template 1: while lo <= hi
  "Find first/last position"   → Template 2: while lo < hi, hi = mid
  "Find min/max that works"    → Template 2 on answer space

  Common gotcha:
    while lo <= hi  →  hi = mid - 1  (shrink both sides)
    while lo < hi   →  hi = mid      (hi could be the answer)

  Binary search on answer pattern:
    1. Define the search space [lo, hi]
    2. Write a can_do(mid) function
    3. Binary search for the boundary
"""

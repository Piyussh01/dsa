"""
SLIDING WINDOW — Two Flavors
==============================

WHEN TO USE:
  - Contiguous subarray/substring
  - "Maximum/minimum sum of size k"
  - "Longest/shortest substring with condition"
  - "Contains at most/at least K distinct"

MENTAL MODEL:
  You have a window [left, right] sliding across the array.
  Expand right to include more.
  Shrink left to fix violations.

  FIXED WINDOW:  window size is always K
  VARIABLE WINDOW: expand until invalid, shrink until valid again
"""

from collections import defaultdict


# ============================================================
# FIXED WINDOW — window size is always K
# ============================================================
def maxSumSubarray(nums, k):
    # Sum of first window
    window_sum = sum(nums[:k])
    max_sum = window_sum

    # Slide: add right element, remove left element
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)

    return max_sum


# ============================================================
# VARIABLE WINDOW TEMPLATE — the universal one
# ============================================================
def variable_window_template(s):
    left = 0
    # state variables (counter, sum, set, dict, etc.)

    best = 0  # or float('inf') for minimum

    for right in range(len(s)):
        # 1. EXPAND: add s[right] to window state

        # 2. SHRINK: while window is INVALID, remove s[left]
        while window_is_invalid():
            # remove s[left] from window state
            left += 1

        # 3. UPDATE answer (window is now valid)
        best = max(best, right - left + 1)  # or min for shortest

    return best

def window_is_invalid():
    pass  # placeholder


# ============================================================
# EXAMPLE: Longest Substring Without Repeating Characters
# ============================================================
def lengthOfLongestSubstring(s):
    seen = set()
    left = 0
    best = 0

    for right in range(len(s)):
        # SHRINK while we have a duplicate
        while s[right] in seen:
            seen.remove(s[left])
            left += 1

        # EXPAND
        seen.add(s[right])
        best = max(best, right - left + 1)

    return best

# "abcabcbb" → 3 ("abc")


# ============================================================
# EXAMPLE: Minimum Window Substring
# ============================================================
# Find shortest substring of s containing all chars of t
def minWindow(s, t):
    if not t or not s:
        return ""

    need = defaultdict(int)
    for c in t:
        need[c] += 1

    have = 0
    required = len(need)  # number of unique chars we need
    window = defaultdict(int)

    best = (float('inf'), 0, 0)  # (length, left, right)
    left = 0

    for right in range(len(s)):
        # EXPAND
        c = s[right]
        window[c] += 1
        if window[c] == need[c]:
            have += 1

        # SHRINK while window is valid (we have everything)
        while have == required:
            # update answer
            if (right - left + 1) < best[0]:
                best = (right - left + 1, left, right)

            # remove left
            window[s[left]] -= 1
            if s[left] in need and window[s[left]] < need[s[left]]:
                have -= 1
            left += 1

    length, l, r = best
    return s[l:r + 1] if length != float('inf') else ""


# ============================================================
# EXAMPLE: Best Time to Buy and Sell Stock
# ============================================================
# This is a simplified sliding window / two pointer
def maxProfit(prices):
    min_price = float('inf')
    max_profit = 0

    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)

    return max_profit


"""
PATTERN RECOGNITION:

  Fixed window size K:
    - Initialize window of size K
    - Slide: add right, remove left
    - O(n) time

  Variable window:
    for right in range(n):
        add s[right]
        while invalid:
            remove s[left]
            left += 1
        update answer

  Common state trackers:
    - set()          → track unique elements
    - defaultdict()  → track character frequencies
    - int            → track running sum
"""

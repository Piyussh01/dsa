"""
DYNAMIC PROGRAMMING — How to Spot It, How to Solve It
=======================================================

WHEN TO USE:
  - "Count the number of ways"
  - "What is the minimum/maximum cost"
  - "Can you reach / is it possible"
  - Optimal substructure + overlapping subproblems

MENTAL MODEL:
  DP = recursion + memoization  (or build table bottom-up)

  RECIPE:
    1. Define STATE: what info do I need to know my position in the problem?
    2. Define TRANSITION: how do I get to this state from smaller states?
    3. Define BASE CASE: what's the answer for the smallest input?
    4. Define ANSWER: which state gives the final answer?

  Start with recursion → add memo → convert to table if needed.
"""


# ============================================================
# 1D DP — Climbing Stairs (the hello world of DP)
# ============================================================
# "How many ways to reach step n, taking 1 or 2 steps at a time?"
# State: dp[i] = number of ways to reach step i
# Transition: dp[i] = dp[i-1] + dp[i-2]  (come from 1 step back or 2 steps back)

def climbStairs(n):
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for i in range(3, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    return prev1

# dp[1]=1, dp[2]=2, dp[3]=3, dp[4]=5, dp[5]=8  (it's Fibonacci!)


# ============================================================
# HOUSE ROBBER — can't rob two adjacent houses
# ============================================================
# State: dp[i] = max money robbing houses 0..i
# Transition: dp[i] = max(dp[i-1], dp[i-2] + nums[i])
#   either skip house i (take dp[i-1])
#   or rob house i (take dp[i-2] + nums[i])

def rob(nums):
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    prev2, prev1 = 0, 0
    for num in nums:
        curr = max(prev1, prev2 + num)
        prev2 = prev1
        prev1 = curr
    return prev1


# ============================================================
# COIN CHANGE — minimum coins to make amount
# ============================================================
# State: dp[amount] = min coins needed
# Transition: dp[a] = min(dp[a - coin] + 1) for each coin

def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], dp[a - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


# ============================================================
# LONGEST INCREASING SUBSEQUENCE
# ============================================================
# State: dp[i] = length of LIS ending at index i
# Transition: dp[i] = max(dp[j] + 1) for all j < i where nums[j] < nums[i]

def lengthOfLIS(nums):
    n = len(nums)
    dp = [1] * n  # every element is a subsequence of length 1

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)

# O(n^2). There's an O(n log n) version with binary search.


# ============================================================
# 2D DP — Unique Paths (grid problems)
# ============================================================
# State: dp[r][c] = number of ways to reach cell (r, c)
# Transition: dp[r][c] = dp[r-1][c] + dp[r][c-1]  (from above + from left)

def uniquePaths(m, n):
    dp = [[1] * n for _ in range(m)]

    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]

    return dp[m - 1][n - 1]


# ============================================================
# LONGEST COMMON SUBSEQUENCE — classic 2D DP
# ============================================================
# State: dp[i][j] = LCS of text1[:i] and text2[:j]
# Transition:
#   if text1[i-1] == text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
#   else:                         dp[i][j] = max(dp[i-1][j], dp[i][j-1])

def longestCommonSubsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


# ============================================================
# WORD BREAK — can string be segmented into dictionary words?
# ============================================================
# State: dp[i] = can s[:i] be broken into words?
# Transition: dp[i] = True if any dp[j] is True AND s[j:i] is in wordDict

def wordBreak(s, wordDict):
    words = set(wordDict)
    dp = [False] * (len(s) + 1)
    dp[0] = True

    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break

    return dp[len(s)]


# ============================================================
# MAXIMUM SUBARRAY (Kadane's Algorithm)
# ============================================================
# Not classical DP table, but same idea: "best ending at index i"
def maxSubArray(nums):
    max_sum = nums[0]
    current = nums[0]

    for i in range(1, len(nums)):
        current = max(nums[i], current + nums[i])  # restart or extend
        max_sum = max(max_sum, current)

    return max_sum


"""
DP RECOGNITION GUIDE:

  "How many ways?"          → count DP (climbing stairs, unique paths)
  "Min/max cost?"           → optimization DP (coin change, house robber)
  "Is it possible?"         → boolean DP (word break, can partition?)
  "Longest/shortest ___?"   → optimization DP (LIS, LCS)

  1D DP: state depends on previous 1-2 values → can optimize to O(1) space
  2D DP: state depends on two dimensions (two strings, grid)

  APPROACH:
    1. Write recursive solution first (top-down)
    2. Add memoization (@cache or dict)
    3. Convert to iterative if needed (bottom-up table)

  SPACE OPTIMIZATION:
    If dp[i] only depends on dp[i-1] and dp[i-2] → use two variables
    If dp[i][j] only depends on dp[i-1][j] → use 1D array
"""

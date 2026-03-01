"""
PERMUTATIONS & COMBINATIONS — Same Skeleton, Different Rules
=============================================================

MENTAL MODEL:
  SUBSETS     = pick any number of items, ORDER DOESN'T MATTER → use start index
  COMBINATIONS = pick exactly K items, ORDER DOESN'T MATTER   → use start index + length check
  PERMUTATIONS = pick all items, ORDER MATTERS                 → use "used" set, restart from 0

  Think of it as:
    Subsets:      "which items do I include?"     → each item: yes/no
    Combinations: "which K items do I include?"   → same but stop at K
    Permutations: "in what order do I place them?" → try every unused item at each slot
"""

# ============================================================
# SUBSETS — every intermediate state is a valid answer
# ============================================================
def subsets(nums):
    result = []
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return result

# subsets([1,2,3]) → [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]


# ============================================================
# SUBSETS II — with duplicates. Sort first, skip same element.
# ============================================================
def subsetsWithDup(nums):
    nums.sort()  # MUST sort to group duplicates
    result = []
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:  # skip duplicate at same level
                continue
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return result


# ============================================================
# COMBINATIONS — pick exactly K items from 1..N
# ============================================================
def combine(n, k):
    result = []
    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
    backtrack(1, [])
    return result

# combine(4, 2) → [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]


# ============================================================
# PERMUTATIONS — order matters, try all unused at each position
# ============================================================
def permute(nums):
    result = []
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):       # start from 0 every time!
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False
    backtrack([], [False] * len(nums))
    return result

# permute([1,2,3]) → [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]


# ============================================================
# PERMUTATIONS II — with duplicates
# ============================================================
def permuteUnique(nums):
    nums.sort()  # sort to group duplicates
    result = []
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            # skip duplicate: same value as previous AND previous not used at this level
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False
    backtrack([], [False] * len(nums))
    return result


"""
CHEAT SHEET:

  Problem        | Loop start | Recurse with | Dedup?
  ─────────────────────────────────────────────────────────
  Subsets        | start      | i + 1        | No
  Subsets II     | start      | i + 1        | sort + skip
  Combinations   | start      | i + 1        | No
  Combo Sum      | start      | i (reuse)    | No
  Combo Sum II   | start      | i + 1        | sort + skip
  Permutations   | 0          | 0 + used[]   | No
  Permutations II| 0          | 0 + used[]   | sort + skip

  The DEDUP trick is always the same:
    1. Sort the input
    2. if i > start and nums[i] == nums[i-1]: continue  (for combos/subsets)
       if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue  (for perms)
"""

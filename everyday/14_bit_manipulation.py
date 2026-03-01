"""
BIT MANIPULATION — XOR Tricks & Bitmask Subsets
=================================================

WHEN TO USE:
  - "Single number" problems (find the odd one out)
  - "Count bits" / "power of two"
  - Generate subsets using bitmask
  - Space optimization (store boolean states as bits)

MENTAL MODEL:
  Every integer is a sequence of bits: 5 = 101, 6 = 110
  Bitwise operations compare/combine them bit by bit.

  KEY OPERATIONS:
    AND  (&)  : 1 only if BOTH are 1       → 101 & 110 = 100
    OR   (|)  : 1 if EITHER is 1           → 101 | 110 = 111
    XOR  (^)  : 1 if DIFFERENT              → 101 ^ 110 = 011
    NOT  (~)  : flip all bits               → ~101 = ...010
    LEFT SHIFT  (<<) : multiply by 2        → 101 << 1 = 1010
    RIGHT SHIFT (>>) : divide by 2          → 101 >> 1 = 10
"""


# ============================================================
# XOR TRICKS
# ============================================================

# Single Number: every element appears twice except one. Find it.
# XOR cancels pairs: a ^ a = 0, a ^ 0 = a
def singleNumber(nums):
    result = 0
    for num in nums:
        result ^= num
    return result

# [4, 1, 2, 1, 2] → 4^1^2^1^2 = 4^(1^1)^(2^2) = 4^0^0 = 4


# ============================================================
# BIT COUNTING
# ============================================================

# Number of 1 bits (Hamming weight)
def hammingWeight(n):
    count = 0
    while n:
        count += n & 1    # check last bit
        n >>= 1           # shift right
    return count

# Brian Kernighan's trick: n & (n-1) removes the lowest set bit
def hammingWeight_fast(n):
    count = 0
    while n:
        n &= (n - 1)     # remove lowest 1-bit
        count += 1
    return count

# 12 = 1100 → 1100 & 1011 = 1000 → 1000 & 0111 = 0000 → count = 2


# Power of Two: exactly one bit set
def isPowerOfTwo(n):
    return n > 0 and (n & (n - 1)) == 0
# 8 = 1000 → 1000 & 0111 = 0 ✓
# 6 = 0110 → 0110 & 0101 = 0100 ≠ 0 ✗


# ============================================================
# BITMASK SUBSETS — generate all subsets using bits
# ============================================================
# For n items, iterate from 0 to 2^n - 1
# Each number's bits represent which items to include

def subsets_bitmask(nums):
    n = len(nums)
    result = []

    for mask in range(1 << n):        # 0 to 2^n - 1
        subset = []
        for i in range(n):
            if mask & (1 << i):       # is bit i set?
                subset.append(nums[i])
        result.append(subset)

    return result

# nums = [a, b, c]
# mask=000 → []        mask=100 → [c]
# mask=001 → [a]       mask=101 → [a, c]
# mask=010 → [b]       mask=110 → [b, c]
# mask=011 → [a, b]    mask=111 → [a, b, c]


# ============================================================
# MISSING NUMBER — XOR or math trick
# ============================================================
def missingNumber(nums):
    n = len(nums)
    # XOR all indices and all values — duplicates cancel
    result = n
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result

# Or simply: return n*(n+1)//2 - sum(nums)


# ============================================================
# REVERSE BITS
# ============================================================
def reverseBits(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)  # shift result left, add last bit of n
        n >>= 1
    return result


"""
BIT TRICKS CHEAT SHEET:

  n & (n - 1)     → remove lowest set bit
  n & (-n)        → isolate lowest set bit
  n | (n - 1)     → fill lowest unset bit and below
  n ^ n = 0       → XOR with self cancels
  n ^ 0 = n       → XOR with 0 is identity
  1 << k          → 2^k (set kth bit)
  n & (1 << k)    → check if kth bit is set
  n | (1 << k)    → set kth bit
  n & ~(1 << k)   → clear kth bit
  n ^ (1 << k)    → toggle kth bit

PATTERN RECOGNITION:
  "Find the unique element"     → XOR everything
  "Count 1s / is power of 2"   → n & (n-1)
  "Generate all subsets"        → bitmask 0 to 2^n
  "Store boolean states"        → use bits as flags
"""

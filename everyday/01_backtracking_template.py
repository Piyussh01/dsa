"""
BACKTRACKING — The One Pattern
===============================

WHEN TO USE:
  - "Generate all ___"  (all permutations, all paths, all valid IPs)
  - "Find all ___"       (all subsets, all combinations)
  - "Can you place ___"  (N-queens, sudoku)

MENTAL MODEL:
  You're exploring a TREE of choices.
  At each node, you CHOOSE → EXPLORE → UNCHOOSE.

  Think of it like filling boxes left to right:
    Box 1: try 'a', try 'b', try 'c' ...
    Box 2: try 'a', try 'b', try 'c' ...
    ...

  If a choice leads to a dead end → undo it (backtrack) → try next.

THE SKELETON:
"""

def backtrack(result, current, choices, start):
    # 1. BASE CASE: when is `current` a complete answer?
    if is_complete(current):
        result.append(current[:])  # COPY! Don't append the reference
        return

    # 2. LOOP through remaining choices
    for i in range(start, len(choices)):
        # 3. SKIP invalid choices (pruning)
        if not is_valid(choices[i]):
            continue

        # 4. CHOOSE
        current.append(choices[i])

        # 5. EXPLORE (recurse deeper)
        backtrack(result, current, choices, i + 1)  # i+1 for combos, i for reuse, 0 for perms

        # 6. UNCHOOSE (backtrack)
        current.pop()

def is_complete(current):
    pass  # define when a solution is ready

def is_valid(choice):
    return True  # define constraints


"""
=== EXAMPLE 1: Restore IP Addresses (the problem you were stuck on) ===

Think of it as: place 3 dots in a string to make 4 valid segments.
Each segment: 1-3 digits, value 0-255, no leading zeros.

Choices at each step: take 1 digit, 2 digits, or 3 digits.
"""

def restoreIpAddresses(s: str) -> list[str]:
    result = []

    def backtrack(start, segments):
        # BASE: 4 segments and we've used all characters
        if len(segments) == 4 and start == len(s):
            result.append(".".join(segments))
            return

        # PRUNE: 4 segments but chars remaining, or not enough chars left
        if len(segments) == 4:
            return

        # TRY taking 1, 2, or 3 characters
        for length in range(1, 4):
            if start + length > len(s):
                break

            segment = s[start:start + length]

            # VALIDATE: no leading zeros, value <= 255
            if len(segment) > 1 and segment[0] == '0':
                break  # "01", "001" invalid — break, not continue
            if int(segment) > 255:
                break

            # CHOOSE + EXPLORE + UNCHOOSE
            segments.append(segment)
            backtrack(start + length, segments)
            segments.pop()

    backtrack(0, [])
    return result

# restoreIpAddresses("25525511135")
# → ["255.255.11.135", "255.255.111.35"]


"""
=== EXAMPLE 2: Subsets ===

Given [1,2,3], return all subsets: [[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]]

Simplest backtracking: at each position, include or skip.
"""

def subsets(nums: list[int]) -> list[list[int]]:
    result = []

    def backtrack(start, current):
        result.append(current[:])  # every partial state is valid

        for i in range(start, len(nums)):
            current.append(nums[i])       # CHOOSE
            backtrack(i + 1, current)      # EXPLORE
            current.pop()                  # UNCHOOSE

    backtrack(0, [])
    return result


"""
=== EXAMPLE 3: Combination Sum ===

Find all combos in [2,3,6,7] that sum to 7.
Same element CAN be reused → pass `i` not `i+1`.
"""

def combinationSum(candidates: list[int], target: int) -> list[list[int]]:
    result = []

    def backtrack(start, current, remaining):
        if remaining == 0:
            result.append(current[:])
            return
        if remaining < 0:
            return

        for i in range(start, len(candidates)):
            current.append(candidates[i])
            backtrack(i, current, remaining - candidates[i])  # i, not i+1 → reuse allowed
            current.pop()

    backtrack(0, [], target)
    return result


"""
KEY INSIGHT — the only thing that changes between problems:

  | Problem           | start param | base case              | pruning            |
  |-------------------|-------------|------------------------|--------------------|
  | Subsets           | i + 1       | always valid           | none               |
  | Combinations      | i + 1       | len == k               | len > k            |
  | Combination Sum   | i (reuse)   | remaining == 0         | remaining < 0      |
  | Permutations      | 0 (any pos) | len == n               | already used       |
  | IP Addresses      | start+len   | 4 segments + end       | >255, leading 0    |
  | Palindrome Parttn | i + 1       | start == end           | not palindrome     |
  | N-Queens          | row + 1     | row == n               | col/diag conflict  |

That's it. Same skeleton. Different constraints.
"""

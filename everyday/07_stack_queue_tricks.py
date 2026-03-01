"""
STACK & QUEUE TRICKS
=====================

MENTAL MODEL:
  STACK = pile of plates (LIFO) → last in, first out → list with .append() / .pop()
  QUEUE = line at store (FIFO) → first in, first out → deque with .append() / .popleft()

  Stack from 2 Queues:  push to q1, pop by moving all-but-last to q2
  Queue from 2 Stacks:  push to s1, pop by flipping s1 into s2
  Monotonic Stack:      keep stack always increasing or decreasing → "next greater element"
"""

from collections import deque


# ============================================================
# QUEUE FROM TWO STACKS — O(1) amortized pop
# ============================================================
# WHY: stack is LIFO, but if you pour stack1 into stack2, order reverses → FIFO!

class MyQueue:
    def __init__(self):
        self.push_stack = []    # new elements go here
        self.pop_stack = []     # reversed elements come here

    def push(self, x):
        self.push_stack.append(x)

    def pop(self):
        self._move()
        return self.pop_stack.pop()

    def peek(self):
        self._move()
        return self.pop_stack[-1]

    def empty(self):
        return not self.push_stack and not self.pop_stack

    def _move(self):
        # only move when pop_stack is empty
        if not self.pop_stack:
            while self.push_stack:
                self.pop_stack.append(self.push_stack.pop())

# push 1,2,3 → push_stack = [1,2,3]
# pop → move to pop_stack = [3,2,1] → pop → 1 ✓ (FIFO!)


# ============================================================
# STACK FROM TWO QUEUES — O(n) push, O(1) pop
# ============================================================
class MyStack:
    def __init__(self):
        self.q = deque()

    def push(self, x):
        self.q.append(x)
        # rotate so the new element is at the front
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())

    def pop(self):
        return self.q.popleft()

    def top(self):
        return self.q[0]

    def empty(self):
        return len(self.q) == 0

# push 1 → [1]
# push 2 → [2,1]  (rotate: [1,2] → move 1 to back → [2,1])
# push 3 → [3,2,1]
# pop → 3 ✓ (LIFO!)


# ============================================================
# MONOTONIC STACK — "Next Greater Element" pattern
# ============================================================
# MENTAL MODEL:
#   Walk left to right. Stack holds INDICES of elements waiting
#   for their "next greater". When we find a bigger element,
#   pop everyone smaller — they found their answer.

def nextGreaterElement(nums):
    n = len(nums)
    result = [-1] * n
    stack = []  # stores indices

    for i in range(n):
        # pop everything smaller than current
        while stack and nums[stack[-1]] < nums[i]:
            idx = stack.pop()
            result[idx] = nums[i]

        stack.append(i)

    return result

# nums =  [2, 1, 2, 4, 3]
# result = [4, 2, 4,-1,-1]
#           ^  ^  ^
#           2→4, 1→2, 2→4  (next element greater than me)


# Daily Temperatures — same pattern, find "days until warmer"
def dailyTemperatures(temperatures):
    n = len(temperatures)
    result = [0] * n
    stack = []

    for i in range(n):
        while stack and temperatures[stack[-1]] < temperatures[i]:
            idx = stack.pop()
            result[idx] = i - idx  # distance, not value
        stack.append(i)

    return result


# ============================================================
# VALID PARENTHESES — classic stack problem
# ============================================================
def isValid(s):
    stack = []
    matching = {')': '(', ']': '[', '}': '{'}

    for c in s:
        if c in matching:                    # closing bracket
            if not stack or stack[-1] != matching[c]:
                return False
            stack.pop()
        else:                                # opening bracket
            stack.append(c)

    return len(stack) == 0


# ============================================================
# MIN STACK — stack that tracks minimum in O(1)
# ============================================================
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []  # parallel stack tracking minimums

    def push(self, val):
        self.stack.append(val)
        # push to min_stack if val is <= current min
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self):
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]


"""
PATTERN RECOGNITION:

  "Next greater/smaller element"  → Monotonic stack
  "Valid brackets/parentheses"    → Stack (match open/close)
  "Min/Max in constant time"      → Two stacks (data + extremes)
  "Process in FIFO order"         → Queue (or 2 stacks)
  "Undo last operation"           → Stack

  MONOTONIC STACK VARIANTS:
    Increasing stack → finds next GREATER element
    Decreasing stack → finds next SMALLER element
    (flip the comparison in the while condition)
"""

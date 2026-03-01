"""
HEAP & GREEDY — Top-K, Merge-K, Intervals
============================================

MENTAL MODEL:
  HEAP (Priority Queue) = always gives you the min (or max) in O(log n)
  Python's heapq is a MIN heap. For MAX heap → negate values.

  GREEDY = make the locally optimal choice at each step.
  Works when: local optimum leads to global optimum (intervals, scheduling).

  WHEN TO USE HEAP:
    "Kth largest/smallest"
    "Merge K sorted things"
    "Top K frequent"
    "Continuously find min/max"
"""

import heapq
from collections import Counter


# ============================================================
# TOP K FREQUENT ELEMENTS
# ============================================================
def topKFrequent(nums, k):
    count = Counter(nums)
    # nlargest uses a min-heap of size k internally → O(n log k)
    return heapq.nlargest(k, count.keys(), key=count.get)

# Or bucket sort approach (O(n)):
def topKFrequent_bucket(nums, k):
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)

    result = []
    for i in range(len(buckets) - 1, -1, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result


# ============================================================
# KTH LARGEST ELEMENT
# ============================================================
# Min heap of size K: the root is the Kth largest
def findKthLargest(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)

    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)  # pop min, push new

    return heap[0]


# ============================================================
# MERGE K SORTED LISTS
# ============================================================
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeKLists(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode(0)
    curr = dummy

    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next


# ============================================================
# MEDIAN FROM DATA STREAM — two heaps
# ============================================================
# Max heap for lower half, min heap for upper half
class MedianFinder:
    def __init__(self):
        self.lo = []   # max heap (negate values)
        self.hi = []   # min heap

    def addNum(self, num):
        heapq.heappush(self.lo, -num)
        # move largest of lo to hi
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        # balance: lo can have at most 1 more than hi
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2


# ============================================================
# GREEDY: MERGE INTERVALS
# ============================================================
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:       # overlapping
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged


# ============================================================
# GREEDY: JUMP GAME
# ============================================================
# Can you reach the last index?
def canJump(nums):
    farthest = 0
    for i in range(len(nums)):
        if i > farthest:
            return False
        farthest = max(farthest, i + nums[i])
    return True


# ============================================================
# GREEDY: NON-OVERLAPPING INTERVALS (min removals)
# ============================================================
def eraseOverlapIntervals(intervals):
    intervals.sort(key=lambda x: x[1])  # sort by END time
    removals = 0
    prev_end = float('-inf')

    for start, end in intervals:
        if start >= prev_end:
            prev_end = end       # no overlap, keep it
        else:
            removals += 1        # overlap, remove (the one with later end)

    return removals


"""
HEAP CHEAT SHEET:

  import heapq
  heapq.heappush(heap, val)      # push
  heapq.heappop(heap)            # pop min
  heapq.heapify(list)            # make list a heap in O(n)
  heapq.nlargest(k, iterable)    # top K
  heapq.nsmallest(k, iterable)   # bottom K

  MAX HEAP trick: push/pop with negated values
    heapq.heappush(heap, -val)
    -heapq.heappop(heap)

GREEDY PATTERN RECOGNITION:

  Intervals:
    Sort by START → merge overlapping
    Sort by END   → max non-overlapping (activity selection)

  Greedy works when:
    "Take the best available option" always leads to the optimal answer.
    If you're not sure → try DP instead.
"""

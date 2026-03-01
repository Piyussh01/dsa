"""
LINKED LIST — The 3 Core Moves
================================

MENTAL MODEL:
  A linked list is a chain of nodes: [1] → [2] → [3] → None
  You can only go FORWARD (singly linked).

  Three moves solve 90% of linked list problems:
    1. REVERSE — flip the arrows
    2. FAST/SLOW — find middle, detect cycle
    3. DUMMY HEAD — simplify edge cases (empty list, head changes)
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ============================================================
# MOVE 1: REVERSE a linked list
# ============================================================
# Think of it as: for each node, point it BACKWARD instead of forward.

def reverseList(head):
    prev = None
    curr = head

    while curr:
        nxt = curr.next    # save next (before we break the link)
        curr.next = prev   # reverse the arrow
        prev = curr        # advance prev
        curr = nxt         # advance curr

    return prev            # prev is the new head

# Before: 1 → 2 → 3 → None
#   Step: None ← 1    2 → 3 → None   (prev=1, curr=2)
#   Step: None ← 1 ← 2    3 → None   (prev=2, curr=3)
#   Step: None ← 1 ← 2 ← 3           (prev=3, curr=None)
# Return prev = 3


# ============================================================
# MOVE 2: FAST & SLOW — find middle
# ============================================================
def middleNode(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow  # slow is at the middle

# 1 → 2 → 3 → 4 → 5
#          ^       ^
#         slow    fast  → slow is middle


# ============================================================
# MOVE 3: DUMMY HEAD — avoids "if head is None" edge cases
# ============================================================

# Merge Two Sorted Lists
def mergeTwoLists(l1, l2):
    dummy = ListNode(0)       # fake head — we return dummy.next at the end
    curr = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next

    curr.next = l1 or l2      # attach remaining
    return dummy.next


# ============================================================
# COMBINED: Reorder List  [1,2,3,4,5] → [1,5,2,4,3]
# ============================================================
# Step 1: Find middle (fast/slow)
# Step 2: Reverse second half
# Step 3: Merge two halves alternating

def reorderList(head):
    if not head or not head.next:
        return

    # 1. Find middle
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # 2. Reverse second half
    second = slow.next
    slow.next = None           # cut the list
    prev = None
    while second:
        nxt = second.next
        second.next = prev
        prev = second
        second = nxt
    second = prev

    # 3. Merge alternating
    first = head
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first = tmp1
        second = tmp2


# ============================================================
# Remove Nth Node From End — fast gets N head start
# ============================================================
def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy

    # advance fast by n+1 steps
    for _ in range(n + 1):
        fast = fast.next

    # move both until fast hits end
    while fast:
        slow = slow.next
        fast = fast.next

    # slow is right before the node to remove
    slow.next = slow.next.next
    return dummy.next


"""
CHEAT SHEET:

  Reverse:     prev, curr, nxt pattern — 3 pointers
  Middle:      slow (1x speed), fast (2x speed)
  Cycle:       same as middle — if they meet, cycle exists
  Merge:       dummy head + compare + attach remaining
  Remove Nth:  fast gets N step head start, then move together

  ALWAYS consider using a dummy head when:
    - The head might change
    - You're building a new list
    - Edge cases with empty list are annoying
"""

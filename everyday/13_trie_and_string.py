"""
TRIE & STRING PATTERNS
========================

WHEN TO USE TRIE:
  - "Autocomplete / prefix search"
  - "Word search in a board" (Word Search II)
  - "Count words with prefix"
  - Multiple string lookups with shared prefixes

MENTAL MODEL:
  A trie is a tree where each edge is a CHARACTER.
  Walking from root to a node spells out a PREFIX.
  Nodes marked as "end" represent complete WORDS.

       root
      / | \
     a  b  c
     |     |
     p     a
    / \    |
   p   e   t    ← "app", "ape", "cat" are words
   |
   l
   e             ← "apple" is a word
"""


# ============================================================
# TRIE IMPLEMENTATION
# ============================================================
class TrieNode:
    def __init__(self):
        self.children = {}     # char → TrieNode
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    def search(self, word):
        node = self._find(word)
        return node is not None and node.is_end

    def startsWith(self, prefix):
        return self._find(prefix) is not None

    def _find(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node.children:
                return None
            node = node.children[c]
        return node


# ============================================================
# WORD SEARCH II — Trie + Backtracking on grid
# ============================================================
# Insert all words into trie, then DFS from each cell
def findWords(board, words):
    trie = Trie()
    for w in words:
        trie.insert(w)

    rows, cols = len(board), len(board[0])
    result = set()

    def dfs(r, c, node, path):
        if node.is_end:
            result.add(path)
            node.is_end = False  # avoid duplicates

        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        char = board[r][c]
        if char not in node.children:
            return

        board[r][c] = '#'  # mark visited
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            dfs(r + dr, c + dc, node.children[char], path + char)
        board[r][c] = char  # unmark

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie.root, "")

    return list(result)


# ============================================================
# STRING PATTERN: Palindrome Check
# ============================================================
def isPalindrome(s, lo, hi):
    while lo < hi:
        if s[lo] != s[hi]:
            return False
        lo += 1
        hi -= 1
    return True


# ============================================================
# STRING PATTERN: Palindrome Partitioning (Backtracking)
# ============================================================
# Partition string so every part is a palindrome
def partition(s):
    result = []

    def backtrack(start, path):
        if start == len(s):
            result.append(path[:])
            return

        for end in range(start + 1, len(s) + 1):
            substring = s[start:end]
            if substring == substring[::-1]:     # is palindrome?
                path.append(substring)
                backtrack(end, path)
                path.pop()

    backtrack(0, [])
    return result

# "aab" → [["a","a","b"], ["aa","b"]]


# ============================================================
# STRING PATTERN: Group Anagrams
# ============================================================
from collections import defaultdict

def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))    # sorted string as key
        groups[key].append(s)
    return list(groups.values())

# Or use character count as key (faster for long strings):
def groupAnagrams_v2(strs):
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        groups[tuple(count)].append(s)
    return list(groups.values())


# ============================================================
# STRING PATTERN: Longest Palindromic Substring
# ============================================================
# Expand around center — every palindrome has a center
def longestPalindrome(s):
    result = ""

    def expand(l, r):
        nonlocal result
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if r - l + 1 > len(result):
                result = s[l:r + 1]
            l -= 1
            r += 1

    for i in range(len(s)):
        expand(i, i)       # odd length palindrome
        expand(i, i + 1)   # even length palindrome

    return result


"""
TRIE vs HASHSET:
  Use HashSet when: exact match only, no prefix queries
  Use Trie when:    prefix queries, autocomplete, multiple word search

STRING TRICKS:
  Anagram?         → sorted(s) == sorted(t)  or  Counter(s) == Counter(t)
  Palindrome?      → s == s[::-1]  or  two pointer expand from center
  Substring search → sliding window + hashmap
  All partitions   → backtracking
"""

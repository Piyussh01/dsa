class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        n = len(haystack)
        m = len(needle)
        if n < m: return -1
        for i in range(n):
            if haystack[i:i+(m)] == needle:
                return i
        return -1
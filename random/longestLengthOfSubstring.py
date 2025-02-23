class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last = {}
        maxL = 0
        l = 0

        for r, char in enumerate(s):
            if char in last and last[char] >= l:
                l = last[char] + 1
            last[char] = r
            maxL = max(maxL, r - l + 1)

        return maxL


class Solution:
    def getLargestOutlier(self, nums: List[int]) -> int:
        # sum * 2 + outlier 
        T = sum(nums)
        freq = Counter(nums)

        cOutlier = []

        for S in freq:
            O = T - 2 * S
            if O in freq:
                if O == S and freq[S] < 2:
                    continue
                cOutlier.append(O)
        return max(cOutlier) if cOutlier else -1

#time O(n)
# space is O(n) worst case
        

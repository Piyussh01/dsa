class Solution:
    def totalStrength(self, strength: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(strength)
        
        # Compute prefix sum: prefix[i] = sum(strength[0:i])
        prefix = [0] * (n + 1)
        for i, x in enumerate(strength):
            prefix[i+1] = (prefix[i] + x) % MOD
            
        # Compute prefix2: prefix2[i] = sum(prefix[0:i])
        prefix2 = [0] * (n + 2)
        for i in range(n+1):
            prefix2[i+1] = (prefix2[i] + prefix[i]) % MOD
        
        # For each index i, we need to find:
        #   l = index of previous element that is strictly less than strength[i] (or -1 if none)
        #   r = index of next element that is strictly less than strength[i] (or n if none)
        left = [-1] * n
        right = [n] * n
        stack = []
        # Find previous less element for every index.
        for i, x in enumerate(strength):
            while stack and strength[stack[-1]] >= x:
                stack.pop()
            left[i] = stack[-1] if stack else -1
            stack.append(i)
        
        stack = []
        # Find next less element for every index.
        for i in range(n-1, -1, -1):
            while stack and strength[stack[-1]] > strength[i]:
                stack.pop()
            right[i] = stack[-1] if stack else n
            stack.append(i)
        
        total = 0
        # Calculate each index's contribution.
        for i, x in enumerate(strength):
            l = left[i]
            r = right[i]
            # The sum of all subarray sums (of prefix sums) for the interval [i, r-1] is:
            #   (prefix2[r+1] - prefix2[i+1]) mod MOD
            # Similarly, for the interval [l+1, i-1]:
            #   (prefix2[i+1] - prefix2[l+1]) mod MOD
            #
            # The contribution of strength[i] as the minimum is given by:
            #   x * ( (i - l) * (prefix2[r+1] - prefix2[i+1]) - (r - i) * (prefix2[i+1] - prefix2[l+1]) )
            contrib = x * (((i - l) * ((prefix2[r+1] - prefix2[i+1]) % MOD) - 
                            (r - i) * ((prefix2[i+1] - prefix2[l+1]) % MOD)) % MOD) % MOD
            total = (total + contrib) % MOD
        
        return total
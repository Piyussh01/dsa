class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [amount + 1] * (amount + 1)
        dp[0] = 0 

        for i in range(1 , amount + 1):
            for coin in coins:
                if coin <= i:
                    dp[i] = min(dp[i], dp[i - coin] + 1)
        
        return dp[amount] if dp[amount] != amount + 1 else -1


# Walkthrough
# 	1.	DP Array Initialization:
# 	•	We create an array dp of size amount + 1 where each element is initially set to amount + 1. This represents an “impossible” value.
# 	•	We set dp[0] = 0 because no coins are needed to form the amount 0.
# 	2.	Filling the DP Array:
# 	•	For each amount i from 1 to amount, we try every coin:
# 	•	Condition: If the coin value is less than or equal to i, it is a candidate.
# 	•	Transition: We update dp[i] as:

# dp[i] = \min(dp[i],\ dp[i - coin] + 1)

# This means: if we use the current coin, then we need 1 coin plus the minimum number of coins needed to form i - coin.
# 	•	We iterate over all coins for each i to compute the minimum coins needed.
# 	3.	Result Check:
# 	•	After filling the dp array, if dp[amount] is still amount + 1, it means the amount cannot be formed using the given coins, so we return -1.
# 	•	Otherwise, we return dp[amount], which is the fewest number of coins needed.


#     For coins = [1,2,5] and amount = 11:
# 	•	Initialization:
# dp is initialized as [0, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12] (since amount + 1 = 12).
# 	•	Iteration i = 1:
# 	•	Try coin 1: dp[1] = min(12, dp[0] + 1) = min(12, 0 + 1) = 1
# 	•	Coins 2 and 5 are too big.
# 	•	Now, dp[1] = 1.
# 	•	Iteration i = 2:
# 	•	For coin 1: dp[2] = min(12, dp[1] + 1) = min(12, 1 + 1) = 2
# 	•	For coin 2: dp[2] = min(2, dp[0] + 1) = min(2, 0 + 1) = 1
# 	•	Coin 5 is too big.
# 	•	Now, dp[2] = 1.
# 	•	… Continue this process until i = 11:
# 	•	Eventually, you’ll find that dp[11] = 3 (for example, using coins 5, 5, and 1).

# Thus, the minimum number of coins needed to form 11 is 3.
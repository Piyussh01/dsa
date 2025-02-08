# Amazon prime games is desinging a game. the player needs to pass n rounds sequentially in this  game. Rules of play are as follows 

# The player loses power[i] health to complete round i.
# the players health must be greater than 0 at all time. 

# player can choose to use armor in any one round. the armor will prevent damage of min(armor, power[i])

# determine the min starting health for the player to win the game

# eg power = [1,2,6,7]
# armor = 5

# give the player 12 units of health at the beginning of the game one of the optimal strategies is to use thhe armor in the third round and only lose 1 unit instead of 6. the health of the player after earch is 

# round health 

# 0 . 12 
# 1. 12 - power[0] = 12 -1 = 11
# 2. 11 - power[1] = 11 -2 =9
# 3. 9 - power[2] + armor = 9-6 + 5 =8 
# 4. 8 - power[3] = 8 -7 =1 

# Complete program in python to give best space and time complexity 

def getMinimumValue(power, armor):
    n = len(power)
    if n == 0:
        return 1 # that is there is no rounds 1 health is sufficient 
    
    prefix_sums = [0] * (n+1)
    for i in range(n):
        prefix_sums[i + 1] = prefix_sums[i] + power[i]
    
    total = prefix_sums[n] # cumalative of total damage
    print(total)

    minDamange = float('inf')
    for j in range(n):
        blocked = min(armor, power[j])
        peakDamage = max(prefix_sums[j], total - blocked)
        minDamange = min(minDamange, peakDamage)
    
    return minDamange + 1


if __name__ == "__main__":
    power = [1, 2, 6 , 7]
    power = power[::-1] # reversing a list
    print(power, "h")
    armor = 5 
    result = getMinimumValue(power, armor)
    print("result:", result)


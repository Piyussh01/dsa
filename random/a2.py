# SWE at Amazon are developing a new lib for NLP. In one modeule, every string needs to be preprocessed in a particular manner to find the length of its longest self sufficient proper substring. 

# A self sufficient proper substring is no where 
# 1. the substring is not the entire string s
# 2. no letter that occurs inside the substring also occurs outside the substring

# given the string fullString of length n , find the length of its longeest self-sufficeint proper substring. if none exists, return 0 

# Eg. fullString = "amazonservices"

# here the length fullString n = 14
# substring amazon length 6 is it self suffieicnet yes 
# services 8 yes
# azonse 6 no
# zonservices 11 yes since longest substring where no letter occurs both inside and outside the substring

# hence we return 11 as answer 

# complete this function in python to give best space and time complexity 
from collections import Counter
def findLongestLength(fullString):
    n = len(fullString)
    if n <= 1:
        return 0
    
    start = {chr(c): None for c in range(ord('a'), ord('z')+1)}
    end   = {chr(c): None for c in range(ord('a'), ord('z')+1)}
    
    for i, ch in enumerate(fullString):
        if start[ch] is None:
            start[ch] = i
        end[ch] = i
    print(start, "start")
    print(end, "end")

    intervals = []
    for c in start:
        if start[c] is not None:
            intervals.append([start[c], end[c]])
    print("i", intervals)
    
    intervals.sort(key=lambda x: x[0])
    print("as", intervals)

    # 3) Merge overlapping intervals
    merged = []
    for interval in intervals:
        if not merged or interval[0] > merged[-1][1]:
            # No overlap, add as a new interval
            print("h",interval)
            merged.append(interval)
            print("y",merged[-1][1])
            #print(interval[0])
        else:
            # Overlaps with the last interval in 'merged'; extend the last interval
            merged[-1][1] = max(merged[-1][1], interval[1])
            print(interval[1], "--", merged[-1][1])
    
    # 4) Pick a consecutive block of merged intervals to form [L, R],
    #    ensuring R-L+1 < n.
    max_len = 0
    m = len(merged)
    
    # For each consecutive subrange of merged
    for i in range(m):
        L = merged[i][0]
        current_end = merged[i][1]
        for j in range(i, m):
            # Extend the bounding box to include M_j
            current_end = max(current_end, merged[j][1])
            length = current_end - L + 1
            
            # Must be a proper substring => length < n
            if length < n:
                max_len = max(max_len, length)
            else:
                # If we've already reached the entire string length, no point checking further
                break
    
    return max_len

    

if __name__ == "__main__":
    test = "amazonservices"
    answer = findLongestLength(test)
    print("self longest", answer)


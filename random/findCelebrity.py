def findCelebrity(n):
    # Step 1: Find a potential candidate
    candidate = 0
    for i in range(1, n):
        if knows(candidate, i):
            candidate = i

    # Step 2: Verify the candidate
    for j in range(n):
        if j == candidate:
            continue
        # Candidate must not know j
        if knows(candidate, j):
            return -1
        # j must know candidate
        if not knows(j, candidate):
            return -1

    return candidate

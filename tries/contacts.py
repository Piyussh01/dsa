def contacts(queries):
    prefix_counts = {}
    result = []
    
    for query in queries:
        op, value = query[0], query[1]
        if op == 'add':
            for i in range(1, len(value)+1):
                prefix = value[:i]
                prefix_counts[prefix] = prefix_counts.get(prefix, 0) + 1
        elif op == 'find':
            result.append(prefix_counts.get(value, 0))
        
    return result

# Yes, that’s exactly the trade-off. The prefix dictionary (or Trie) method precomputes and stores additional data to make each find query extremely fast—typically O(1) or O(m) where m is the length of the search string. However, this comes at the cost of extra space to store counts for every prefix.

# On the other hand, if you choose to iterate over every contact during each find operation (i.e. checking if the contact starts with the given substring on the fly), you save space because you’re not storing extra prefix data. But then, each find operation becomes much slower—specifically, it takes O(N \cdot L) time per query, where N is the number of contacts and L is the average length of the contacts.

# In summary:
# 	•	Prefix Dictionary/Trie:
# 	•	Pros: Fast find queries.
# 	•	Cons: Uses extra memory.
# 	•	Naive Iteration:
# 	•	Pros: Minimal extra space.
# 	•	Cons: Potentially very slow when there are many contacts or many queries.

# So the choice depends on the problem constraints: if you expect a high volume of queries and many contacts, the extra space for precomputation is well worth it to maintain performance.

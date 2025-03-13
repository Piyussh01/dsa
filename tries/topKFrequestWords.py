from collections import defaultdict
import heapq
class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        cnt=defaultdict(lambda :[0,""])
        for i in words:
            cnt[i]=[cnt[i][0]-1,i]  # python automatically sorts words in lexicographically order
        lst=list(cnt.values())
        heapq.heapify(lst)
        lst=heapq.nsmallest(k,lst)
        ans=[]
        for i in lst:
            ans.append(i[1])
        return ans  

# This ensures that for words with the same frequency, the lexicographically larger word
# is considered "smaller" and gets removed first from the heap.
# class HeapItem:
#     def __init__(self, s: str) -> None:
#         self.s = s

#     def __lt__(self, other: "HeapItem") -> bool:
#         # Inverted comparison: return True if self.s is lexicographically greater than other.s.
#         return self.s > other.s

#     def __eq__(self, other: "HeapItem") -> bool:
#         # Check equality based on the underlying string.
#         return self.s == other.s

# class Solution:
#     def topKFrequent(self, words: List[str], k: int) -> List[str]:
#         # Count the frequency of each word in the list.
#         word_freq = Counter(words)

#         min_heap = []
        
#         # Build a min-heap of size k.
#         # Each heap element is a tuple: (frequency, custom HeapItem, word)
#         for word, freq in word_freq.items():
#             heapq.heappush(min_heap, (freq, HeapItem(word), word))
#             # Maintain the heap size to be at most k by popping the smallest element.
#             if len(min_heap) > k:
#                 heapq.heappop(min_heap)

#         result = []
#         # Extract words from the heap. They are in ascending order based on frequency and custom order.
#         while min_heap:
#             result.append(heapq.heappop(min_heap)[2])
        
#         # Reverse the result to get the most frequent words first.
#         return result[::-1]
from collections import deque

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        # If endWord not in wordList, no transformation is possible
        if endWord not in wordList:
            return 0
        
        # Convert wordList into a set for O(1) lookups
        word_set = set(wordList)
        
        # BFS queue: each element is (current_word, distance)
        queue = deque([(beginWord, 1)])
        
        # Mark visited words to avoid revisiting
        visited = set([beginWord])
        
        while queue:
            word, dist = queue.popleft()
            
            # If this word is endWord, return the path length
            if word == endWord:
                return dist
            
            # Try transforming word by changing each letter to 'a'..'z'
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    # If same char, skip
                    if c == word[i]:
                        continue
                    
                    # Form a new word by replacing the i-th char
                    new_word = word[:i] + c + word[i+1:]
                    
                    # If in word_set and not visited, it's a valid neighbor
                    if new_word in word_set and new_word not in visited:
                        visited.add(new_word)
                        queue.append((new_word, dist + 1))
        
        # If we exhaust BFS without reaching endWord, no transformation is possible
        return 0
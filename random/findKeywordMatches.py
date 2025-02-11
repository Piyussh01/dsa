def find_shortest_segment(document: str, keywords) -> str:
    """
    Finds the shortest segment (substring) of the document that contains all the keywords.
    Assumes that the document is tokenized by whitespace.

    Parameters:
        document (str): The full document as a string.
        keywords (Iterable[str]): A collection of keywords to match.
        
    Returns:
        str: The shortest segment containing all keywords, or an empty string if not possible.
    """
    # Tokenize the document into words
    words = document.split()
    
    # Convert keywords to a set for quick lookup
    keyword_set = set(keywords)
    required = len(keyword_set)
    
    # This dictionary will count the occurrences of keywords in the current window.
    window_counts = {}
    
    # Initialize pointers and variables to track the best window found.
    have = 0
    res = (-1, -1)
    res_len = float('inf')
    left = 0

    # Iterate with the right pointer over the words.
    for right, word in enumerate(words):
        # If the current word is a keyword, update its count in the window.
        if word in keyword_set:
            window_counts[word] = window_counts.get(word, 0) + 1
            print(window_counts[word], "here")
            # If this is the first time the keyword appears in the window, increment our match count.
            if window_counts[word] == 1:
                have += 1
        
        # When the current window contains all keywords, try to shrink it from the left.
        while have == required and left <= right:
            # Update the result if the current window is smaller.
            window_length = right - left + 1
            if window_length < res_len:
                res = (left, right)
                res_len = window_length
            
            # Prepare to shrink the window from the left.
            left_word = words[left]
            if left_word in keyword_set:
                window_counts[left_word] -= 1
                # If a keyword's count drops to zero, we no longer satisfy the requirement.
                if window_counts[left_word] == 0:
                    have -= 1
            left += 1
    
    # If no valid window was found, return an empty string.
    if res_len == float('inf'):
        return ""
    
    # Otherwise, return the shortest segment (reconstructing it from words).
    start, end = res
    return " ".join(words[start:end+1])


# Example usage:
if __name__ == "__main__":
    doc = "this is a test document that we will use to test the keyword matching algorithm"
    keywords = ["test", "keyword", "algorithm"]
    result = find_shortest_segment(doc, keywords)
    print("Shortest segment:", result)
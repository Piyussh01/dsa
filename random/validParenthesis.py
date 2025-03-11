class Solution:
    def isValid(self, s: str) -> bool:
        corr_open_paranthesis = {")": "(", "}": "{", "]": "["}
        stack = []

        for char in s:
            # If it's an opening bracket, push to stack.
            if char in ["(", "{", "["]:
                stack.append(char)
            else:
                # It's a closing bracket. Check if stack is empty or matches.
                if not stack or corr_open_paranthesis[char] != stack[-1]:
                    return False
                stack.pop()
        
        # Finally, stack must be empty for a valid string.
        return len(stack) == 0
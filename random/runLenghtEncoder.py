class Solution:
    def encoder(self, s: str) -> None:
        # Handle empty string input
        if not s:
            print("")
            return
        
        result = []  # This will store parts of our encoded string.
        count = 1   # Start with count 1 for the first character
        
        # Iterate from the second character to the end
        for i in range(1, len(s)):
            if s[i] == s[i - 1]:
                count += 1
            else:
                # When the current character is different, append the previous character and its count.
                result.append(s[i - 1] + str(count))
                count = 1  # Reset count for the new character
        
        # Append the final run after the loop ends.
        result.append(s[-1] + str(count))
        
        # Join all parts together and print the encoded string.
        encoded_string = "".join(result)
        print(encoded_string)

if __name__ == "__main__":
    sol = Solution()
    st = "wwwwaaadexxxxxxywww"
    sol.encoder(st)
class Solution:
    def restoreIpAddresses(self, s: str) -> list[str]:
        result = []

        def backtrack(start, segments):
            if len(segments) == 4 and start == len(s):
                result.append(".".join(segments))
                return
            
            if len(segments) == 4:
                return
            
            for length in range(1,4):
                if start + length > len(s):
                    break
                segment = s[start:start+length]
                
                if len(segment) > 1 and segment[0] == '0':
                    break 

                if int(segment) > 255:
                    break
                
                segments.append(segment)
                backtrack(start+length, segments)
                segments.pop()

        backtrack(0, [])
        return result
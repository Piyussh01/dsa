class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        dic = {}
        for i, num in enumerate(nums):
            c = target - num
            if c in dic:
              return [dic[c], i]
            dic[num] = i
        return []
        
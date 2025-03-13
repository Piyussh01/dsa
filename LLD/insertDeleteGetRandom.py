import random

class RandomizedSet:

    def __init__(self):
        # List to store the elements
        self.nums = []
        # Dictionary to map each value to its index in self.nums
        self.indices = {}
        
    def insert(self, val: int) -> bool:
        """
        Inserts an item val into the set if not present.
        Returns True if the item was not present, False otherwise.
        """
        if val in self.indices:
            return False
        
        # Record the index where we will place this value.
        self.indices[val] = len(self.nums)
        self.nums.append(val)
        return True

    def remove(self, val: int) -> bool:
        """
        Removes an item val from the set if present.
        Returns True if the item was present, False otherwise.
        """
        if val not in self.indices:
            return False
        
        # Get the index of the element to remove
        idx_to_remove = self.indices[val]
        
        # Get the last element
        last_element = self.nums[-1]
        
        # Swap the last element with the element to remove
        self.nums[idx_to_remove] = last_element
        self.indices[last_element] = idx_to_remove
        
        # Remove the last element
        self.nums.pop()
        del self.indices[val]
        
        return True

    def getRandom(self) -> int:
        """
        Returns a random element from the current set of elements.
        Each element must have the same probability of being returned.
        """
        rand_idx = random.randrange(len(self.nums))
        return self.nums[rand_idx]

class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None 
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}

        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    #A <-> node <-> B
    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev #since doubly linkedin list
    
    #head <-> node <-> first
    def _add(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add(node) ## Move to front (mark as recently used)
        return node.val
    
    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        
        node = Node(key,value)
        self.cache[key]= node
        self._add(node)

        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

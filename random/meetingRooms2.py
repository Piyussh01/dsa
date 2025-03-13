import heapq

class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        # If there are no meetings, no rooms are needed.
        if not intervals:
            return 0

        # 1) Sort intervals by start time
        intervals.sort(key=lambda x: x[0])

        # 2) Initialize a min-heap to store end times
        room_heap = []

        for meeting in intervals:
            start, end = meeting

            # 3) If the earliest ending meeting is done before 'start', free that room
            if room_heap and room_heap[0] <= start:
                heapq.heappop(room_heap)

            # 4) Allocate a new room (or reuse just freed room) by pushing the current end
            heapq.heappush(room_heap, end)

        # 5) The size of the heap is the number of rooms in use
        return len(room_heap)

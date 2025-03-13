class Solution:
    def reorderLogFiles(self, logs: List[str]) -> List[str]:
        letter_logs = []
        digit_logs = []

        for log in logs:

            id_end = log.find(" ")
            identifier = log[:id_end]
            rest = log[id_end+1:]

            if rest[0].isdigit():
                digit_logs.append(log)
            else:
                letter_logs.append((identifier, rest))
        
        letter_logs.sort(key=lambda x: (x[1], x[0]))
        letter_logs = [f"{iden} {rest}" for (iden, rest) in letter_logs]

        return letter_logs + digit_logs

	# •	Partitioning each log into digit or letter takes  O(n)  operations (each log is scanned briefly).
	# •	Sorting the letter-logs: In the worst case, almost all logs are letter-logs, so up to  O(n \log n) .
	# •	Comparison for each pair involves comparing the “rest” strings and possibly the identifier (both up to length  m ), so each comparison is  O(m) .
	# •	Overall  O(n \log n \times m)  for sorting.
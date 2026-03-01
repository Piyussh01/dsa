# 🚀 2-Week Interview Prep Master Guide

**Study Plan:** 2 hours coding + 1 hour system design + 30 min behavioral daily

---

## 📦 What's Included

### 📘 Core Guides
1. **`problem_solving_guide.md`** - Universal problem-solving framework
   - Step-by-step flow for any coding problem
   - Analogies for every pattern
   - Communication tips
   - How to get "aha moments"

2. **`week_practice_plan.md`** - Your 7-day roadmap
   - Day-by-day breakdown
   - Real Python projects (not LeetCode!)
   - System design topics
   - Behavioral prep

### 💻 Runnable Python Projects (Days 1-2)

**Day 1: Graph Foundations (DFS/BFS)**
- **`day1_file_explorer.py`** - File system traversal
  - DFS: Find all files recursively
  - BFS: Organize by depth level
  - Cycle detection: Handle symbolic links
  
**Day 2: Advanced Graphs**
- **`day2_task_scheduler.py`** - Topological Sort
  - CI/CD pipeline scheduling
  - Dependency resolution
  - Circular dependency detection
  
- **`day2_network_router.py`** - Dijkstra's Algorithm
  - Find fastest network routes
  - Calculate broadcast time
  - Alternative path finding

---

## 🎯 Quick Start Guide

### 1. Start with the Problem-Solving Guide
```bash
# Read this FIRST
cat problem_solving_guide.md
```

**Key takeaways:**
- The 6-step universal framework
- Pattern recognition triggers
- How to think through problems
- Communication strategies

### 2. Review Your Week Plan
```bash
cat week_practice_plan.md
```

**This gives you:**
- What to study each day
- Real projects to build
- System design topics
- Behavioral questions

### 3. Run the Python Projects
```bash
# Day 1: Graph basics
python day1_file_explorer.py

# Day 2: Topological Sort
python day2_task_scheduler.py

# Day 2: Dijkstra's Algorithm
python day2_network_router.py
```

**Each project includes:**
- Real-world scenario
- Detailed explanations
- Interview walkthroughs
- Key insights section

---

## 🗓️ Your Daily Routine

### Morning (2 hours - Coding)
**Hour 1: Theory + LeetCode (60 min)**
- Read problem
- Identify pattern (use guide!)
- Solve 2-3 problems from your list

**Hour 2: Real Project (60 min)**
- Build practical application
- Understand WHY, not just HOW
- Run and modify the code

### Midday (1 hour - System Design)
Follow the framework:
1. Requirements (5 min)
2. Capacity estimation (5 min)
3. High-level design (15 min)
4. Deep dive (25 min)
5. Bottlenecks (10 min)

### Afternoon (30 min - Behavioral)
Practice STAR method:
- **S**ituation
- **T**ask
- **A**ction
- **R**esult

---

## 🎓 How to Use the Python Projects

### They're NOT Just Code to Read
They're learning tools with:

1. **Real-world context**
   - "Why would I use this?"
   - Practical applications
   
2. **Multiple perspectives**
   - Beginner explanations
   - Advanced optimizations
   - Interview walkthroughs

3. **Runnable demos**
   - See algorithms in action
   - Modify and experiment
   - Test edge cases

### Example Learning Flow:
```bash
# 1. Run the project
python day1_file_explorer.py

# 2. Read the code comments
#    (They explain WHY, not just WHAT)

# 3. Modify it!
#    Change parameters, add features, break it!

# 4. Apply to LeetCode
#    Now solve: "Number of Islands" using same pattern
```

---

## 🧠 Problem-Solving Mindset

### Before Coding, Ask:
1. "What pattern is this?" (Graph? DP? Sliding window?)
2. "What's the brute force?" (Always start here!)
3. "How can I optimize?" (Better data structure? Different approach?)

### During Coding, Say:
- "I'm using X because..."
- "This handles the edge case where..."
- "Let me trace through an example..."

### After Coding, Check:
- Empty input
- Single element
- All same elements
- Maximum size input

---

## 📊 Problem Categories & Patterns

From your list, here are the main patterns:

### Graph Algorithms (Days 1-2)
- **DFS**: Redundant Connection, Connected Components
- **BFS**: Shortest Path in Matrix, Word Ladder
- **Topological Sort**: Course Schedule
- **Dijkstra**: Network Delay
- **MST**: Minimum Cost to Connect Cities

**Trigger words:** connected, path, network, shortest, dependencies

### Dynamic Programming (Day 3)
- **LIS**: Longest Increasing Subsequence
- **LCS**: Longest Common Subsequence
- **Knapsack**: Word Break
- **Kadane's**: Maximum Product Subarray

**Trigger words:** subsequence, maximum, optimal, count ways

### Sliding Window (Day 4)
- Longest Substring Without Repeating
- Subarray Sum Equals K
- Minimum Size Subarray Sum

**Trigger words:** subarray, substring, contiguous, window

### Heaps (Day 5)
- Merge K Sorted Lists
- Koko Eating Bananas

**Trigger words:** K largest/smallest, merge sorted, median

### Strings (Day 6)
- Longest Palindromic Substring
- Word Break
- String Compression

**Trigger words:** palindrome, pattern matching, compression

---

## 🎯 LeetCode Problem Mapping

Use our projects to solve these from your list:

**After Day 1 (DFS/BFS):**
- ✅ Redundant Connection
- ✅ Number of Connected Components
- ✅ Shortest Clear Path in Matrix
- ✅ All Nodes at Distance K

**After Day 2 (Topological/Dijkstra):**
- ✅ Course Schedule
- ✅ Network Delay
- ✅ Shortest Path in DAG
- ✅ Cheapest Flights within K Stops

**After Day 3 (DP):**
- ✅ Longest Increasing Subsequence
- ✅ Longest Common Subsequence
- ✅ Maximum Product Subarray
- ✅ Word Break

**After Day 4 (Sliding Window):**
- ✅ Longest Substring Without Repeating
- ✅ Subarray Sum Equals K
- ✅ Longest Subarray of 1s

**After Day 5 (Heaps):**
- ✅ Merge K Sorted Lists
- ✅ Koko Eating Bananas

---

## 💡 Analogy Cheat Sheet

Quick mental models to remember:

| Algorithm | Analogy | Use When |
|-----------|---------|----------|
| DFS | Exploring a maze (go deep) | Need all paths |
| BFS | Ripples in pond (go wide) | Need shortest path |
| Topological Sort | Getting dressed (order matters) | Dependencies |
| Dijkstra | GPS navigation | Weighted shortest path |
| DP | Climbing stairs with memory | Overlapping subproblems |
| Sliding Window | Train window view | Contiguous subarray |
| Heap | ER triage (most urgent first) | K largest/smallest |
| Binary Search | Guessing game (higher/lower) | Sorted search |

---

## 🚨 Common Interview Mistakes to Avoid

1. **Going silent** 
   ❌ Code in silence
   ✅ Think out loud constantly

2. **Not clarifying**
   ❌ Assume requirements
   ✅ Ask questions first

3. **Jumping to code**
   ❌ Start coding immediately
   ✅ Explain approach first

4. **Ignoring edge cases**
   ❌ Only test happy path
   ✅ Test empty, single, max inputs

5. **Not optimizing**
   ❌ Stop at brute force
   ✅ Discuss better approaches

6. **Over-complicating**
   ❌ Use advanced syntax
   ✅ Keep it simple and clear

---

## 📈 Progress Tracking

Create a simple checklist:

```
Week 1:
□ Day 1: Graph basics (DFS/BFS)
□ Day 2: Advanced graphs (Topological/Dijkstra)
□ Day 3: DP basics
□ Day 4: Sliding Window
□ Day 5: Heaps & Binary Search
□ Day 6: Strings & review
□ Day 7: Mixed practice

Week 2:
□ Review all patterns
□ Speed practice (time yourself!)
□ Mock interviews
□ System design deep dives
□ Polish behavioral stories
```

---

## 🎬 Interview Day Checklist

### Night Before
- ✅ Review pattern cheat sheet
- ✅ Do ONE easy problem
- ✅ Get good sleep (8 hours!)
- ❌ DON'T cram new topics

### Day Of
- ✅ Eat a good breakfast
- ✅ Test your setup (camera, mic)
- ✅ Have water nearby
- ✅ Paper and pen ready
- ✅ Positive mindset!

### During Interview
- ✅ Breathe deeply
- ✅ Think out loud
- ✅ Ask clarifying questions
- ✅ Start with brute force
- ✅ Test your code
- ✅ Stay positive even if stuck

---

## 🤝 Remember

**You're not trying to be perfect.**
**You're trying to be hire-able.**

Interviewers evaluate:
- 40% Problem-solving approach
- 30% Communication
- 20% Code quality
- 10% Getting the right answer

So even if you don't finish, showing good process matters!

---

## 📚 Additional Resources

### Week 1 Projects (Coming)
- Day 3: Text Diff Tool (DP)
- Day 4: Log Analyzer (Sliding Window)
- Day 5: Task Priority System (Heaps)
- Day 6: Autocomplete (Trie/Strings)
- Day 7: Mini Database (Mixed)

### System Design Resources
- Grokking System Design Interview
- System Design Primer (GitHub)
- ByteByteGo videos

### Behavioral Prep
- Prepare 5 STAR stories
- Practice with friend
- Record yourself

---

## 🎯 Final Tips

1. **Consistency > Intensity**
   - 2 hours daily > 14 hours Sunday

2. **Understand > Memorize**
   - Know WHY, not just WHAT

3. **Practice out loud**
   - Talk through problems alone

4. **Stay positive**
   - Everyone gets stuck
   - Interviewers are rooting for you

5. **It's a skill**
   - Gets easier with practice
   - Patterns become second nature

---

## 🚀 Let's Go!

Your journey starts now:
1. Read `problem_solving_guide.md`
2. Open `week_practice_plan.md`
3. Run `day1_file_explorer.py`
4. Solve your first problem!

**You've got this! 💪**

---

## 📞 Questions?

If confused about a concept:
1. Run the Python project
2. Read the explanations in code
3. Draw it out on paper
4. Explain it to yourself out loud
5. Try modifying the code

Remember: Understanding beats memorization every time!

---

**Good luck! You're more prepared than you think! 🎉**

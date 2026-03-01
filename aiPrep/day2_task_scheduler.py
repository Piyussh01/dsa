"""
DAY 2 PROJECT A: Task Scheduler with Dependencies
Concept: Topological Sort (Kahn's Algorithm)

Real-world scenario: CI/CD Pipeline
- Tasks have dependencies (can't deploy before testing)
- Need to find valid execution order
- Detect impossible builds (circular dependencies)
"""

from collections import defaultdict, deque

class TaskScheduler:
    def __init__(self):
        self.graph = defaultdict(list)  # dependency -> tasks that depend on it
        self.indegree = defaultdict(int)  # task -> number of dependencies
        self.all_tasks = set()
    
    def add_task(self, task, dependencies=None):
        """
        Add a task with its dependencies
        
        Example: add_task("deploy", ["test", "build"])
        means: "deploy" requires "test" and "build" to be done first
        """
        if dependencies is None:
            dependencies = []
        
        self.all_tasks.add(task)
        
        # Initialize indegree
        if task not in self.indegree:
            self.indegree[task] = 0
        
        # Build graph and track indegrees
        for dep in dependencies:
            self.all_tasks.add(dep)
            self.graph[dep].append(task)
            self.indegree[task] += 1
    
    def can_complete_all_tasks(self):
        """
        Topological Sort - Kahn's Algorithm
        
        ANALOGY: Getting dressed in the morning
        - Can't put on shoes before socks!
        - Some things have no prerequisites (underwear)
        - Start with those, then work your way up
        
        ALGORITHM:
        1. Start with tasks that have NO dependencies (indegree = 0)
        2. "Complete" them, reduce dependency count of tasks waiting on them
        3. If any task becomes ready (indegree = 0), add to queue
        4. If we complete all tasks → no cycle! If not → cycle exists
        
        TIME: O(V + E) where V = tasks, E = dependencies
        SPACE: O(V)
        """
        # Find all tasks with no dependencies
        queue = deque([task for task in self.all_tasks if self.indegree[task] == 0])
        completed = []
        
        while queue:
            # "Complete" this task
            current_task = queue.popleft()
            completed.append(current_task)
            
            # For all tasks that depended on this one
            for next_task in self.graph[current_task]:
                # One less dependency
                self.indegree[next_task] -= 1
                
                # If no more dependencies, can do it now!
                if self.indegree[next_task] == 0:
                    queue.append(next_task)
        
        # If we completed all tasks, no cycle
        return len(completed) == len(self.all_tasks)
    
    def get_execution_order(self):
        """
        Return valid execution order, or None if impossible
        """
        # Make a copy of indegree so we don't modify original
        indegree_copy = self.indegree.copy()
        
        queue = deque([task for task in self.all_tasks if indegree_copy[task] == 0])
        execution_order = []
        
        while queue:
            task = queue.popleft()
            execution_order.append(task)
            
            for next_task in self.graph[task]:
                indegree_copy[next_task] -= 1
                if indegree_copy[next_task] == 0:
                    queue.append(next_task)
        
        # Check if we could schedule all tasks
        if len(execution_order) != len(self.all_tasks):
            return None  # Circular dependency!
        
        return execution_order
    
    def find_circular_dependency(self):
        """
        Find which tasks form a circular dependency
        """
        execution = self.get_execution_order()
        if execution is not None:
            return None  # No circular dependency
        
        # Find tasks that couldn't be scheduled
        indegree_copy = self.indegree.copy()
        queue = deque([task for task in self.all_tasks if indegree_copy[task] == 0])
        completed = set()
        
        while queue:
            task = queue.popleft()
            completed.add(task)
            
            for next_task in self.graph[task]:
                indegree_copy[next_task] -= 1
                if indegree_copy[next_task] == 0:
                    queue.append(next_task)
        
        # Tasks not completed form the cycle
        return list(self.all_tasks - completed)


def demo():
    print("=" * 70)
    print("🔧 TASK SCHEDULER DEMO - Topological Sort")
    print("=" * 70)
    
    # Demo 1: Valid CI/CD Pipeline
    print("\n📍 DEMO 1: Valid CI/CD Pipeline")
    print("-" * 70)
    
    scheduler = TaskScheduler()
    scheduler.add_task("install_deps", [])
    scheduler.add_task("lint", ["install_deps"])
    scheduler.add_task("unit_test", ["install_deps"])
    scheduler.add_task("integration_test", ["unit_test"])
    scheduler.add_task("build", ["lint", "integration_test"])
    scheduler.add_task("deploy_staging", ["build"])
    scheduler.add_task("smoke_test", ["deploy_staging"])
    scheduler.add_task("deploy_prod", ["smoke_test"])
    
    print("Tasks and dependencies:")
    print("  install_deps → (no dependencies)")
    print("  lint → install_deps")
    print("  unit_test → install_deps")
    print("  integration_test → unit_test")
    print("  build → lint, integration_test")
    print("  deploy_staging → build")
    print("  smoke_test → deploy_staging")
    print("  deploy_prod → smoke_test")
    
    print(f"\n✅ Can complete? {scheduler.can_complete_all_tasks()}")
    order = scheduler.get_execution_order()
    print(f"📋 Execution order:")
    for i, task in enumerate(order, 1):
        print(f"  {i}. {task}")
    
    # Demo 2: Circular Dependency
    print("\n\n📍 DEMO 2: Circular Dependency Detection")
    print("-" * 70)
    
    scheduler2 = TaskScheduler()
    scheduler2.add_task("task_A", ["task_B"])
    scheduler2.add_task("task_B", ["task_C"])
    scheduler2.add_task("task_C", ["task_A"])  # Creates cycle!
    
    print("Tasks and dependencies:")
    print("  task_A → task_B")
    print("  task_B → task_C")
    print("  task_C → task_A  ⚠️  CIRCULAR!")
    
    can_complete = scheduler2.can_complete_all_tasks()
    print(f"\n❌ Can complete? {can_complete}")
    
    if not can_complete:
        cycle_tasks = scheduler2.find_circular_dependency()
        print(f"🔴 Tasks in circular dependency: {cycle_tasks}")
    
    # Demo 3: College Course Prerequisites
    print("\n\n📍 DEMO 3: College Course Prerequisites")
    print("-" * 70)
    
    scheduler3 = TaskScheduler()
    scheduler3.add_task("CS101", [])
    scheduler3.add_task("CS102", ["CS101"])
    scheduler3.add_task("CS201", ["CS102"])
    scheduler3.add_task("CS301", ["CS201"])
    scheduler3.add_task("MATH101", [])
    scheduler3.add_task("MATH201", ["MATH101"])
    scheduler3.add_task("CS250_Algorithms", ["CS102", "MATH101"])
    scheduler3.add_task("CS350_AI", ["CS250_Algorithms", "MATH201"])
    
    print("Taking courses in valid order:")
    order = scheduler3.get_execution_order()
    
    semester = 1
    courses_per_semester = []
    current_semester = []
    
    for course in order:
        current_semester.append(course)
        if len(current_semester) == 2:  # 2 courses per semester
            courses_per_semester.append(current_semester)
            current_semester = []
    
    if current_semester:
        courses_per_semester.append(current_semester)
    
    for i, courses in enumerate(courses_per_semester, 1):
        print(f"\n  Semester {i}: {', '.join(courses)}")


def interview_walkthrough():
    print("\n\n" + "=" * 70)
    print("💼 INTERVIEW WALKTHROUGH")
    print("=" * 70)
    
    print("""
    QUESTION: Given a list of courses and prerequisites, determine if it's
    possible to finish all courses. Also return a valid course order.
    
    Example:
    courses = 4
    prerequisites = [[1,0], [2,0], [3,1], [3,2]]
    
    STEP-BY-STEP THINKING:
    
    1️⃣  RECOGNIZE THE PATTERN
       - "Prerequisites" = dependencies
       - "Check if possible" = detect cycle
       - "Order of courses" = topological sort
       → This is a DIRECTED GRAPH problem
    
    2️⃣  VISUALIZE AS GRAPH
       Draw it out:
       
         0 → 1 → 3
         ↓       ↑
         2 ------┘
       
       Course 0 has no prerequisites (indegree = 0)
       Course 1 requires course 0 (indegree = 1)
       Course 3 requires courses 1 AND 2 (indegree = 2)
    
    3️⃣  ALGORITHM CHOICE
       Topological Sort using BFS (Kahn's Algorithm)
       WHY? We need:
       - Detect cycles (impossible to complete all courses)
       - Find valid ordering
       - BFS naturally gives us level-order (semester-wise planning!)
    
    4️⃣  DATA STRUCTURES
       - graph: dict of lists (course → courses that depend on it)
       - indegree: dict (course → number of prerequisites)
       - queue: deque (courses we can take now)
    
    5️⃣  WALKTHROUGH WITH EXAMPLE
       
       Initial state:
       indegree = {0: 0, 1: 1, 2: 1, 3: 2}
       queue = [0]  (only course 0 has indegree 0)
       
       Step 1: Take course 0
       - Remove 0 from queue
       - Decrease indegree of courses that need 0: [1, 2]
       - indegree = {1: 0, 2: 0, 3: 2}
       - Add 1 and 2 to queue
       
       Step 2: Take course 1
       - Remove 1 from queue
       - Decrease indegree of 3
       - indegree = {2: 0, 3: 1}
       
       Step 3: Take course 2
       - Remove 2 from queue
       - Decrease indegree of 3
       - indegree = {3: 0}
       - Add 3 to queue
       
       Step 4: Take course 3
       - Done!
       
       Result: [0, 1, 2, 3] (one valid order)
    
    6️⃣  EDGE CASES TO MENTION
       ✓ No courses (return empty list)
       ✓ No prerequisites (any order works)
       ✓ Circular dependency (impossible, return False)
       ✓ Disconnected components (some courses independent)
    
    7️⃣  COMPLEXITY ANALYSIS
       Time: O(V + E) where V = courses, E = prerequisites
       - Build graph: O(E)
       - Process each node once: O(V)
       - Process each edge once: O(E)
       
       Space: O(V + E)
       - Graph storage: O(E)
       - Indegree array: O(V)
       - Queue: O(V) worst case
    
    8️⃣  CODE (Simple version)
       ```python
       def can_finish(num_courses, prerequisites):
           # Build graph and indegree
           graph = [[] for _ in range(num_courses)]
           indegree = [0] * num_courses
           
           for course, prereq in prerequisites:
               graph[prereq].append(course)
               indegree[course] += 1
           
           # Find courses with no prerequisites
           queue = [i for i in range(num_courses) if indegree[i] == 0]
           completed = 0
           
           # Process courses
           while queue:
               current = queue.pop(0)
               completed += 1
               
               for next_course in graph[current]:
                   indegree[next_course] -= 1
                   if indegree[next_course] == 0:
                       queue.append(next_course)
           
           return completed == num_courses
       ```
    """)


def key_insights():
    print("\n" + "=" * 70)
    print("🎯 KEY INSIGHTS - Topological Sort")
    print("=" * 70)
    print("""
    1. WHEN TO USE
       ✓ Tasks with dependencies
       ✓ Need ordering that respects constraints
       ✓ Detect circular dependencies
       
       Keywords: "prerequisites", "order", "dependencies", "schedule"
    
    2. TWO APPROACHES
       a) DFS-based (with recursion stack)
          - Finish times in reverse order
          
       b) BFS-based / Kahn's Algorithm (what we used)
          - Start with nodes having no dependencies
          - More intuitive for beginners!
    
    3. REAL-WORLD USES
       - Build systems (Make, Gradle, Maven)
       - Package managers (npm, pip)
       - Course scheduling
       - Task prioritization
       - Spreadsheet cell calculation order
    
    4. INDEGREE TECHNIQUE
       indegree[node] = number of incoming edges
       - Indegree 0 = ready to process (no dependencies)
       - Decrease indegree when dependency is met
       - If indegree never reaches 0 → part of cycle!
    
    5. CYCLE DETECTION
       If we can't schedule all tasks → cycle exists
       Tasks left over form the circular dependency
    
    6. INTERVIEW TIPS
       - Always draw the graph first!
       - Explain indegree concept clearly
       - Mention it's a "DAG problem" (Directed Acyclic Graph)
       - Talk through the queue logic step by step
    """)


if __name__ == "__main__":
    demo()
    interview_walkthrough()
    key_insights()

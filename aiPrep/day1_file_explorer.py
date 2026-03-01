"""
DAY 1 PROJECT: File System Explorer
Concepts: DFS, BFS, Cycle Detection

Real-world scenario: You're building a backup system that needs to:
- Find all files recursively (DFS)
- Organize files by depth (BFS)
- Detect symbolic link loops (Cycle Detection)
"""

import os
from collections import deque

class FileExplorer:
    def __init__(self, root_path):
        self.root_path = root_path
        self.visited = set()
    
    def dfs_find_all_files(self, current_path=None, file_extension=None):
        """
        DFS Implementation
        
        ANALOGY: Exploring a maze
        - Pick a path and go as deep as possible
        - When you hit a dead end, backtrack
        - Mark visited rooms to avoid loops
        
        WHY DFS HERE?
        - We want ALL files, so depth doesn't matter
        - Natural recursion fits directory structure
        - Memory efficient for deep but narrow trees
        """
        if current_path is None:
            current_path = self.root_path
        
        # CYCLE DETECTION: Prevent infinite loops from symbolic links
        real_path = os.path.realpath(current_path)
        if real_path in self.visited:
            print(f"⚠️  Cycle detected at: {current_path}")
            return []
        
        self.visited.add(real_path)
        files = []
        
        try:
            # Base case: if it's a file, return it
            if os.path.isfile(current_path):
                if file_extension is None or current_path.endswith(file_extension):
                    return [current_path]
                return []
            
            # Recursive case: explore all subdirectories
            for item in os.listdir(current_path):
                item_path = os.path.join(current_path, item)
                # Recursively DFS into each item
                files.extend(self.dfs_find_all_files(item_path, file_extension))
                
        except PermissionError:
            print(f"⛔ Permission denied: {current_path}")
        
        return files
    
    def bfs_files_by_depth(self):
        """
        BFS Implementation
        
        ANALOGY: Ripples in a pond
        - Explore all neighbors at same distance first
        - Then move to next distance level
        - Like scanning one floor before going to next floor
        
        WHY BFS HERE?
        - We care about DEPTH LEVEL
        - Want to organize files by how nested they are
        - Perfect for level-order traversal
        """
        queue = deque([(self.root_path, 0)])  # (path, depth)
        files_by_depth = {}
        visited = set()
        
        while queue:
            current_path, depth = queue.popleft()
            
            # Cycle detection
            real_path = os.path.realpath(current_path)
            if real_path in visited:
                continue
            visited.add(real_path)
            
            # Track files at this depth
            if depth not in files_by_depth:
                files_by_depth[depth] = []
            
            try:
                if os.path.isfile(current_path):
                    files_by_depth[depth].append(current_path)
                else:
                    # Add all immediate children to queue
                    for item in os.listdir(current_path):
                        queue.append((os.path.join(current_path, item), depth + 1))
            except PermissionError:
                pass
        
        return files_by_depth
    
    def find_duplicate_filenames(self):
        """
        BONUS: Find files with same name in different locations
        Uses DFS + HashMap
        """
        filename_map = {}
        all_files = self.dfs_find_all_files()
        
        for filepath in all_files:
            filename = os.path.basename(filepath)
            if filename not in filename_map:
                filename_map[filename] = []
            filename_map[filename].append(filepath)
        
        # Return only duplicates
        return {name: paths for name, paths in filename_map.items() if len(paths) > 1}


def demo():
    """
    Run demonstrations
    """
    print("=" * 70)
    print("🗂️  FILE EXPLORER DEMO - Graph Traversal in Real Life")
    print("=" * 70)
    
    # Create a test directory structure
    test_dir = "/tmp/file_explorer_demo"
    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(f"{test_dir}/docs", exist_ok=True)
    os.makedirs(f"{test_dir}/docs/2024", exist_ok=True)
    os.makedirs(f"{test_dir}/code", exist_ok=True)
    
    # Create some test files
    open(f"{test_dir}/readme.txt", 'w').write("Root file")
    open(f"{test_dir}/docs/report.txt", 'w').write("Doc file")
    open(f"{test_dir}/docs/2024/summary.txt", 'w').write("Nested doc")
    open(f"{test_dir}/code/main.py", 'w').write("print('hello')")
    
    explorer = FileExplorer(test_dir)
    
    # Demo 1: DFS - Find all files
    print("\n📍 DEMO 1: DFS - Find all Python files")
    print("-" * 70)
    print("USE CASE: 'Find all .py files in my project'")
    print("ALGORITHM: DFS (explores deep before wide)")
    print()
    
    all_files = explorer.dfs_find_all_files(file_extension='.txt')
    for i, f in enumerate(all_files, 1):
        print(f"  {i}. {f}")
    print(f"\n✅ Found {len(all_files)} text files using DFS")
    
    # Demo 2: BFS - Organize by depth
    print("\n\n📍 DEMO 2: BFS - Organize files by nesting level")
    print("-" * 70)
    print("USE CASE: 'Show me what's at each depth level'")
    print("ALGORITHM: BFS (explores level by level)")
    print()
    
    explorer.visited.clear()  # Reset for new traversal
    by_depth = explorer.bfs_files_by_depth()
    
    for depth in sorted(by_depth.keys()):
        print(f"\n  Depth {depth} ({len(by_depth[depth])} items):")
        for item in by_depth[depth][:3]:  # Show first 3
            print(f"    • {os.path.basename(item)}")
        if len(by_depth[depth]) > 3:
            print(f"    ... and {len(by_depth[depth]) - 3} more")
    
    # Demo 3: Cycle Detection
    print("\n\n📍 DEMO 3: Cycle Detection")
    print("-" * 70)
    print("USE CASE: 'Detect infinite loops from symbolic links'")
    print()
    
    # Create a symbolic link that creates a cycle
    try:
        symlink_path = f"{test_dir}/cycle_link"
        if not os.path.exists(symlink_path):
            os.symlink(test_dir, symlink_path)
        
        print(f"  Created symbolic link: {symlink_path} -> {test_dir}")
        print("  This creates a cycle in the file system!")
        print()
        
        explorer.visited.clear()
        print("  Running DFS with cycle detection...")
        files_with_cycle = explorer.dfs_find_all_files()
        print(f"  ✅ Cycle detected and handled! Found {len(files_with_cycle)} unique files")
        
    except OSError as e:
        print(f"  (Skipping symlink demo: {e})")
    
    # Comparison
    print("\n\n📊 DFS vs BFS - When to use which?")
    print("=" * 70)
    print("""
    DFS (Depth-First Search)
    ✅ Use when: Need to explore ALL possibilities
    ✅ Use when: Memory is a concern (narrower trees)
    ✅ Use when: Finding any solution (not necessarily shortest)
    📝 Example: "Find any file named config.txt"
    
    BFS (Breadth-First Search)  
    ✅ Use when: Need SHORTEST path
    ✅ Use when: Care about LEVELS/DEPTH
    ✅ Use when: Want closest matches first
    📝 Example: "Find shallowest occurrence of config.txt"
    """)
    
    print("\n🧹 Cleaning up demo files...")
    import shutil
    shutil.rmtree(test_dir)
    print("✅ Done!")


def interview_practice():
    """
    Practice question for interviews
    """
    print("\n" + "=" * 70)
    print("💼 INTERVIEW PRACTICE")
    print("=" * 70)
    
    print("""
    QUESTION: Given a file system, implement a function to find all files
    that are duplicates (same name, different locations).
    
    APPROACH:
    1. Use DFS to traverse all files
    2. Use HashMap to track filename -> list of paths
    3. Return files that appear in multiple locations
    
    TIME COMPLEXITY: O(N) where N is number of files
    SPACE COMPLEXITY: O(N) for the hashmap
    """)
    
    print("\n📝 WALKTHROUGH:")
    print("""
    Example directory:
    /project
        /src
            main.py
        /tests
            main.py      <- duplicate name!
        /docs
            readme.md
    
    Step 1: DFS to get all files
    Step 2: Build map: {"main.py": ["/project/src/main.py", "/project/tests/main.py"]}
    Step 3: Filter to only duplicates
    
    Result: {"main.py": [...]}
    """)


if __name__ == "__main__":
    demo()
    interview_practice()
    
    print("\n" + "=" * 70)
    print("🎯 KEY TAKEAWAYS")
    print("=" * 70)
    print("""
    1. DFS = Go deep first (recursion, stack)
       - Natural for nested structures
       - Memory efficient for deep trees
    
    2. BFS = Go wide first (queue)
       - Best for shortest path
       - Best for level-order
    
    3. Always track VISITED to prevent cycles!
    
    4. Real-world uses:
       - DFS: File search, dependency resolution
       - BFS: Social networks, shortest routes
       - Cycle detection: Deadlock detection, circular dependencies
    """)

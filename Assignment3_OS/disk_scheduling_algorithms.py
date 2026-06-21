"""
Disk Scheduling Algorithms Implementation
Purpose: To calculate total head movement for different disk scheduling strategies
"""

def fcfs(initial, requests):
    """
    FCFS - First Come First Served
    Processes disk requests in the exact order they arrive
    Simplest but often inefficient with high seek times
    """
    if not requests:
        return 0
    
    total_movement = 0
    current_pos = initial
    
    for track in requests:
        distance = abs(track - current_pos)
        total_movement += distance
        current_pos = track
    
    return total_movement


def sstf(initial, requests):
    """
    SSTF - Shortest Seek Time First
    Always services the request closest to current head position
    Minimizes seek time but can cause starvation
    """
    if not requests:
        return 0
    
    total_movement = 0
    current_pos = initial
    remaining = requests.copy()
    
    while remaining:
        # Find and process the closest request
        closest = min(remaining, key=lambda x: abs(x - current_pos))
        distance = abs(closest - current_pos)
        total_movement += distance
        current_pos = closest
        remaining.remove(closest)
    
    return total_movement


def scan(initial, requests, disk_size=200):
    """
    SCAN - Elevator Algorithm (moving toward 0 initially)
    Head moves from current position toward 0, HITS TRACK 0,
    then moves back toward 199 servicing remaining requests.
    Direction: LEFT FIRST (toward 0)
    """
    if not requests:
        return 0
    
    total_movement = 0
    current_pos = initial
    remaining = requests.copy()
    
    left = sorted([x for x in remaining if x < current_pos], reverse=True)
    right = sorted([x for x in remaining if x >= current_pos])
    
    # Direction 1: Move LEFT toward 0, servicing all left requests
    for track in left:
        total_movement += abs(track - current_pos)
        current_pos = track
        
    # MUST hit the disk boundary (Track 0) before reversing
    total_movement += abs(0 - current_pos)
    current_pos = 0
    
    # Direction 2: Reverse and move RIGHT, servicing all right requests
    for track in right:
        total_movement += abs(track - current_pos)
        current_pos = track
    
    return total_movement


def c_scan(initial, requests, disk_size=200):
    """
    C-SCAN - Circular SCAN (moving toward 199 initially)
    Head moves from current position toward 199, HITS TRACK 199,
    jumps to 0, and returns to starting area moving right.
    Direction: RIGHT FIRST (toward 199)
    """
    if not requests:
        return 0
    
    total_movement = 0
    current_pos = initial
    remaining = requests.copy()
    
    left = sorted([x for x in remaining if x < current_pos])
    right = sorted([x for x in remaining if x >= current_pos])
    
    # Direction 1: Move RIGHT toward 199, servicing all right requests
    for track in right:
        total_movement += abs(track - current_pos)
        current_pos = track
        
    # MUST hit the upper disk boundary (Track 199)
    total_movement += abs((disk_size - 1) - current_pos)
    current_pos = disk_size - 1
    
    # Jump back to 0
    total_movement += abs(0 - current_pos)
    current_pos = 0
    
    # Direction 2: Move RIGHT from 0, servicing all left requests
    for track in left:
        total_movement += abs(track - current_pos)
        current_pos = track
    
    return total_movement


def c_look(initial, requests):
    """
    C-LOOK - Circular LOOK (moving toward 0 initially)
    Services left, jumps to HIGHEST right request, continues servicing left.
    Direction: LEFT FIRST (toward 0), jump, LEFT AGAIN.
    """
    if not requests:
        return 0
    
    total_movement = 0
    current_pos = initial
    remaining = requests.copy()
    
    # Both sorted descending because C-LOOK only services in ONE direction (toward 0)
    left = sorted([x for x in remaining if x < current_pos], reverse=True)
    right = sorted([x for x in remaining if x >= current_pos], reverse=True)
    
    # Phase 1: Move LEFT toward 0
    for track in left:
        total_movement += abs(track - current_pos)
        current_pos = track
    
    # Jump to highest request on the right (if it exists)
    if right:
        highest_right = max(right)
        total_movement += abs(highest_right - current_pos)
        current_pos = highest_right
        
        # Phase 2: Continue moving LEFT (toward 0)
        # Exclude the highest_right since we just jumped to it
        for track in right[1:]:
            total_movement += abs(track - current_pos)
            current_pos = track
    
    return total_movement


def n_step_scan(initial, requests, n=4):
    """
    N-STEP SCAN - Divides request queue into groups of N
    Each group is processed using SCAN algorithm independently (toward 0)
    """
    if not requests:
        return 0
    
    total_movement = 0
    current_pos = initial
    remaining = requests.copy()
    
    # Process requests in groups of n
    while remaining:
        batch = remaining[:n]
        remaining = remaining[n:]
        
        # Apply SCAN logic to this batch (move left first toward 0)
        left = sorted([x for x in batch if x < current_pos], reverse=True)
        right = sorted([x for x in batch if x >= current_pos])
        
        # Move left
        for track in left:
            total_movement += abs(track - current_pos)
            current_pos = track
            
        # Hit boundary
        total_movement += abs(0 - current_pos)
        current_pos = 0
        
        # Move right
        for track in right:
            total_movement += abs(track - current_pos)
            current_pos = track
    
    return total_movement


def lifo(initial, requests):
    """
    LIFO - Last-In First-Out
    Processes requests in reverse order
    """
    if not requests:
        return 0
    
    total_movement = 0
    current_pos = initial
    remaining = requests.copy()
    
    # Process in reverse order (LIFO behavior)
    while remaining:
        track = remaining.pop()
        distance = abs(track - current_pos)
        total_movement += distance
        current_pos = track
    
    return total_movement


def rss(initial, requests):
    """
    RSS - Random Scheduling (RSS)
    Processes requests in random order
    """
    if not requests:
        return 0
    
    import random
    
    total_movement = 0
    current_pos = initial
    remaining = requests.copy()
    
    # Randomize the order of requests
    random.shuffle(remaining)
    
    # Process in random order
    for track in remaining:
        distance = abs(track - current_pos)
        total_movement += distance
        current_pos = track
    
    return total_movement


# ==== MAIN PROGRAM ====

def run_test(initial_head, requests, test_name=""):
    """Run all algorithms on a given request queue and return results"""
    print(f"\n{'='*60}")
    print(f"Test: {test_name} (Queue Size: {len(requests)})")
    print(f"{'='*60}")
    print(f"Initial Head Position: {initial_head}")
    print(f"Request Queue: {requests}\n")
    
    results = {
        'FCFS': fcfs(initial_head, requests),
        'SSTF': sstf(initial_head, requests),
        'SCAN': scan(initial_head, requests),
        'C-SCAN': c_scan(initial_head, requests),
        'C-LOOK': c_look(initial_head, requests),
        'N-STEP-SCAN': n_step_scan(initial_head, requests), # Using default N=4
        'LIFO': lifo(initial_head, requests),
        'RSS': rss(initial_head, requests),
    }
    
    # Print results sorted by efficiency
    print(f"{'Algorithm':<15} {'Total Movement':<15} {'Efficiency Rank':<15}")
    print("-" * 45)
    
    sorted_results = sorted(results.items(), key=lambda x: x[1])
    for rank, (algo, movement) in enumerate(sorted_results, 1):
        print(f"{algo:<15} {movement:<15} {rank}")
    
    return results


# Test Data from Assignment
head = 50
reqs = [78, 170, 43, 156, 24, 160, 190, 160, 67, 40, 112, 45, 78]

# Run tests with different queue sizes
print("DISK SCHEDULING ALGORITHM ANALYSIS")
print("="*60)

# Original test set (13 requests)
results_13 = run_test(head, reqs, "Original Dataset")

# Test with 5 requests
reqs_5 = reqs[:5]
results_5 = run_test(head, reqs_5, "Reduced Set (5 requests)")

# Test with 10 requests
reqs_10 = reqs[:10]
results_10 = run_test(head, reqs_10, "Medium Set (10 requests)")

# Test with 20 requests
reqs_20 = reqs + reqs[:7]
results_20 = run_test(head, reqs_20, "Expanded Set (20 requests)")

# Test with 100 requests (larger dataset)
import random
random.seed(42)  # For reproducibility
reqs_100 = reqs + [random.randint(0, 199) for _ in range(87)]
results_100 = run_test(head, reqs_100, "Large Set (100 requests)")

# Summary comparison
print(f"\n{'='*60}")
print("PERFORMANCE SUMMARY ACROSS DIFFERENT QUEUE SIZES")
print(f"{'='*60}\n")
print(f"{'Algorithm':<15} {'Q=5':<12} {'Q=10':<12} {'Q=13':<12} {'Q=20':<12} {'Q=100':<12}")
print("-" * 75)

for algo in ['FCFS', 'SSTF', 'SCAN', 'C-SCAN', 'C-LOOK', 'N-STEP-SCAN', 'LIFO']:
    print(f"{algo:<15} {results_5[algo]:<12} {results_10[algo]:<12} {results_13[algo]:<12} {results_20[algo]:<12} {results_100[algo]:<12}")

print("\nBest performing algorithm (Original 13-queue test):")
best_algo = min(results_13.items(), key=lambda x: x[1])
print(f"  {best_algo[0]}: {best_algo[1]} tracks")
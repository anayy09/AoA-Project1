"""
Network Packet Scheduling - Greedy Algorithm

Real Problem:
In modern network routers and switches, packets arrive continuously and need to be 
transmitted through a network interface with limited bandwidth. Each packet has a 
deadline (by which it must be transmitted to avoid timeout), a priority level 
(critical medical data vs regular browsing), and a transmission time. The router 
must decide which packets to transmit to maximize the total priority value of 
successfully transmitted packets before their deadlines.

This is critical in Quality of Service (QoS) systems for telecommunications, 
IoT networks, and real-time data transmission systems.

Abstract Problem:
Given a set of jobs J = {j1, j2, ..., jn} where each job ji has:
- deadline di (time unit by which it must complete)
- priority/value pi (importance of the job)
- processing time ti (time required to complete)

Find a subset S ⊆ J and an ordering of jobs in S such that:
1. No job in S misses its deadline
2. The sum of priorities Σ(pi) for jobs in S is maximized

This is a variant of the weighted job scheduling problem with deadlines.
"""

import time
import json
from typing import List, Tuple, Dict
import random


class Packet:
    """Represents a network packet with deadline, priority, and transmission time"""
    
    def __init__(self, packet_id: int, deadline: int, priority: int, transmission_time: int):
        self.id = packet_id
        self.deadline = deadline
        self.priority = priority
        self.transmission_time = transmission_time
    
    def __repr__(self):
        return f"Packet({self.id}, d={self.deadline}, p={self.priority}, t={self.transmission_time})"


def greedy_packet_scheduling(packets: List[Packet]) -> Tuple[List[Packet], int, float]:
    """
    Greedy Algorithm for Packet Scheduling
    
    Strategy: Sort packets by priority/time ratio (priority density) in descending order,
    then greedily select packets that can meet their deadlines.
    
    Algorithm:
    1. Sort packets by priority density (priority/transmission_time) in descending order
    2. Initialize current_time = 0, scheduled = []
    3. For each packet in sorted order:
        a. If current_time + transmission_time <= deadline:
            - Schedule the packet
            - Update current_time
    4. Return scheduled packets and total priority
    
    Time Complexity Analysis:
    - Sorting: O(n log n) where n is the number of packets
    - Iteration and selection: O(n)
    - Total: O(n log n)
    
    Space Complexity: O(n) for storing the sorted list and scheduled packets
    
    Args:
        packets: List of Packet objects
    
    Returns:
        Tuple of (scheduled_packets, total_priority, execution_time)
    """
    start_time = time.perf_counter()
    
    # Sort by priority density (priority per unit time) in descending order
    # Ties broken by earliest deadline (EDF - Earliest Deadline First)
    sorted_packets = sorted(
        packets,
        key=lambda p: (p.priority / p.transmission_time, -p.deadline),
        reverse=True
    )
    
    scheduled = []
    current_time = 0
    total_priority = 0
    
    for packet in sorted_packets:
        # Check if packet can be scheduled before its deadline
        if current_time + packet.transmission_time <= packet.deadline:
            scheduled.append(packet)
            current_time += packet.transmission_time
            total_priority += packet.priority
    
    execution_time = time.perf_counter() - start_time
    
    return scheduled, total_priority, execution_time


def verify_schedule(scheduled: List[Packet]) -> bool:
    """
    Verify that a schedule is valid (no deadline violations)
    
    Args:
        scheduled: List of scheduled packets in order
    
    Returns:
        True if valid, False otherwise
    """
    current_time = 0
    for packet in scheduled:
        current_time += packet.transmission_time
        if current_time > packet.deadline:
            return False
    return True


def generate_test_case(n: int, max_deadline: int = None, seed: int = None) -> List[Packet]:
    """
    Generate a random test case with n packets
    
    Args:
        n: Number of packets
        max_deadline: Maximum deadline value (default: 2*n)
        seed: Random seed for reproducibility
    
    Returns:
        List of Packet objects
    """
    if seed is not None:
        random.seed(seed)
    
    if max_deadline is None:
        max_deadline = 2 * n
    
    packets = []
    for i in range(n):
        transmission_time = random.randint(1, 10)
        deadline = random.randint(transmission_time, max_deadline)
        priority = random.randint(1, 100)
        packets.append(Packet(i, deadline, priority, transmission_time))
    
    return packets


def run_experiments(sizes: List[int], trials: int = 5) -> Dict:
    """
    Run experiments with different input sizes
    
    Args:
        sizes: List of input sizes to test
        trials: Number of trials per size
    
    Returns:
        Dictionary with experimental results
    """
    results = {
        "algorithm": "Greedy Packet Scheduling",
        "complexity": "O(n log n)",
        "experiments": []
    }
    
    for n in sizes:
        print(f"Running experiments for n={n}...")
        size_results = {
            "input_size": n,
            "trials": []
        }
        
        for trial in range(trials):
            packets = generate_test_case(n, seed=trial * n)
            scheduled, total_priority, exec_time = greedy_packet_scheduling(packets)
            
            is_valid = verify_schedule(scheduled)
            
            trial_result = {
                "trial": trial + 1,
                "total_packets": n,
                "scheduled_packets": len(scheduled),
                "total_priority": total_priority,
                "execution_time_ms": exec_time * 1000,
                "valid": is_valid
            }
            size_results["trials"].append(trial_result)
        
        # Calculate averages
        avg_exec_time = sum(t["execution_time_ms"] for t in size_results["trials"]) / trials
        avg_scheduled = sum(t["scheduled_packets"] for t in size_results["trials"]) / trials
        avg_priority = sum(t["total_priority"] for t in size_results["trials"]) / trials
        
        size_results["average_execution_time_ms"] = avg_exec_time
        size_results["average_scheduled_packets"] = avg_scheduled
        size_results["average_total_priority"] = avg_priority
        
        results["experiments"].append(size_results)
        print(f"  Average execution time: {avg_exec_time:.4f} ms")
    
    return results


def demonstrate_algorithm():
    """Demonstrate the algorithm with a small example"""
    print("=" * 80)
    print("GREEDY PACKET SCHEDULING DEMONSTRATION")
    print("=" * 80)
    
    # Create a small example
    packets = [
        Packet(0, deadline=10, priority=50, transmission_time=3),
        Packet(1, deadline=8, priority=40, transmission_time=2),
        Packet(2, deadline=15, priority=60, transmission_time=5),
        Packet(3, deadline=6, priority=30, transmission_time=2),
        Packet(4, deadline=12, priority=45, transmission_time=3),
    ]
    
    print("\nInput Packets:")
    print(f"{'ID':<5} {'Deadline':<10} {'Priority':<10} {'Time':<10} {'Density':<10}")
    print("-" * 55)
    for p in packets:
        density = p.priority / p.transmission_time
        print(f"{p.id:<5} {p.deadline:<10} {p.priority:<10} {p.transmission_time:<10} {density:<10.2f}")
    
    scheduled, total_priority, exec_time = greedy_packet_scheduling(packets)
    
    print(f"\nScheduled Packets (Total Priority: {total_priority}):")
    print(f"{'ID':<5} {'Deadline':<10} {'Priority':<10} {'Time':<10} {'Finish Time':<15}")
    print("-" * 60)
    current_time = 0
    for p in scheduled:
        current_time += p.transmission_time
        print(f"{p.id:<5} {p.deadline:<10} {p.priority:<10} {p.transmission_time:<10} {current_time:<15}")
    
    print(f"\nExecution Time: {exec_time * 1000:.4f} ms")
    print(f"Valid Schedule: {verify_schedule(scheduled)}")
    print()


if __name__ == "__main__":
    # Demonstrate the algorithm
    demonstrate_algorithm()
    
    # Run experiments
    print("=" * 80)
    print("RUNNING EXPERIMENTS")
    print("=" * 80)
    print()
    
    # Test with increasing input sizes
    sizes = [10, 50, 100, 500, 1000, 2000, 5000, 10000]
    results = run_experiments(sizes, trials=5)
    
    # Save results to JSON
    output_file = "greedy_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {output_file}")
    print("\nSummary of Experiments:")
    print(f"{'Input Size':<15} {'Avg Time (ms)':<20} {'Avg Scheduled':<20}")
    print("-" * 55)
    for exp in results["experiments"]:
        print(f"{exp['input_size']:<15} {exp['average_execution_time_ms']:<20.4f} {exp['average_scheduled_packets']:<20.1f}")

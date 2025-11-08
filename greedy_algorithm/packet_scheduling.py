"""
Network Packet Scheduling - Greedy Algorithm (UNIT-TIME PACKETS)

Real Problem:
In modern network routers and switches, fixed-size control packets arrive continuously 
and need to be transmitted through a network interface. Each packet has a deadline 
(by which it must be transmitted to avoid timeout) and a priority level (critical 
network control data, routing updates, keepalive signals, etc.). All packets have 
the same transmission time (e.g., fixed-size 64-byte control frames).

The router must decide which packets to transmit to maximize the total priority value 
of successfully transmitted packets before their deadlines.

This is critical in Quality of Service (QoS) systems for control plane traffic in 
telecommunications networks, IoT networks, and SDN (Software-Defined Networking) 
systems where control messages are standardized sizes.

Abstract Problem:
Given a set of jobs J = {j1, j2, ..., jn} where each job ji has:
- deadline di (time unit by which it must complete, di ∈ {1, 2, ..., n})
- priority/value pi (importance of the job)
- processing time ti = 1 (UNIT TIME - all jobs take exactly 1 time unit)

Find a subset S ⊆ J and an ordering/schedule of jobs in S such that:
1. No job in S misses its deadline
2. The sum of priorities Σ(pi) for jobs in S is maximized

This is the classic weighted job scheduling problem with unit-time jobs and deadlines,
which admits an optimal greedy solution.
"""

import time
import json
from typing import List, Tuple, Dict
import random


class Packet:
    """Represents a unit-time network packet with deadline and priority"""
    
    def __init__(self, packet_id: int, deadline: int, priority: int):
        self.id = packet_id
        self.deadline = deadline
        self.priority = priority
        self.transmission_time = 1  # UNIT TIME: all packets take exactly 1 time unit
    
    def __repr__(self):
        return f"Packet({self.id}, d={self.deadline}, p={self.priority})"


def greedy_packet_scheduling(packets: List[Packet]) -> Tuple[List[Packet], int, float]:
    """
    Optimal Greedy Algorithm for Unit-Time Packet Scheduling
    
    Strategy: Sort packets by priority (descending). For each packet, schedule it in 
    the latest available time slot that is <= its deadline.
    
    Algorithm (Latest-Slot Assignment):
    1. Sort packets by priority in descending order
    2. Initialize: slot[t] = None for all time slots t = 1, 2, ..., max_deadline
    3. For each packet p in sorted order:
        a. Find the latest free slot t where 1 <= t <= p.deadline and slot[t] is free
        b. If such slot exists:
            - Assign packet p to slot[t]
        c. Else: skip packet (cannot meet deadline)
    4. Return scheduled packets and total priority
    
    This is optimal: by scheduling high-priority packets first and placing them as 
    late as possible, we preserve earlier slots for other packets.
    
    Time Complexity Analysis:
    - Sorting: O(n log n) where n is the number of packets
    - For each packet: find latest free slot
      * Naive: O(n) per packet -> O(n²) total
      * With Union-Find (DSU): O(n α(n)) ≈ O(n) amortized per packet
    - Total with DSU optimization: O(n log n)
    - Total without DSU: O(n²) worst case, but acceptable for practical sizes
    
    Space Complexity: O(d) where d is the maximum deadline
    
    Args:
        packets: List of Packet objects (all with transmission_time = 1)
    
    Returns:
        Tuple of (scheduled_packets, total_priority, execution_time)
    """
    start_time = time.perf_counter()
    
    if not packets:
        return [], 0, time.perf_counter() - start_time
    
    # Sort by priority in descending order (highest priority first)
    sorted_packets = sorted(packets, key=lambda p: p.priority, reverse=True)
    
    # Find max deadline to allocate slot array
    max_deadline = max(p.deadline for p in packets)
    
    # Initialize slots: slot[t] = packet assigned to time slot t (1-indexed)
    # slot[0] is unused, slots are 1, 2, ..., max_deadline
    slots = [None] * (max_deadline + 1)
    
    scheduled = []
    total_priority = 0
    
    # For each packet in priority order
    for packet in sorted_packets:
        # Find the latest free slot <= packet.deadline
        slot_found = None
        for t in range(packet.deadline, 0, -1):
            if slots[t] is None:
                slot_found = t
                break
        
        if slot_found is not None:
            # Schedule packet in this slot
            slots[slot_found] = packet
            scheduled.append(packet)
            total_priority += packet.priority
    
    execution_time = time.perf_counter() - start_time
    
    # Sort scheduled packets by their assigned time slot for output clarity
    scheduled_with_slots = [(slots.index(p), p) for p in scheduled]
    scheduled_with_slots.sort()
    scheduled_ordered = [p for _, p in scheduled_with_slots]
    
    return scheduled_ordered, total_priority, execution_time


def verify_schedule(scheduled: List[Packet]) -> bool:
    """
    Verify that a schedule is valid (no deadline violations)
    
    For unit-time packets, each packet occupies exactly one time slot.
    We verify that each packet's slot number <= its deadline.
    
    Args:
        scheduled: List of scheduled packets (should be in time-slot order)
    
    Returns:
        True if valid, False otherwise
    """
    # Packets are scheduled in time slots 1, 2, 3, ...
    for slot_number, packet in enumerate(scheduled, start=1):
        if slot_number > packet.deadline:
            return False
    return True


def generate_test_case(n: int, max_deadline: int = None, seed: int = None) -> List[Packet]:
    """
    Generate a random test case with n unit-time packets
    
    Args:
        n: Number of packets
        max_deadline: Maximum deadline value (default: n)
        seed: Random seed for reproducibility
    
    Returns:
        List of Packet objects (all with transmission_time = 1)
    """
    if seed is not None:
        random.seed(seed)
    
    if max_deadline is None:
        max_deadline = n  # Reasonable default: deadline in range [1, n]
    
    packets = []
    for i in range(n):
        # Unit-time packets: transmission_time = 1
        # Deadline: must be at least 1, at most max_deadline
        deadline = random.randint(1, max_deadline)
        priority = random.randint(1, 100)
        packets.append(Packet(i, deadline, priority))
    
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
        "algorithm": "Greedy Unit-Time Packet Scheduling (Latest-Slot Assignment)",
        "complexity": "O(n^2) worst case, O(n log n) with DSU optimization",
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
    print("GREEDY UNIT-TIME PACKET SCHEDULING DEMONSTRATION")
    print("=" * 80)
    
    # Create a small example
    packets = [
        Packet(0, deadline=3, priority=50),
        Packet(1, deadline=2, priority=40),
        Packet(2, deadline=4, priority=60),
        Packet(3, deadline=2, priority=30),
        Packet(4, deadline=3, priority=45),
    ]
    
    print("\nInput Packets (all transmission_time = 1):")
    print(f"{'ID':<5} {'Deadline':<10} {'Priority':<10}")
    print("-" * 25)
    for p in packets:
        print(f"{p.id:<5} {p.deadline:<10} {p.priority:<10}")
    
    scheduled, total_priority, exec_time = greedy_packet_scheduling(packets)
    
    print(f"\nScheduled Packets (Total Priority: {total_priority}):")
    print(f"{'Time Slot':<12} {'Packet ID':<12} {'Deadline':<12} {'Priority':<10}")
    print("-" * 46)
    for slot, p in enumerate(scheduled, start=1):
        print(f"{slot:<12} {p.id:<12} {p.deadline:<12} {p.priority:<10}")
    
    print(f"\nExecution Time: {exec_time * 1000:.4f} ms")
    print(f"Valid Schedule: {verify_schedule(scheduled)}")
    print(f"Scheduled {len(scheduled)} out of {len(packets)} packets")
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
    sizes = [10, 50, 100, 500, 1000, 2000, 5000, 10000, 20000]
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

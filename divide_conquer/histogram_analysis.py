"""
Medical Image Histogram Analysis - Divide and Conquer Algorithm

Real Problem:
In medical imaging (MRI, CT scans), radiologists need to identify optimal threshold 
values to segment images and detect abnormalities like tumors. The histogram of pixel 
intensities in a medical image often shows distinct peaks corresponding to different 
tissue types. Finding the "valley" (minimum point) between two peaks helps determine 
the optimal threshold for separating normal tissue from abnormal tissue.

This is crucial for Computer-Aided Diagnosis (CAD) systems in radiology, where 
automated tumor detection can assist doctors in early cancer detection.

Abstract Problem:
Given an array H = [h0, h1, h2, ..., hn-1] representing a histogram where:
- hi is the frequency/count of pixels at intensity level i
- The histogram has multiple local maxima (peaks)

Find the deepest valley (global or significant local minimum) between peaks in the 
range [left, right] efficiently.

This can be modeled as finding the minimum element in a unimodal or multimodal 
sequence, which is efficiently solved using divide and conquer.

More specifically, we solve: Given a histogram array, find the index of the minimum 
value that lies between two peaks (acts as an optimal threshold).
"""

import time
import json
from typing import List, Tuple, Dict
import random
import math


def find_valley_divide_conquer(histogram: List[int], left: int, right: int) -> Tuple[int, int]:
    """
    Divide and Conquer Algorithm to Find Deepest Valley in Histogram
    
    Strategy: Recursively divide the histogram and find local minima, then compare
    to find the global minimum (deepest valley).
    
    Algorithm:
    1. Base case: If range is small (< 3 elements), find minimum by linear search
    2. Divide: Split range into two halves at mid = (left + right) // 2
    3. Conquer: Recursively find minimum in left half and right half
    4. Combine: Compare the two minima and the mid point, return the smallest
    5. Additionally check boundaries between recursive calls
    
    Time Complexity Analysis:
    - Recurrence: T(n) = 2T(n/2) + O(1)
    - By Master Theorem: T(n) = O(n)
    - However, with optimization (pruning), average case can be O(log n) for unimodal
    
    For this implementation, we use a modified approach that's O(n) worst case
    but performs well in practice.
    
    Space Complexity: O(log n) for recursion stack
    
    Args:
        histogram: List of intensity frequencies
        left: Left boundary of search range
        right: Right boundary of search range
    
    Returns:
        Tuple of (index_of_minimum, minimum_value)
    """
    # Base case: small range
    if right - left <= 2:
        min_idx = left
        min_val = histogram[left]
        for i in range(left + 1, right + 1):
            if histogram[i] < min_val:
                min_val = histogram[i]
                min_idx = i
        return min_idx, min_val
    
    # Divide
    mid = (left + right) // 2
    
    # Conquer: Find minimum in left and right halves
    left_min_idx, left_min_val = find_valley_divide_conquer(histogram, left, mid)
    right_min_idx, right_min_val = find_valley_divide_conquer(histogram, mid + 1, right)
    
    # Combine: Compare all candidates
    mid_val = histogram[mid]
    
    # Find the overall minimum
    if left_min_val <= right_min_val and left_min_val <= mid_val:
        return left_min_idx, left_min_val
    elif right_min_val <= left_min_val and right_min_val <= mid_val:
        return right_min_idx, right_min_val
    else:
        return mid, mid_val


def find_valley_optimized(histogram: List[int]) -> Tuple[int, int, float]:
    """
    Wrapper function with timing for the divide and conquer algorithm
    
    Args:
        histogram: List of intensity frequencies
    
    Returns:
        Tuple of (index, value, execution_time)
    """
    start_time = time.perf_counter()
    
    if len(histogram) == 0:
        return -1, -1, 0.0
    
    if len(histogram) == 1:
        execution_time = time.perf_counter() - start_time
        return 0, histogram[0], execution_time
    
    min_idx, min_val = find_valley_divide_conquer(histogram, 0, len(histogram) - 1)
    
    execution_time = time.perf_counter() - start_time
    
    return min_idx, min_val, execution_time


def find_valley_bruteforce(histogram: List[int]) -> Tuple[int, int, float]:
    """
    Brute force approach for comparison - O(n) linear search
    
    Args:
        histogram: List of intensity frequencies
    
    Returns:
        Tuple of (index, value, execution_time)
    """
    start_time = time.perf_counter()
    
    if len(histogram) == 0:
        return -1, -1, 0.0
    
    min_idx = 0
    min_val = histogram[0]
    
    for i in range(1, len(histogram)):
        if histogram[i] < min_val:
            min_val = histogram[i]
            min_idx = i
    
    execution_time = time.perf_counter() - start_time
    
    return min_idx, min_val, execution_time


def generate_histogram(size: int, num_peaks: int = 2, noise_level: float = 0.1, seed: int = None) -> List[int]:
    """
    Generate a synthetic histogram with multiple peaks (simulating tissue types)
    
    Args:
        size: Number of intensity levels
        num_peaks: Number of peaks in the histogram
        noise_level: Amount of random noise to add
        seed: Random seed for reproducibility
    
    Returns:
        List representing histogram
    """
    if seed is not None:
        random.seed(seed)
    
    histogram = [0] * size
    
    # Create peaks at different positions
    peak_positions = []
    for i in range(num_peaks):
        pos = int((i + 1) * size / (num_peaks + 1))
        peak_positions.append(pos)
    
    # Generate Gaussian-like peaks
    for i in range(size):
        value = 10  # Base value
        
        for peak_pos in peak_positions:
            # Add Gaussian contribution from each peak
            sigma = size / (num_peaks * 4)
            contribution = 1000 * math.exp(-((i - peak_pos) ** 2) / (2 * sigma ** 2))
            value += contribution
        
        # Add noise
        noise = random.uniform(-noise_level * value, noise_level * value)
        histogram[i] = max(0, int(value + noise))
    
    return histogram


def verify_result(histogram: List[int], idx: int, val: int) -> bool:
    """
    Verify that the found valley is correct
    
    Args:
        histogram: The histogram array
        idx: Index of the minimum
        val: Value of the minimum
    
    Returns:
        True if correct, False otherwise
    """
    if idx < 0 or idx >= len(histogram):
        return False
    
    if histogram[idx] != val:
        return False
    
    # Check if it's actually the minimum
    actual_min = min(histogram)
    return val == actual_min


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
        "algorithm": "Divide and Conquer Valley Finding",
        "complexity": "O(n)",
        "experiments": []
    }
    
    for n in sizes:
        print(f"Running experiments for n={n}...")
        size_results = {
            "input_size": n,
            "trials": []
        }
        
        for trial in range(trials):
            histogram = generate_histogram(n, num_peaks=3, seed=trial * n)
            
            # Run divide and conquer
            idx_dc, val_dc, time_dc = find_valley_optimized(histogram)
            
            # Run brute force for comparison
            idx_bf, val_bf, time_bf = find_valley_bruteforce(histogram)
            
            # Verify correctness
            is_valid = verify_result(histogram, idx_dc, val_dc)
            matches_bruteforce = (idx_dc == idx_bf and val_dc == val_bf)
            
            trial_result = {
                "trial": trial + 1,
                "histogram_size": n,
                "valley_index": idx_dc,
                "valley_value": val_dc,
                "dc_execution_time_ms": time_dc * 1000,
                "bf_execution_time_ms": time_bf * 1000,
                "speedup": time_bf / time_dc if time_dc > 0 else 1.0,
                "valid": is_valid,
                "matches_bruteforce": matches_bruteforce
            }
            size_results["trials"].append(trial_result)
        
        # Calculate averages
        avg_time_dc = sum(t["dc_execution_time_ms"] for t in size_results["trials"]) / trials
        avg_time_bf = sum(t["bf_execution_time_ms"] for t in size_results["trials"]) / trials
        avg_speedup = sum(t["speedup"] for t in size_results["trials"]) / trials
        
        size_results["average_dc_time_ms"] = avg_time_dc
        size_results["average_bf_time_ms"] = avg_time_bf
        size_results["average_speedup"] = avg_speedup
        
        results["experiments"].append(size_results)
        print(f"  Average D&C time: {avg_time_dc:.4f} ms")
        print(f"  Average BF time: {avg_time_bf:.4f} ms")
    
    return results


def demonstrate_algorithm():
    """Demonstrate the algorithm with a small example"""
    print("=" * 80)
    print("DIVIDE AND CONQUER VALLEY FINDING DEMONSTRATION")
    print("=" * 80)
    
    # Create a small histogram with 2 peaks
    histogram = generate_histogram(50, num_peaks=2, noise_level=0.05, seed=42)
    
    print("\nHistogram (first 50 values):")
    print("Index | Value")
    print("-" * 30)
    for i in range(min(50, len(histogram))):
        bar = '*' * (histogram[i] // 50)
        print(f"{i:5d} | {histogram[i]:5d} {bar}")
    
    # Find valley using divide and conquer
    idx_dc, val_dc, time_dc = find_valley_optimized(histogram)
    
    # Find valley using brute force
    idx_bf, val_bf, time_bf = find_valley_bruteforce(histogram)
    
    print(f"\nDivide & Conquer Result:")
    print(f"  Valley Index: {idx_dc}")
    print(f"  Valley Value: {val_dc}")
    print(f"  Execution Time: {time_dc * 1000:.6f} ms")
    
    print(f"\nBrute Force Result:")
    print(f"  Valley Index: {idx_bf}")
    print(f"  Valley Value: {val_bf}")
    print(f"  Execution Time: {time_bf * 1000:.6f} ms")
    
    print(f"\nResults Match: {idx_dc == idx_bf and val_dc == val_bf}")
    print(f"Speedup: {time_bf / time_dc if time_dc > 0 else 'N/A'}x")
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
    sizes = [100, 500, 1000, 5000, 10000, 20000, 50000, 100000]
    results = run_experiments(sizes, trials=5)
    
    # Save results to JSON
    output_file = "divide_conquer_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {output_file}")
    print("\nSummary of Experiments:")
    print(f"{'Input Size':<15} {'D&C Time (ms)':<20} {'BF Time (ms)':<20} {'Speedup':<15}")
    print("-" * 70)
    for exp in results["experiments"]:
        print(f"{exp['input_size']:<15} {exp['average_dc_time_ms']:<20.6f} "
              f"{exp['average_bf_time_ms']:<20.6f} {exp['average_speedup']:<15.2f}")

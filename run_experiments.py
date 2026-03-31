import argparse
import random
import time
import numpy as np
import matplotlib.pyplot as plt
import sys

# ==========================================
# Part A - Algorithm Implementation
# ==========================================

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def quick_sort(arr):
    _quick_sort_recursive(arr, 0, len(arr) - 1)

def _quick_sort_recursive(arr, low, high):
    if low < high:
        pi = _partition(arr, low, high)
        _quick_sort_recursive(arr, low, pi - 1)
        _quick_sort_recursive(arr, pi + 1, high)

def _partition(arr, low, high):
    # Using random pivot to avoid worst-case O(n^2) on nearly sorted arrays
    pivot_idx = random.randint(low, high)
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
    
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# Dictionary to map IDs to functions and names
ALGORITHMS = {
    2: ("Selection Sort", selection_sort),
    4: ("Merge Sort", merge_sort),
    5: ("Quick Sort", quick_sort)
}

# ==========================================
# Helper Functions for Experiments
# ==========================================

def generate_array(size, exp_type):
    """
    Generates an array based on the experiment type.
    exp_type: 0 (Random), 1 (5% noise), 2 (20% noise)
    """
    if exp_type == 0:
        return [random.randint(0, 100000) for _ in range(size)]
    
    # Parts C - Nearly sorted arrays
    arr = list(range(size))
    noise_level = 0.05 if exp_type == 1 else 0.20
    num_swaps = int(size * noise_level)
    
    for _ in range(num_swaps):
        i, j = random.randint(0, size - 1), random.randint(0, size - 1)
        arr[i], arr[j] = arr[j], arr[i]
        
    return arr

def run_experiment(algo_func, array_sizes, exp_type, repetitions):
    results_mean = []
    results_std = []
    
    for size in array_sizes:
        times = []
        for _ in range(repetitions):
            # Generate a fresh array for each repetition
            arr = generate_array(size, exp_type)
            
            # Measure time
            start_time = time.perf_counter()
            algo_func(arr)
            end_time = time.perf_counter()
            
            times.append(end_time - start_time)
            
        results_mean.append(np.mean(times))
        results_std.append(np.std(times))
        
    return results_mean, results_std

# ==========================================
# Main Execution & CLI (Part D)
# ==========================================

def main():
    parser = argparse.ArgumentParser(description="Sorting Algorithms Experiment Runner")
    parser.add_argument('-a', '--algorithms', nargs='+', type=int, required=True, 
                        help="List of algorithm IDs (e.g., -a 2 4 5)")
    parser.add_argument('-s', '--sizes', nargs='+', type=int, required=True, 
                        help="List of array sizes (e.g., -s 100 500 1000)")
    parser.add_argument('-e', '--experiment', type=int, default=0, choices=[0, 1, 2],
                        help="0: Random, 1: 5% noise, 2: 20% noise")
    parser.add_argument('-r', '--repetitions', type=int, default=10, 
                        help="Number of repetitions per size")
    
    args = parser.parse_args()
    
    # Setting up the plot
    plt.figure(figsize=(10, 6))
    
    # Titles and file names based on experiment type
    if args.experiment == 0:
        title = "Runtime Comparison (Random Arrays)"
        filename = "result1.png"
    elif args.experiment == 1:
        title = "Runtime Comparison (Nearly Sorted, 5% Noise)"
        filename = "result2.png"
    else:
        title = "Runtime Comparison (Nearly Sorted, 20% Noise)"
        filename = "result2_20_percent.png"

    plt.title(title)
    plt.xlabel("Array size (n)")
    plt.ylabel("Runtime (seconds)")
    
    for algo_id in args.algorithms:
            
        algo_name, algo_func = ALGORITHMS[algo_id]
        print(f"Running experiments for {algo_name}...")
        
        # In python, deep recursion can crash Quick Sort on large arrays. 
        # Increasing recursion limit for safety.
        sys.setrecursionlimit(max(sys.getrecursionlimit(), max(args.sizes) * 2))
        
        means, stds = run_experiment(algo_func, args.sizes, args.experiment, args.repetitions)
        
        # Plotting with standard deviation shading
        means = np.array(means)
        stds = np.array(stds)
        plt.plot(args.sizes, means, marker='o', label=algo_name)
        plt.fill_between(args.sizes, means - stds, means + stds, alpha=0.2)
        
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(filename)
    print(f"Experiment complete! Plot saved to {filename}")

if __name__ == "__main__":
    main()
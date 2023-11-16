import timeit
import matplotlib.pyplot as plt
from copy import deepcopy

def range_addition(
    ranges_a: list[list[int]],
    ranges_b: list[list[int]]
) -> tuple[list[list[int]], list[list[int]]]:
    """Addition between two validated list of ranges.
     Simulates the addition between two sets.
     Return[adittion product, intersection]"""
    if not ranges_b:
        return deepcopy(ranges_a), []
    if not ranges_a:
        return deepcopy(ranges_b), []
    result = []
    conflict = []
    a_i = b_i = 0
    len_a = len(ranges_a)
    len_b = len(ranges_b)
    while a_i < len_a or b_i < len_b:
        if (a_i < len_a and
                (b_i >= len_b or ranges_a[a_i][1] < ranges_b[b_i][0] - 1)):
            result.append(ranges_a[a_i])
            a_i += 1
        elif (b_i < len_b and
                (a_i >= len_a or ranges_b[b_i][1] < ranges_a[a_i][0] - 1)):
            result.append(ranges_b[b_i])
            b_i += 1
        # Intersection and continuos ranges
        else:
            fst = max(ranges_a[a_i][0], ranges_b[b_i][0])
            snd = min(ranges_a[a_i][1], ranges_b[b_i][1])
            if fst <= snd:
                conflict.append([fst, snd])
            new_range = [
                min(ranges_a[a_i][0], ranges_b[b_i][0]),
                max(ranges_a[a_i][1], ranges_b[b_i][1])
            ]
            a_i += 1
            b_i += 1
            while a_i < len_a or b_i < len_b:
                if a_i < len_a and (ranges_a[a_i][0] <= new_range[1] + 1):
                    if ranges_a[a_i][0] <= new_range[1]:
                        conflict.append([
                            max(ranges_a[a_i][0], new_range[0]),
                            min(ranges_a[a_i][1], new_range[1])
                        ])
                    new_range[1] = max(ranges_a[a_i][1], new_range[1])
                    a_i += 1
                elif b_i < len_b and (ranges_b[b_i][0] <= new_range[1] + 1):
                    if ranges_b[b_i][0] <= new_range[1]:
                        conflict.append([
                            max(ranges_b[b_i][0], new_range[0]),
                            min(ranges_b[b_i][1], new_range[1])
                        ])
                    new_range[1] = max(ranges_b[b_i][1], new_range[1])
                    b_i += 1
                else:
                    break
            result.append(new_range)
    return result, conflict


def my_function(args, available):
    # Your method or code to be measured goes here
    result = range_addition(args, available)
    return result

def measure_time(func, *args):
    # Measure the execution time of the given function with arguments
    start_time = timeit.default_timer()
    result = func(*args)
    end_time = timeit.default_timer()
    execution_time = end_time - start_time
    return result, execution_time

def ploting_1():
    """
    1. No conflicts, 1024 ranges:
    available = [[1, 2], [5, 6], ... ]
    tags = [[3, 4], [7, 8], ... ]
    """
    available = []
    tags = []
    for i in range(1, 4096, 4):
        available.append([i, i+1])
        tags.append([i+2, i+3])
    arguments = (available, tags)  # Adjust the arguments as needed
    results = []
    execution_times = []

    # Repeat measurements for better accuracy
    num_measurements = 50
    for _ in range(num_measurements):
        result, execution_time = measure_time(my_function, *arguments)
        results.append(result)
        execution_times.append(execution_time)

    # Plot the execution times
    plt.plot(range(1, num_measurements + 1), execution_times, marker='o')
    plt.title('Execution Times')
    plt.xlabel('Measurement')
    plt.ylabel('Time (seconds)')

    # Save the plot to a file (e.g., PNG)
    plt.savefig('ploting_1.png')

    # Close the plot
    plt.close()

def ploting_2():
    """
    2. Conflicts, 1024 ranges:
    available = [[1, 2], [4, 6], ... ]
    tags = [[2, 4], [6, 8], ... ]
    conflicts = [[2, 2], [6, 6] ... ]
    """
    available = []
    tags = []
    for i in range(1, 4096, 4):
        available.append([i, i+1])
        tags.append([i+1, i+2])
    arguments = (available, tags)  # Adjust the arguments as needed
    results = []
    execution_times = []

    # Repeat measurements for better accuracy
    num_measurements = 50
    for _ in range(num_measurements):
        result, execution_time = measure_time(my_function, *arguments)
        results.append(result)
        execution_times.append(execution_time)

    # Plot the execution times
    plt.plot(range(1, num_measurements + 1), execution_times, marker='o')
    plt.title('Execution Times')
    plt.xlabel('Measurement')
    plt.ylabel('Time (seconds)')

    # Save the plot to a file (e.g., PNG)
    plt.savefig('ploting_2.png')

    # Close the plot
    plt.close()

def ploting_3():
    """
    3. Conflicts, 1024 available ranges and 2047 tag ranges: 
    available = [[2, 2], [6, 6], [10, 10]... ]
    tags = [[1, 1], [3, 3], [6, 6]... ]
    conflicts = [[6, 6], [10, 10], ... ]
    """
    available = []
    tags = []
    available = [[n, n] for n in range(2, 4095, 4)]
    tags = [[n, n] for n in range(1, 4095, 2)]
    arguments = (available, tags)  # Adjust the arguments as needed
    results = []
    execution_times = []

    # Repeat measurements for better accuracy
    num_measurements = 50
    for _ in range(num_measurements):
        result, execution_time = measure_time(my_function, *arguments)
        results.append(result)
        execution_times.append(execution_time)

    # Plot the execution times
    plt.plot(range(1, num_measurements + 1), execution_times, marker='o')
    plt.title('Execution Times')
    plt.xlabel('Measurement')
    plt.ylabel('Time (seconds)')

    # Save the plot to a file (e.g., PNG)
    plt.savefig('ploting_3.png')

    # Close the plot
    plt.close()

def ploting_4():
    """
    4. Conflicts, 8 available ranges and 7 tag ranges: 
    available = [[3, 10], [20, 50], [60, 70], [80, 90], [100, 110], [112, 120], [130, 140], [150, 160]]
    tags = [[1, 1], [3,3], [9, 22], [24, 55], [57, 62], [81, 101], [123, 128]]
    conflicts = [[3, 3], [9, 10], [20, 22], [24, 50], [60, 62], [81, 90], [100, 101]]
    """
    available = [[3, 10], [20, 50], [60, 70], [80, 90], [100, 110], [112, 120], [130, 140], [150, 160]]
    tags = [[1, 1], [3,3], [9, 22], [24, 55], [57, 62], [81, 101], [123, 128]]
    arguments = (available, tags)  # Adjust the arguments as needed
    results = []
    execution_times = []

    # Repeat measurements for better accuracy
    num_measurements = 50
    for _ in range(num_measurements):
        result, execution_time = measure_time(my_function, *arguments)
        results.append(result)
        execution_times.append(execution_time)

    # Plot the execution times
    plt.plot(range(1, num_measurements + 1), execution_times, marker='o')
    plt.title('Execution Times')
    plt.xlabel('Measurement')
    plt.ylabel('Time (seconds)')

    # Save the plot to a file (e.g., PNG)
    plt.savefig('ploting_4.png')

    # Close the plot
    plt.close()

def ploting_5():
    """
    5. Conflicts, 3 available ranges and 1 tag ranges: 
    available = [[3, 10], [20, 30], [40, 50]]
    tags = [[5, 18]]
    conflicts = [[5, 10]]
    """
    available= [[3, 10], [20, 30], [40, 50]]
    tags = [[5, 18]]
    arguments = (available, tags)  # Adjust the arguments as needed
    results = []
    execution_times = []

    # Repeat measurements for better accuracy
    num_measurements = 50
    for _ in range(num_measurements):
        result, execution_time = measure_time(my_function, *arguments)
        results.append(result)
        execution_times.append(execution_time)

    # Plot the execution times
    plt.plot(range(1, num_measurements + 1), execution_times, marker='o')
    plt.title('Execution Times')
    plt.xlabel('Measurement')
    plt.ylabel('Time (seconds)')

    # Save the plot to a file (e.g., PNG)
    plt.savefig('ploting_5.png')

    # Close the plot
    plt.close()

# Example usage:
if __name__ == "__main__":
    ploting_1()
    ploting_2()
    ploting_3()
    ploting_4()
    ploting_5()
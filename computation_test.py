import numpy as np
import matplotlib.pyplot as plt
import time


def measure_time(operation, size, dimensions, iterations=8):
    times = []
    for _ in range(iterations):
        if dimensions == 1:
            a = np.random.rand(size)
            b = np.random.rand(size)
        elif dimensions == 2:
            a = np.random.rand(size, size)
            b = np.random.rand(size, size)
        elif dimensions == 3:
            a = np.random.rand(size, size, size)
            b = np.random.rand(size, size, size)

        start_time = time.time()
        operation(a, b)
        times.append(time.time() - start_time)

    return np.mean(times), np.std(times)

def element_multiply(a, b):
    if a.ndim == 1:
        return [x * y for x, y in zip(a, b)]
    elif a.ndim == 2:
        return [[x * y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]
    elif a.ndim == 3:
        return [[[x * y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(mat_a, mat_b)]
                 for mat_a, mat_b in zip(a, b)]

sizes = range(50,151,20 )
dimensions = [1, 2, 3]

list_times = {dim: [] for dim in dimensions}
list_errors = {dim: [] for dim in dimensions}
array_times = {dim: [] for dim in dimensions}
array_errors = {dim: [] for dim in dimensions}

for dim in dimensions:
    for size in sizes:
        mean_time, std_time = measure_time(element_multiply, size, dim)
        list_times[dim].append(mean_time)
        list_errors[dim].append(std_time)

for dim in dimensions:
    for size in sizes:
        mean_time, std_time = measure_time(np.multiply, size, dim)
        array_times[dim].append(mean_time)
        array_errors[dim].append(std_time)

plt.figure(figsize=(10, 12))

plt.subplot(2, 1, 1)
for dim in dimensions:
    plt.errorbar(sizes, list_times[dim], yerr=list_errors[dim], label=f'Lists - Dim {dim}', fmt='o')

    coeffs = np.polyfit(sizes, list_times[dim], deg=3)
    poly_appr = np.poly1d(coeffs)
    plt.plot(range(50,151,1 ), poly_appr(range(50,151,1 )), linestyle='--', label=f'Fit - Lists Dim {dim}')

plt.title('Lists')
plt.xlabel('Size')
plt.ylabel('Time (seconds)')
plt.yscale('log')
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
for dim in dimensions:
    plt.errorbar(sizes, array_times[dim], yerr=array_errors[dim], label=f'Numpy Arrays - Dim {dim}', fmt='o')

    coeffs = np.polyfit(sizes, array_times[dim], deg=3)
    poly_appr = np.poly1d(coeffs)
    plt.plot(range(50,151,1), poly_appr(range(50,151,1 )), linestyle='--', label=f'Fit - Numpy Dim {dim}')

plt.title('Numpy Arrays')
plt.xlabel('Size')
plt.ylabel('Time (seconds)')
plt.yscale('log')
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig('vector_calculation_speed.png')

import numpy as np
import matplotlib.pyplot as plt
import time


def measure_time(operation, size, dimensions, iterations=100):
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

sizes = range(50,150,10 )
dimensions = [1, 2, 3]

list_times = {dim: [] for dim in dimensions}
list_errors = {dim: [] for dim in dimensions}
array_times = {dim: [] for dim in dimensions}
array_errors = {dim: [] for dim in dimensions}

for dim in dimensions:
    for size in sizes:
        mean_time, std_time = measure_time(lambda a, b: [a[i]*b[i] for i in range(len(a))], size, dim)
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

    coeffs = np.polyfit(sizes, list_times[dim], deg=2)
    poly_appr = np.poly1d(coeffs)
    plt.plot(sizes, poly_appr(sizes), linestyle='--', label=f'Fit - Lists Dim {dim}')

plt.title('Lists')
plt.xlabel('Size')
plt.ylabel('Time (seconds)')
plt.yscale('log')
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
for dim in dimensions:
    plt.errorbar(sizes, array_times[dim], yerr=array_errors[dim], label=f'Numpy Arrays - Dim {dim}', fmt='o')

    coeffs = np.polyfit(sizes, array_times[dim], deg=2)
    poly_appr = np.poly1d(coeffs)
    plt.plot(sizes, poly_appr(sizes), linestyle='--', label=f'Fit - Numpy Dim {dim}')

plt.title('Numpy Arrays')
plt.xlabel('Size')
plt.ylabel('Time (seconds)')
plt.yscale('log')
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig('vector_calculation_speed.png')

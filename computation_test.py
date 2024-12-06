import numpy as np
import matplotlib.pyplot as plt
import time

def time_list_multiply(shape, trials=5):
    times = []
    for _ in range(trials):
        list_a = list(np.random.rand(*shape))
        list_b = list(np.random.rand(*shape))
        start_time = time.time()
        result = [a * b for a, b in zip(list_a, list_b)]
        end_time = time.time()
        times.append(end_time - start_time)
    return np.mean(times), np.std(times)

def time_numpy_multiply(shape, trials=5):
    times = []
    for _ in range(trials):
        arr_a = np.random.rand(*shape)
        arr_b = np.random.rand(*shape)
        start_time = time.time()
        result = arr_a * arr_b
        end_time = time.time()
        times.append(end_time - start_time)
    return np.mean(times), np.std(times)

sizes = [10, 100, 1000, 5000]
shapes = [
    (size,) for size in sizes  # одномерные
] + [
    (size, size) for size in sizes  # двумерные
] + [
    (size, size, size) for size in sizes  # трехмерные
]

list_times_mean = []
list_times_std = []
for shape in shapes:
    mean, std = time_list_multiply(shape)
    list_times_mean.append(mean)
    list_times_std.append(std)

numpy_times_mean = []
numpy_times_std = []
for shape in shapes:
    mean, std = time_numpy_multiply(shape)
    numpy_times_mean.append(mean)
    numpy_times_std.append(std)


from numpy.polynomial.polynomial import Polynomial

def fit_polynomial(x, y, degree=3):
    p = Polynomial.fit(x, y, degree)
    return p

x = np.array(sizes * 3)  # Точки для оси x (размеры)
y_list = np.array(list_times_mean)  # Время для списков
y_numpy = np.array(numpy_times_mean)  # Время для numpy массивов

p_list = fit_polynomial(x, y_list)
p_numpy = fit_polynomial(x, y_numpy)

# Построение графиков
plt.figure(figsize=(10, 12))

# График 1: Время для списков
plt.subplot(2, 1, 1)
plt.errorbar(sizes * 3, list_times_mean, yerr=list_times_std, fmt='o', label='Списки')
plt.plot(sizes * 3, p_list(x), label='Аппроксимация (списки)', linestyle='--')
plt.xlabel('Размер (в числе элементов)')
plt.ylabel('Время (сек)')
plt.legend()
plt.title('Время перемножения двух списков')

# График 2: Время для numpy массивов
plt.subplot(2, 1, 2)
plt.errorbar(sizes * 3, numpy_times_mean, yerr=numpy_times_std, fmt='o', label='Numpy массивы')
plt.plot(sizes * 3, p_numpy(x), label='Аппроксимация (numpy)', linestyle='--')
plt.xlabel('Размер (в числе элементов)')
plt.ylabel('Время (сек)')
plt.legend()
plt.title('Время перемножения двух numpy массивов')

plt.tight_layout()
plt.savefig('vector_calculation_speed.png')
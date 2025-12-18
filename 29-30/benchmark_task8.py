import random
import timeit

# -------------------------------
# НЕЭФФЕКТИВНАЯ ВЕРСИЯ (list)
# -------------------------------

def reverse_num(x):
    return int(str(abs(x))[::-1]) * (-1 if x < 0 else 1)

def count_common_slow(a, b):
    return sum(
        map(lambda x: (x in b) or (reverse_num(x) in b), a)
    )

# -------------------------------
# ОПТИМИЗИРОВАННАЯ ВЕРСИЯ (set)
# -------------------------------

def count_common_fast(a, b):
    sb = set(b)
    return sum(
        map(lambda x: (x in sb) or (reverse_num(x) in sb), a)
    )

# -------------------------------
# ТЕСТОВЫЕ ДАННЫЕ
# -------------------------------

N = 10_000

a = [random.randint(-99_999, 99_999) for _ in range(N)]
b = [random.randint(-99_999, 99_999) for _ in range(N)]

# -------------------------------
# БЕНЧМАРК
# -------------------------------

slow_time = timeit.timeit(
    lambda: count_common_slow(a, b),
    number=10
)

fast_time = timeit.timeit(
    lambda: count_common_fast(a, b),
    number=10
)

print("Размер массивов:", N)
print("Медленная версия (list):", slow_time)
print("Быстрая версия (set):  ", fast_time)
print("Ускорение:", round(slow_time / fast_time, 2), "раз")

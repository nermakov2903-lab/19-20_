"""
Задание 8 — подсчёт общих чисел с учётом реверса.

Модуль реализует конечный автомат с использованием корутин.
Алгоритм учитывает совпадение числа либо его
реверсивного представления.

Состояния автомата:
- NO_DATA
- HAS_DATA
- HAS_RESULT
"""

import random
from messages import MESSAGES
from logger import logger

msgs = MESSAGES["task8"]

def count_common_with_reverse(a, b):
    """
    Подсчитать количество общих чисел с учётом реверса.

    Parameters
    ----------
    a : list[int]
        Первый массив чисел.
    b : list[int]
        Второй массив чисел.

    Returns
    -------
    int
        Количество совпадающих чисел.
    """
    s = set(b)
    count = 0
    for x in a:
        rev = int(str(abs(x))[::-1])
        if x < 0:
            rev = -rev
        if x in s or rev in s:
            count += 1
    return count

def task8_fsm():
    """
    Корутина конечного автомата задачи 8.

    Управляет вводом массивов, запуском алгоритма
    подсчёта и выводом результата.

    Yields
    ------
    None
        Ожидание пользовательского ввода.

    Returns
    -------
    None
        Возвращает управление в главный автомат.
    """
    a = b = result = None
    state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        for opt in msgs["menu"]:
            print(opt)

        choice = yield
        logger.info(f"task8 choice={choice}, state={state}")

        if choice == "5":
            return

        if state == "NO_DATA":
            if choice == "1":
                a = list(map(int, input("A: ").split()))
                b = list(map(int, input("B: ").split()))
                state = "HAS_DATA"
            elif choice == "2":
                a = [random.randint(-99, 99) for _ in range(5)]
                b = [random.randint(-99, 99) for _ in range(5)]
                state = "HAS_DATA"
            else:
                print(msgs["no_data"])

        elif state in ("HAS_DATA", "HAS_RESULT"):
            if choice == "3":
                result = count_common_with_reverse(a, b)
                print(msgs["algorithm_done"])
                state = "HAS_RESULT"
            elif choice == "4":
                print("Результат:", result if result else msgs["no_result"])

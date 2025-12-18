"""
Задание 4 — операции над большими числами.

Числа представлены в виде массивов цифр.
Модуль реализует конечный автомат задачи
с использованием корутин.

Логические состояния автомата:
- NO_DATA
- HAS_DATA
- HAS_RESULT

Notes
-----
- Каждое состояние автомата описывается явно.
- Переходы выполняются через управляющие конструкции.
- Корутина сохраняет состояние между вызовами `send()`.
"""
import random
from messages import MESSAGES
from logger import logger
from exceptions import DataNotSetError

msgs = MESSAGES["task4"]

def big_number_operation(a, b, op):
    """
    Выполнить операцию над большими числами.

    Parameters
    ----------
    a : list[int]
        Первое число в виде массива цифр.
    b : list[int]
        Второе число в виде массива цифр.
    op : {'add', 'sub'}
        Тип операции.

    Returns
    -------
    list[int]
        Результат операции в виде массива цифр.
    """
    x = int("".join(map(str, a)))
    y = int("".join(map(str, b)))
    return list(map(int, str(x + y if op == "add" else x - y)))

def task4_fsm():
    """
    Корутина конечного автомата задачи 4.

    Обеспечивает ввод массивов цифр, выполнение
    арифметической операции и вывод результата.

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
        logger.info(f"task4 choice={choice}, state={state}")

        if choice == "5":
            return

        if state == "NO_DATA":
            if choice == "1":
                a = list(map(int, input("A: ").split()))
                b = list(map(int, input("B: ").split()))
                state = "HAS_DATA"
            elif choice == "2":
                a = [random.randint(0, 9) for _ in range(5)]
                b = [random.randint(0, 9) for _ in range(5)]
                state = "HAS_DATA"
            else:
                print(msgs["no_data"])

        elif state in ("HAS_DATA", "HAS_RESULT"):
            if choice == "3":
                op = input("add/sub: ")
                result = big_number_operation(a, b, op)
                print(msgs["operation_done"])
                state = "HAS_RESULT"
                logger.info(f"operation: {op}")
            elif choice == "4":
                print("Результат:", result if result else msgs["no_result"])
                logger.info(f"result shown")
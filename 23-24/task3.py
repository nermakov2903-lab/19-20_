"""
Задание 3 — поворот матрицы на 90 градусов.

Модуль реализует конечный автомат задачи 3
с использованием корутин (generator-based FSM).

Автомат имеет логические состояния:
- NO_DATA   — матрица не задана
- HAS_DATA  — матрица задана
- HAS_RESULT — выполнен поворот матрицы

Состояние автомата хранится внутри корутины,
а переходы между состояниями описываются
управляющими конструкциями языка Python.

Notes
-----
- Автомат реализован без таблиц переходов.
- Переходы осуществляются через `yield` / `send`.
- Возврат в главное меню осуществляется оператором `return`.
"""

import random
from messages import MESSAGES
from logger import logger
from exceptions import DataNotSetError, InvalidValueError

msgs = MESSAGES["task3"]

def rotate_matrix_algo(matrix, direction="clockwise"):
    """
    Выполнить поворот матрицы на 90 градусов.

    Parameters
    ----------
    matrix : list[list[int]]
        Исходная матрица.
    direction : {'clockwise', 'counterclockwise'}, optional
        Направление поворота.

    Returns
    -------
    list[list[int]]
        Повернутая матрица.

    Raises
    ------
    DataNotSetError
        Если матрица не задана.
    InvalidValueError
        Если направление поворота некорректно.
    """
    if matrix is None:
        raise DataNotSetError
    if direction == "clockwise":
        return [list(row)[::-1] for row in zip(*matrix)]
    elif direction == "counterclockwise":
        return list(zip(*matrix))[::-1]
    else:
        raise InvalidValueError

def generate_random_matrix(n, m):
    return [[random.randint(0, 9) for _ in range(m)] for _ in range(n)]

def task3_fsm():
    """
    Корутина конечного автомата задачи 3.

    Управляет вводом матрицы, её генерацией,
    выполнением поворота и выводом результата.

    Yields
    ------
    None
        Ожидание пользовательского ввода (пункта меню).

    Returns
    -------
    None
        Возвращает управление в главный автомат.
    """
    matrix = None
    result = None
    state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        for opt in msgs["menu"]:
            print(opt)

        #yield соответствует приёму входного символа автомата.
        #Корутины позволяют естественным образом описывать автоматы без внешних таблиц переходов.
        #Состояние хранится локально, переходы описываются явно
        choice = yield
        logger.info(f"task3 choice={choice}, state={state}")

        if choice == "5":
            return

        if state == "NO_DATA":
            if choice == "1":
                try:
                    n = int(input("N: "))
                    m = int(input("M: "))
                    matrix = [list(map(int, input().split())) for _ in range(n)]
                    state = "HAS_DATA"
                except:
                    print(msgs["input_error"])
            elif choice == "2":
                n = int(input("N: "))
                m = int(input("M: "))
                matrix = generate_random_matrix(n, m)
                state = "HAS_DATA"
            else:
                print(msgs["no_matrix"])

        elif state in ("HAS_DATA", "HAS_RESULT"):
            if choice == "3":
                try:
                    direction = input("Направление: ")
                    result = rotate_matrix_algo(matrix, direction)
                    print(msgs["rotation_done"])
                    state = "HAS_RESULT"
                    logger.info(f"rotation: {direction}")
                except:
                    print(msgs["input_error"])
                    logger.info(f"rotation shown")
            elif choice == "4":
                if result is None:
                    print(msgs["no_result"])
                else:
                    for row in result:
                        print(row)

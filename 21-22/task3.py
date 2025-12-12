"""
Task 3 — поворот матрицы (модуль/подменю) в стиле конечного автомата.

Модуль реализует локальный конечный автомат для задачи 3 с тремя состояниями:
'NO_DATA', 'HAS_DATA', 'HAS_RESULT'. Меню позволяет:
- ввести матрицу вручную,
- сгенерировать случайную матрицу,
- выполнить поворот (clockwise / counterclockwise),
- показать результат,
- вернуться в главное меню,
- отключить логирование.

Публичные API
--------------
task3_menu()
    Запускает локальный цикл меню (FSM). Возвращает управление в caller при выборе "Назад".

Реализованные вспомогательные функции
------------------------------------
rotate_matrix_algo(matrix, direction='clockwise')
    Повернуть матрицу на 90 градусов в указанном направлении.

generate_random_matrix(n, m, low=0, high=9)
    Сгенерировать случайную матрицу n x m.

Пример
------
>>> from task3 import task3_menu
>>> task3_menu()
(интерактивное меню)
"""

import random
from logger import logger
from messages import MESSAGES
from exceptions import DataNotSetError, InvalidValueError

msgs = MESSAGES["task3"]

# Алгоритмы / вспомогательные-
def rotate_matrix_algo(matrix, direction="clockwise"):
    """Поворачивает матрицу на 90 градусов по/против часовой стрелки."""
    if matrix is None:
        raise DataNotSetError("Матрица не задана")
    if direction not in ("clockwise", "counterclockwise"):
        raise InvalidValueError("Направление должно быть 'clockwise' или 'counterclockwise'")
    if direction == "clockwise":
        return [list(row)[::-1] for row in zip(*matrix)]
    else:
        rotated = [list(row) for row in zip(*matrix)]
        return rotated[::-1]

def generate_random_matrix(n, m, low=0, high=9):
    """Создаёт случайную матрицу n x m."""
    if n <= 0 or m <= 0:
        raise InvalidValueError("Размеры должны быть положительными")
    return [[random.randint(low, high) for _ in range(m)] for _ in range(n)]

def _print_matrix(matrix, title="Матрица"):
    print(f"\n{title}:")
    for row in matrix:
        print(row)

# -----------------------------
# Action handlers (работают с контейнером состояния)
def _input_matrix(state_container):
    """Ввод матрицы вручную. Сохраняет в state_container['data'] и сбрасывает result."""
    try:
        n = int(input("N: ").strip())
        m = int(input("M: ").strip())
        matrix = []
        for i in range(n):
            # Ожидаем строку из m чисел
            row = list(map(int, input(f"Введите {m} чисел для строки {i}: ").split()))
            if len(row) != m:
                raise ValueError("Неверное количество элементов в строке")
            matrix.append(row)
        state_container["data"] = matrix
        state_container["result"] = None
        _print_matrix(matrix, "Введенная матрица")
        logger.info("task3: matrix input")
    except Exception as e:
        logger.info(f"task3 input error: {e}")
        print(msgs["input_error"])

def _generate_matrix(state_container):
    """Генерация случайной матрицы и сохранение в container."""
    try:
        n = int(input("N: ").strip())
        m = int(input("M: ").strip())
        if n <= 0 or m <= 0:
            raise ValueError("Размеры должны быть положительными")
        matrix = generate_random_matrix(n, m)
        state_container["data"] = matrix
        state_container["result"] = None
        _print_matrix(matrix, "Сгенерированная матрица")
        logger.info(f"task3: generated matrix {n}x{m}")
    except Exception as e:
        logger.info(f"task3 generate error: {e}")
        print(msgs["input_error"])

def _perform_rotate(state_container):
    """Выполняет поворот текущей матрицы. Требует data в контейнере."""
    try:
        data = state_container.get("data")
        if data is None:
            raise DataNotSetError(msgs["no_matrix"])
        direction = input("Направление (clockwise/counterclockwise): ").strip().lower()
        if direction not in ("clockwise", "counterclockwise"):
            raise InvalidValueError("Направление должно быть 'clockwise' или 'counterclockwise'")
        result = rotate_matrix_algo(data, direction)
        state_container["result"] = result
        _print_matrix(result, "Повернутая матрица")
        print(msgs["rotation_done"])
        logger.info(f"task3: rotated matrix ({direction})")
    except Exception as e:
        logger.info(f"task3 rotate error: {e}")
        print(msgs["input_error"])

def _show_result(state_container):
    """Показывает результат последней операции (если есть)."""
    result = state_container.get("result")
    if result is None:
        print("Нет результата!")
        logger.info("task3: show_result called but result is None")
    else:
        _print_matrix(result, "Результат")
        logger.info("task3: result shown")

def _back(state_container):
    logger.info("task3: back requested (return to main)")

#словарь действий (имена → функции)
#handler - Это функция, которая выполняет одно конкретное действие, соответствующее пункту меню(внутри словаря)
ACTION_MAP = {
    "input_matrix": _input_matrix,
    "generate_matrix": _generate_matrix,
    "perform_rotate": _perform_rotate,
    "show_result": _show_result,
    "disable_logging": _disable_logging,
    "back": _back
}

# -----------------------------
# TRANSITIONS: state -> { choice -> { action / error / next } }
#словарь состояний
#action - метки, по которому FSM выбирает нужный handler(внутри словаря)
TRANSITIONS = {
    "NO_DATA": {
        "1": {"action": "input_matrix", "next": "HAS_DATA"},
        "2": {"action": "generate_matrix", "next": "HAS_DATA"},
        "3": {"error": "no_data"},
        "4": {"error": "algorithm_not_executed"},
        "5": {"action": "back", "next": "BACK"},
        "6": {"action": "disable_logging", "next": "NO_DATA"}
    },
    "HAS_DATA": {
        "1": {"action": "input_matrix", "next": "HAS_DATA"},
        "2": {"action": "generate_matrix", "next": "HAS_DATA"},
        "3": {"action": "perform_rotate", "next": "HAS_RESULT"},
        "4": {"error": "algorithm_not_executed"},
        "5": {"action": "back", "next": "BACK"},
        "6": {"action": "disable_logging", "next": "HAS_DATA"}
    },
    "HAS_RESULT": {
        "1": {"action": "input_matrix", "next": "HAS_DATA"},
        "2": {"action": "generate_matrix", "next": "HAS_DATA"},
        "3": {"action": "perform_rotate", "next": "HAS_RESULT"},
        "4": {"action": "show_result", "next": "HAS_RESULT"},
        "5": {"action": "back", "next": "BACK"},
        "6": {"action": "disable_logging", "next": "HAS_RESULT"}
    }
}

# -----------------------------
# Меню-цикл
# -----------------------------
def task3_menu():
   """
    Запустить меню задачи 3 (локальный FSM).

    Поведение
    ---------
    Цикл отображает пункты меню (MESSAGES['task3']['menu']), читает выбор и по таблице
    TRANSITIONS вызывает соответствующий action из ACTION_MAP. При выборе "5" (Back)
    функция возвращает управление в вызывающий код (обычно main).

    Returns
    -------
    None

    Raises
    ------
    DataNotSetError
        Если попытаться выполнить поворот без данных.
    """
    state_container = {"data": None, "result": None}
    state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        for opt in msgs["menu"]:
            print(opt)

        choice = input(msgs["prompt"]).strip()
        logger.info(f"task3 choice: {choice} (state={state})")

        entry = TRANSITIONS[state].get(choice)
        if not entry:
            print(msgs["invalid_choice"])
            logger.info("task3 invalid choice")
            continue

        # Ошибочная попытка (например, поворот без данных)
        if "error" in entry:
            key = entry["error"]
            if key == "no_data":
                print(msgs["no_matrix"])
                logger.warning("task3: attempted action with no data")
            elif key == "algorithm_not_executed":
                print(msgs.get("no_result", "Сначала выполните операцию"))
                logger.warning("task3: attempted show without result")
            continue

        action_name = entry.get("action")
        next_state = entry.get("next", state)

        # Выполнение действия
        action = ACTION_MAP.get(action_name)
        if action:
            action(state_container)

        # Обработка перехода 'BACK' -> вернуть управление в main
        if next_state == "BACK":
            logger.info("task3: returning to main")
            return

        # Иначе установить новое состояние
        state = next_state

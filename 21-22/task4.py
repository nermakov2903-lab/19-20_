"""
Task 4 — операции над большими числами, представленных массивом цифр.

Модуль реализует локальный автомат с состояниями 'NO_DATA', 'HAS_DATA', 'HAS_RESULT'.
Пункты меню:
- ввод массивов вручную,
- генерация массивов случайно,
- выполнение операции ('add' или 'sub'),
- показ результата,
- назад,
- отключить логирование.

Публичные API
--------------
task4_menu()
    Запускает интерактивное меню задачи 4.

Вспомогательные функции
-----------------------
array_to_int(arr)
    Преобразует массив цифр в целое число.

int_to_array(num)
    Преобразует целое число в массив цифр.

big_number_operation(a, b, op)
    Выполняет сложение или вычитание массивов-чисел.

Примеры
-------
>>> from task4 import task4_menu
>>> task4_menu()
(интерактивно)
"""
import random
from logger import logger
from messages import MESSAGES
from exceptions import DataNotSetError, InvalidValueError

msgs = MESSAGES["task4"]

def array_to_int(arr):
    if not all(isinstance(x, int) for x in arr):
        raise InvalidValueError("Массив должен содержать только цифры")
    return int("".join(map(str, arr)))

def int_to_array(num):
    return list(map(int, str(num)))

def big_number_operation(a, b, op):
    if op not in ("add", "sub"):
        raise InvalidValueError("op must be 'add' or 'sub'")
    num1 = array_to_int(a)
    num2 = array_to_int(b)
    if op == "add":
        return int_to_array(num1 + num2)
    else:
        return int_to_array(num1 - num2)

def generate_digits(n):
    return [random.randint(0, 9) for _ in range(n)]

# --- action handlers ---
def _input_arrays(state_container):
    try:
        a = list(map(int, input("Массив 1: ").split()))
        b = list(map(int, input("Массив 2: ").split()))
        state_container["a"], state_container["b"], state_container["result"] = a, b, None
        logger.info("task4: arrays input")
    except Exception as e:
        logger.info(f"task4 input error: {e}")
        print(msgs["input_error"])

def _generate_arrays(state_container):
    try:
        len1 = int(input("Длина массива 1: "))
        len2 = int(input("Длина массива 2: "))
        a = generate_digits(len1)
        b = generate_digits(len2)
        state_container["a"], state_container["b"], state_container["result"] = a, b, None
        print("A:", a); print("B:", b)
        logger.info("task4: arrays generated")
    except Exception as e:
        logger.info(f"task4 generate error: {e}")
        print(msgs["input_error"])

def _perform_operation(state_container):
    try:
        a = state_container.get("a"); b = state_container.get("b")
        if a is None or b is None:
            raise DataNotSetError(msgs["no_data"])
        op = input("Операция (add/sub): ").strip()
        res = big_number_operation(a, b, op)
        state_container["result"] = res
        print(msgs["operation_done"])
        logger.info("task4: operation performed")
    except Exception as e:
        logger.info(f"task4 operation error: {e}")
        print("Ошибка:", e)

def _show_result(state_container):
    res = state_container.get("result")
    if res is None:
        print("Нет результата!")
    else:
        print("Результат:", res)
        logger.info("task4: result shown")

def _back(state_container):
    logger.info("task4: back requested")

ACTION_MAP = {
    "input_arrays": _input_arrays,
    "generate_arrays": _generate_arrays,
    "perform_operation": _perform_operation,
    "show_result": _show_result,
    "back": _back
}

# --- transitions per state ---
TRANSITIONS = {
    "NO_DATA": {
        "1": {"action": "input_arrays", "next": "HAS_DATA"},
        "2": {"action": "generate_arrays", "next": "HAS_DATA"},
        "3": {"error": "no_data"},
        "4": {"error": "algorithm_not_executed"},
        "5": {"action": "back", "next": "BACK"},
    },
    "HAS_DATA": {
        "1": {"action": "input_arrays", "next": "HAS_DATA"},
        "2": {"action": "generate_arrays", "next": "HAS_DATA"},
        "3": {"action": "perform_operation", "next": "HAS_RESULT"},
        "4": {"error": "algorithm_not_executed"},
        "5": {"action": "back", "next": "BACK"},
    },
    "HAS_RESULT": {
        "1": {"action": "input_arrays", "next": "HAS_DATA"},
        "2": {"action": "generate_arrays", "next": "HAS_DATA"},
        "3": {"action": "perform_operation", "next": "HAS_RESULT"},
        "4": {"action": "show_result", "next": "HAS_RESULT"},
        "5": {"action": "back", "next": "BACK"},
    }
}

def task4_menu():
    """
    Запустить меню задачи 4 (локальный FSM).

    Notes
    -----
    Контейнер состояния хранит keys: 'a', 'b', 'result'.

    Returns
    -------
    None
    """
    # local container holds a, b, result
    state_container = {"a": None, "b": None, "result": None}
    state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        for opt in msgs["menu"]:
            print(opt)

        choice = input(msgs["prompt"]).strip()
        logger.info(f"task4 choice: {choice} (state={state})")

        entry = TRANSITIONS[state].get(choice)
        if not entry:
            print(msgs["invalid_choice"])
            logger.info("task4 invalid choice")
            continue

        if "error" in entry:
            key = entry["error"]
            if key == "no_data":
                print(msgs["no_data"])
                logger.warning("task4 attempted action with no data")
            elif key == "algorithm_not_executed":
                print(msgs["no_data"])
                logger.warning("task4 attempted show without result")
            continue

        action_name = entry.get("action")
        next_state = entry.get("next", state)
        # run action
        action = ACTION_MAP.get(action_name)
        if action:
            action(state_container)

        if next_state == "BACK":
            logger.info("task4: returning to main")
            return
        state = next_state

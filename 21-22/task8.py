# task8.py
"""
Task8 as FSM: NO_DATA / HAS_DATA / HAS_RESULT
"""
import random
from logger import logger
from messages import MESSAGES
from exceptions import DataNotSetError, InvalidValueError

msgs = MESSAGES["task8"]

def count_common_with_reverse(array1, array2):
    if array1 is None or array2 is None:
        raise DataNotSetError("Массивы не заданы")
    set2 = set(array2)
    count = 0
    for number in array1:
        if not isinstance(number, int):
            raise InvalidValueError("Массив должен содержать только целые числа")
        if number < 0:
            reversed_number = -int(str(-number)[::-1])
        else:
            reversed_number = int(str(number)[::-1])
        if number in set2 or reversed_number in set2:
            count += 1
    return count

def generate_random_array(size, min_val=-999, max_val=999):
    return [random.randint(min_val, max_val) for _ in range(size)]

# actions
def _input_arrays(state_container):
    try:
        state_container["a"] = list(map(int, input("Массив 1: ").split()))
        state_container["b"] = list(map(int, input("Массив 2: ").split()))
        state_container["result"] = None
        logger.info("task8: arrays input")
    except Exception as e:
        logger.info(f"task8 input error: {e}")
        print(msgs["input_error"])

def _generate_arrays(state_container):
    try:
        size1 = int(input("Размер массива 1: "))
        size2 = int(input("Размер массива 2: "))
        state_container["a"] = generate_random_array(size1)
        state_container["b"] = generate_random_array(size2)
        state_container["result"] = None
        print("Массив 1:", state_container["a"])
        print("Массив 2:", state_container["b"])
        logger.info("task8: arrays generated")
    except Exception as e:
        logger.info(f"task8 generate error: {e}")
        print(msgs["input_error"])

def _perform_algorithm(state_container):
    try:
        a = state_container.get("a"); b = state_container.get("b")
        if a is None or b is None:
            raise DataNotSetError(msgs["no_data"])
        res = count_common_with_reverse(a, b)
        state_container["result"] = res
        print(msgs["algorithm_done"])
        logger.info("task8: algorithm executed")
    except Exception as e:
        logger.info(f"task8 algorithm error: {e}")
        print("Ошибка:", e)

def _show_result(state_container):
    res = state_container.get("result")
    if res is None:
        print("Нет результата!")
    else:
        print("Количество общих чисел:", res)
        logger.info("task8: result shown")

def _disable_logging(state_container):
    logger.setLevel("CRITICAL")
    print("Логирование отключено")
    logger.critical("task8 logging disabled")

def _back(state_container):
    logger.info("task8: back requested")

ACTION_MAP = {
    "input_arrays": _input_arrays,
    "generate_arrays": _generate_arrays,
    "perform_algorithm": _perform_algorithm,
    "show_result": _show_result,
    "back": _back
}

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
        "3": {"action": "perform_algorithm", "next": "HAS_RESULT"},
        "4": {"error": "algorithm_not_executed"},
        "5": {"action": "back", "next": "BACK"},
    },
    "HAS_RESULT": {
        "1": {"action": "input_arrays", "next": "HAS_DATA"},
        "2": {"action": "generate_arrays", "next": "HAS_DATA"},
        "3": {"action": "perform_algorithm", "next": "HAS_RESULT"},
        "4": {"action": "show_result", "next": "HAS_RESULT"},
        "5": {"action": "back", "next": "BACK"},
    }
}

def task8_menu():
    state_container = {"a": None, "b": None, "result": None}
    state = "NO_DATA"
    while True:
        print("\n" + msgs["title"])
        for opt in msgs["menu"]:
            print(opt)

        choice = input(msgs["prompt"]).strip()
        logger.info(f"task8 choice: {choice} (state={state})")

        entry = TRANSITIONS[state].get(choice)
        if not entry:
            print(msgs["invalid_choice"])
            logger.info("task8 invalid choice")
            continue

        if "error" in entry:
            key = entry["error"]
            if key == "no_data":
                print(msgs["no_data"]); logger.warning("task8: no data")
            elif key == "algorithm_not_executed":
                print(msgs["no_data"]); logger.warning("task8: algorithm not executed")
            continue

        action_name = entry.get("action")
        next_state = entry.get("next", state)
        action = ACTION_MAP.get(action_name)
        if action:
            action(state_container)

        if next_state == "BACK":
            logger.info("task8: returning to main")
            return
        state = next_state

import random
from messages import MESSAGES
from logger import logger

msgs = MESSAGES["task8"]

# =====================================================
# АЛГОРИТМЫ
# =====================================================

reverse_num = lambda x: int(str(abs(x))[::-1]) * (-1 if x < 0 else 1)

count_common_with_reverse = lambda a, b: (
    lambda sb: sum(
        1 for x in a if x in sb or reverse_num(x) in sb
    )
)(set(b))
#
# • set(b) вместо list → поиск O(1)
# • генератор вместо списка → меньше памяти
# • было O(n²), стало O(n)

# =====================================================
# FSM 
# =====================================================

def task8_fsm():
    a = b = result = None
    state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        list(map(print, msgs["menu"]))

        choice = yield
        logger.info(f"task8 choice={choice}, state={state}")

        if choice == "5":
            return

        if state == "NO_DATA":
            actions = {
                "1": lambda: (
                    list(map(int, input("A: ").split())),
                    list(map(int, input("B: ").split()))
                ),
                "2": lambda: (
                    [random.randint(-99, 99) for _ in range(5)],
                    [random.randint(-99, 99) for _ in range(5)]
                )
            }

            try:
                a, b = actions.get(choice, lambda: (_ for _ in ()).throw(ValueError()))()
                state = "HAS_DATA"
            except:
                print(msgs["input_error"])

        else:
            actions = {
                "3": lambda: (
                    print(msgs["algorithm_done"]),
                    count_common_with_reverse(a, b)
                )[1],
                "4": lambda: print(
                    "Результат:",
                    result if result is not None else msgs["no_result"]
                )
            }

            result = actions.get(choice, lambda: print(msgs["invalid_choice"]))()
            state = "HAS_RESULT" if result is not None else state

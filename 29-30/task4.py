import random
from functools import reduce
from messages import MESSAGES
from logger import logger
from exceptions import InvalidValueError

msgs = MESSAGES["task4"]

# =====================================================
# АЛГОРИТМЫ
# =====================================================

to_int = lambda digits: reduce(
    lambda acc, d: acc * 10 + d,
    digits,
    0
)
#
# reduce вместо int("".join(map(str, digits)))
# → нет строк и временных объектов

big_number_operation = lambda a, b, op: list(
    map(
        int,
        str(
            {
                "add": lambda: to_int(a) + to_int(b),
                "sub": lambda: to_int(a) - to_int(b)
            }.get(op, lambda: (_ for _ in ()).throw(InvalidValueError()))()
        )
    )
)

# =====================================================
# FSM
# =====================================================

def task4_fsm():
    a = b = result = None
    state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        list(map(print, msgs["menu"]))

        choice = yield
        logger.info(f"task4 choice={choice}, state={state}")

        if choice == "5":
            return

        if state == "NO_DATA":
            actions = {
                "1": lambda: (
                    list(map(int, input("A: ").split())),
                    list(map(int, input("B: ").split()))
                ),
                "2": lambda: (
                    [random.randint(0, 9) for _ in range(5)],
                    [random.randint(0, 9) for _ in range(5)]
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
                    lambda op: (
                        print(msgs["operation_done"]),
                        big_number_operation(a, b, op)
                    )[1]
                )(input("add/sub: ")),
                "4": lambda: print("Результат:", result if result else msgs["no_result"])
            }

            try:
                result = actions.get(choice, lambda: print(msgs["invalid_choice"]))()
                state = "HAS_RESULT" if result else state
            except:
                print(msgs["input_error"])

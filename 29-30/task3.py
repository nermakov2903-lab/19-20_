import random
from messages import MESSAGES
from logger import logger
from exceptions import DataNotSetError, InvalidValueError

msgs = MESSAGES["task3"]

# =====================================================
# АЛГОРИТМЫ
# =====================================================

rotate_clockwise = lambda m: [
    list(row)[::-1] for row in zip(*m)
]
#list comprehension быстрее, чем ручной for + append

rotate_counter = lambda m: [
    list(row) for row in zip(*m)
][::-1]
#  минимум временных структур, сразу list[list[int]]

rotate_matrix_algo = lambda m, d="clockwise": (
    m is None and (_ for _ in ()).throw(DataNotSetError()) or
    {
        "clockwise": rotate_clockwise,
        "counterclockwise": rotate_counter
    }.get(d, lambda _: (_ for _ in ()).throw(InvalidValueError()))(m)
)
#  аргумент по умолчанию вместо лишних проверок

generate_random_matrix = lambda n, m: [
    [random.randint(0, 9) for _ in range(m)]
    for _ in range(n)
]
#  list comprehension вместо вложенных циклов

read_row = lambda _: list(map(int, input().split()))
# [EFFICIENCY] map быстрее ручного преобразования

# =====================================================
# FSM
# =====================================================

def task3_fsm():
    matrix = None
    result = None
    state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        list(map(print, msgs["menu"]))

        choice = yield
        logger.info(f"task3 choice={choice}, state={state}")

        if choice == "5":
            return

        if state == "NO_DATA":
            actions = {
                "1": lambda: (
                    lambda n, m: [read_row(i) for i in range(n)]
                )(int(input("N: ")), int(input("M: "))),
                "2": lambda: generate_random_matrix(
                    int(input("N: ")), int(input("M: "))
                )
            }

            try:
                matrix = actions.get(choice, lambda: (_ for _ in ()).throw(ValueError()))()
                state = "HAS_DATA"
            except:
                print(msgs["input_error"])

        else:
            actions = {
                "3": lambda: (
                    lambda d: (
                        print(msgs["rotation_done"]),
                        rotate_matrix_algo(matrix, d)
                    )[1]
                )(input("Направление: ")),
                "4": lambda: (
                    list(map(print, result))
                    if result else print(msgs["no_result"])
                )
            }

            try:
                result = actions.get(choice, lambda: print(msgs["invalid_choice"]))()
                state = "HAS_RESULT" if result else state
            except:
                print(msgs["input_error"])

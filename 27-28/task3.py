import random
from messages import MESSAGES
from logger import logger
from exceptions import DataNotSetError, InvalidValueError

msgs = MESSAGES["task3"]

#ФУНКЦИОНАЛЬНЫЕ АЛГОРИТМЫ

#Функции высшего порядка
#map заменяет цикл for
rotate_clockwise = lambda m: list(
    map(lambda r: list(r)[::-1], zip(*m))
)

rotate_counter = lambda m: list(
    map(list, zip(*m))
)[::-1]

rotate_matrix_algo = lambda m, d="clockwise": (
    m is None and (_ for _ in ()).throw(DataNotSetError()) or
    {
        "clockwise": rotate_clockwise,
        "counterclockwise": rotate_counter
    }.get(d, lambda _: (_ for _ in ()).throw(InvalidValueError()))(m)
)

generate_random_matrix = lambda n, m: list(
    map(lambda _: [random.randint(0, 9) for _ in range(m)], range(n))
)

read_row = lambda _: list(map(int, input().split()))

# --- FSM ---

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
                #Функциональный dispatch, без if/elif
                #легко расширять, выбор поведения как данных
                "1": lambda: (
                    lambda n, m: list(map(read_row, range(n)))
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

from logger import logger
from messages import MESSAGES
from task3 import task3_menu
from task4 import task4_menu
from task8 import task8_menu

"""
Главное меню как конечный автомат:
Состояние одно — MAIN.
Переходы определяются словарём.
"""

MAIN_FSM = {
    "MAIN": {
        "1": {"action": "task3"},
        "2": {"action": "task4"},
        "3": {"action": "task8"},
        "4": {"action": "exit"}
    }
}

# обработчики действий
def do_task3():
    logger.info("→ Переход в task3")
    task3_menu()

def do_task4():
    logger.info("→ Переход в task4")
    task4_menu()

def do_task8():
    logger.info("→ Переход в task8")
    task8_menu()

def do_exit():
    print(MESSAGES["main_menu"]["exit"])
    logger.info("Приложение завершено пользователем")
    return False

ACTION_MAP = {
    "task3": do_task3,
    "task4": do_task4,
    "task8": do_task8,
    "exit": do_exit
}


def main():
    state = "MAIN"
    msgs = MESSAGES["main_menu"]

    while True:
        print("\n" + msgs["title"])
        for opt in msgs["options"]:
            print(opt)

        choice = input(msgs["prompt"]).strip()
        logger.info(f"MAIN choice: {choice}")

        entry = MAIN_FSM[state].get(choice)
        if not entry:
            print(msgs["invalid"])
            logger.warning("Main: неверный пункт")
            continue

        action_name = entry["action"]
        handler = ACTION_MAP[action_name]

        should_continue = handler()
        if should_continue is False:  # выход
            break


if __name__ == "__main__":
    main()

from logger import logger
from messages import MESSAGES
from task3 import task3_menu
from task4 import task4_menu
from task8 import task8_menu

"""
Главный модуль приложения (конечный автомат главного меню).

Модуль реализует верхний уровень пользовательского интерфейса:
печатает главное меню, принимает выбор пользователя и вызывает
соответствующие подпроцессы (task3, task4, task8) или завершает приложение.

Архитектура
----------
MAIN_FSM : dict
    Словарь переходов главного автомата. Ключи — состояния (обычно 'MAIN'),
    значения — словари, где ключи — пользовательский ввод ('1','2','3','4'),
    а значения — конфигурация перехода (например, {"action": "task3"}).

ACTION_MAP : dict
    Отображение имён действий (строк) в вызываемые функции (handlers).
    Используется для вызова обработчиков, заданных в MAIN_FSM.

Основные элементы
-----------------
main()
    Главная функция, запускающая цикл интерфейса.

do_task3(), do_task4(), do_task8(), do_exit()
    Обёртки-обработчики для вызова подпроцессов/завершения приложения.

Examples
--------
Запуск приложения из командной строки::

    python main.py

Примечания
---------
- Модуль использует MESSAGES из messages.py для текстов меню и сообщений.
- Подпроцессы task3, task4, task8 должны экспортировать функции taskN_menu().
"""


#карта переходов(логика)
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


#словарь обработчиков, выполнение функций
ACTION_MAP = {
    "task3": do_task3,
    "task4": do_task4,
    "task8": do_task8,
    "exit": do_exit
}


def main():
     """
    Главный цикл программы — обработка ввода главного меню через FSM.

    Алгоритм
    --------
    1. Печать текста главного меню из MESSAGES.
    2. Чтение выбора пользователя.
    3. Поиск записи в MAIN_FSM[state][choice].
    4. Поиск соответствующего обработчика в ACTION_MAP и его вызов.
    5. Если обработчик вернул False — завершение цикла.

    Raises
    ------
    KeyError
        Если конфигурация MAIN_FSM некорректна (отсутствует action в записи).
    """
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

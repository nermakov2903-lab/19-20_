"""
Главный модуль приложения.

Модуль реализует главный конечный автомат приложения
в парадигме автоматного программирования с использованием корутин.

Автомат обрабатывает пользовательский ввод главного меню
и в зависимости от выбранного пункта передаёт управление
во вложенные автоматы (task3, task4, task8) с помощью конструкции
`yield from`.

Notes
-----
- Каждое меню реализовано как корутина (generator).
- Состояние автомата инкапсулировано внутри корутины.
- Пользовательский ввод передаётся в автомат через метод `send()`.

See Also
--------
task3_fsm : Автомат задания 3.
task4_fsm : Автомат задания 4.
task8_fsm : Автомат задания 8.
"""
from messages import MESSAGES
from logger import logger
from task3 import task3_fsm
from task4 import task4_fsm
from task8 import task8_fsm

def main_fsm():
    """
    Корутина главного меню (FSM верхнего уровня).

    Реализует конечный автомат главного меню приложения.
    Ожидает пользовательский ввод через `send()` и
    выполняет переходы между состояниями.

    Yields
    ------
    None
        Ожидание пользовательского ввода.

    Returns
    -------
    None
        Завершает работу приложения при выборе пункта "Выход".
    """
    msgs = MESSAGES["main_menu"]

    while True:
        print("\n" + msgs["title"])
        for opt in msgs["options"]:
            print(opt)

        choice = yield
        logger.info(f"MAIN choice: {choice}")

        #вложенность автоматов реализуется через yield from
        if choice == "1":
            yield from task3_fsm()
        elif choice == "2":
            yield from task4_fsm()
        elif choice == "3":
            yield from task8_fsm()
        elif choice == "4":
            print(msgs["exit"])
            return
        else:
            print(msgs["invalid"])

def main():
    fsm = main_fsm()
    next(fsm)

    while True:
        try:
            #корутина сохраняет своё состояние между вызовами send()
            choice = input("Выберите пункт: ").strip()
            fsm.send(choice)
        except StopIteration:
            break

if __name__ == "__main__":
    main()

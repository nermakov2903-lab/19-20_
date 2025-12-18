# messages.py

class Messages:
    """Централизованные сообщения для всех меню и FSM."""

    class MENU_MAIN:
        title = "=== ГЛАВНОЕ МЕНЮ ==="
        options = [
            "1. Задание 3 (Поворот матрицы)",
            "2. Задание 4 (Операции над большими числами)",
            "3. Задание 8 (Общие числа с реверсом)",
            "4. Выход"
        ]
        prompt = "Выберите пункт: "
        invalid = "Неверный пункт!"
        exit_msg = "Выход из программы..."

    class TASK3:
        title = "=== ЗАДАНИЕ 3 ==="
        menu = [
            "1. Ввести матрицу вручную",
            "2. Сгенерировать случайную матрицу",
            "3. Выполнить поворот",
            "4. Показать результат",
            "5. Назад",
        ]
        prompt = "Выберите пункт: "
        input_error = "Ошибка ввода матрицы!"
        rotation_done = "Поворот выполнен."
        no_matrix = "Сначала введите матрицу!"
        no_result = "Нет результата!"
        invalid_choice = "Неверный пункт!"

    class TASK4:
        title = "=== ЗАДАНИЕ 4 ==="
        menu = [
            "1. Ввести массивы вручную",
            "2. Сгенерировать массивы случайно",
            "3. Выполнить операцию",
            "4. Показать результат",
            "5. Назад",
        ]
        prompt = "Выберите пункт: "
        input_error = "Ошибка ввода массивов!"
        operation_done = "Операция выполнена"
        no_data = "Сначала введите массивы!"
        no_result = "Нет результата!"
        invalid_choice = "Неверный пункт!"

    class TASK8:
        title = "=== ЗАДАНИЕ 8 ==="
        menu = [
            "1. Ввести массивы вручную",
            "2. Сгенерировать массивы случайно",
            "3. Выполнить алгоритм",
            "4. Показать результат",
            "5. Назад",
        ]
        prompt = "Выберите пункт: "
        input_error = "Ошибка ввода массивов!"
        algorithm_done = "Алгоритм выполнен"
        no_data = "Сначала введите массивы!"
        no_result = "Нет результата!"
        invalid_choice = "Неверный пункт!"

# совместимость со старым стилем
MESSAGES = {
    "main_menu": {
        "title": Messages.MENU_MAIN.title,
        "options": Messages.MENU_MAIN.options,
        "prompt": Messages.MENU_MAIN.prompt,
        "invalid": Messages.MENU_MAIN.invalid,
        "exit": Messages.MENU_MAIN.exit_msg
    },

    "task3": {
        "title": Messages.TASK3.title,
        "menu": Messages.TASK3.menu,
        "prompt": Messages.TASK3.prompt,
        "input_error": Messages.TASK3.input_error,
        "rotation_done": Messages.TASK3.rotation_done,
        "no_matrix": Messages.TASK3.no_matrix,
        "no_result": Messages.TASK3.no_result,
        "invalid_choice": Messages.TASK3.invalid_choice
    },

    "task4": {
        "title": Messages.TASK4.title,
        "menu": Messages.TASK4.menu,
        "prompt": Messages.TASK4.prompt,
        "input_error": Messages.TASK4.input_error,
        "operation_done": Messages.TASK4.operation_done,
        "no_data": Messages.TASK4.no_data,
        "no_result": Messages.TASK4.no_result,
        "invalid_choice": Messages.TASK4.invalid_choice
    },

    "task8": {
        "title": Messages.TASK8.title,
        "menu": Messages.TASK8.menu,
        "prompt": Messages.TASK8.prompt,
        "input_error": Messages.TASK8.input_error,
        "algorithm_done": Messages.TASK8.algorithm_done,
        "no_data": Messages.TASK8.no_data,
        "no_result": Messages.TASK8.no_result,
        "invalid_choice": Messages.TASK8.invalid_choice
    }
}

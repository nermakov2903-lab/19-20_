"""
exceptions.py

Содержит классы исключений для приложения.

Все исключения наследуются от базового класса AppError.
Иерархия:
- AppError — базовый класс
    - InputError — ошибки ввода пользователем
    - OperationError — ошибки при выполнении операций
    - DataNotSetError — данные не заданы, но функция требует их наличия
    - InvalidValueError — некорректные значения или параметры функций

Пример использования:
    from exceptions import DataNotSetError

    if data is None:
        raise DataNotSetError("Данные не заданы")
"""

class AppError(Exception):
    """Базовый класс всех исключений приложения"""
    pass

class InputError(AppError):
    """Ошибка ввода пользователем"""
    pass

class OperationError(AppError):
    """Ошибка выполнения операции"""
    pass

class DataNotSetError(AppError):
    """Ошибка, когда данные не заданы"""
    pass

class InvalidValueError(AppError):
    """Ошибка некорректного значения или параметра"""
    pass

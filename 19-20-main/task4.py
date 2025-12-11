# task4.py
from typing import List

def _digits_to_int(digits: List[int]) -> int:
    """
    Преобразует список цифр (msb..lsb) в целое число.


    Parameters
    ----------
    digits : list of int
    Список цифр в порядке от старших к младшим (msb ... lsb). Может содержать
    положительные однозначные целые числа.


    Returns
    -------
    int
    Целое число, соответствующее последовательности цифр. Для пустого списка
    возвращает 0.


    Examples
    --------
    >> _digits_to_int([1, 2, 3])
    123
    """

    if not digits:
        return 0
    # предполагаем, что массив — в порядке от старших к младшим (msb ... lsb)
    s = ''.join(str(abs(int(d))) for d in digits)
    return int(s)

def _int_to_digits(n: int) -> List[int]:
    """
    Преобразует целое число в список цифр (msb..lsb).


    Parameters
    ----------
    n : int
    Число, которое нужно представить в виде списка цифр. Отрицательные числа
    рассматриваются по модулю.


    Returns
    -------
    list of int
    Список цифр (msb..lsb). Для 0 возвращает [0].


    Examples
    --------
    >> _int_to_digits(504)
    [5, 0, 4]
    """
    if n == 0:
        return [0]
    s = str(abs(int(n)))
    return [int(ch) for ch in s]

def add_or_sub_bigints(a: List[int], b: List[int], op: str = 'add') -> List[int]:
    """
    Складывает или вычитает большие числа, представленные списками цифр.


    Parameters
    ----------
    a : list of int
    Первое число, список цифр в порядке msb..lsb.
    b : list of int
    Второе число, список цифр в порядке msb..lsb.
    op : {'add', 'sub'}, optional
    Операция: 'add' — сложение (по умолчанию), 'sub' — вычитание (a - b).


    Returns
    -------
    list of int
    Результат в виде списка цифр (msb..lsb). В случае отрицательного результата
    при `op='sub'` возвращается представление отрицательного числа без знака —
    рекомендуется интерпретировать отдельно при необходимости.


    Notes
    -----
    Текущая реализация использует преобразование в Python `int` для простоты.
    При необходимости можно заменить на поразрядную обработку для очень больших
    чисел, выходящих за пределы памяти.


    Examples
    --------
    >> add_or_sub_bigints([1,2,3], [4,5,6], op='add')
    [5, 7, 9]
    """
    ia = _digits_to_int(a)
    ib = _digits_to_int(b)
    if op == 'add':
        res = ia + ib
    else:
        res = ia - ib
    return _int_to_digits(res)

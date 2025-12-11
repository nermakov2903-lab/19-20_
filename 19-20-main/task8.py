# task8.py
from typing import List, Set

def _rev_number(n: int) -> int:
    """
    Возвращает число, полученное инвертированием десятичной записи числа `n`.


    Parameters
    ----------
    n : int
    Входное число (может быть отрицательным — берётся абсолютное значение).


    Returns
    -------
    int
    Целое число, полученное зеркальным отражением цифр.


    Examples
    --------
    >> _rev_number(120)
    21
    """
    s = str(abs(int(n)))
    return int(s[::-1])

def common_with_reversed(a: List[int], b: List[int]) -> int:
    """
    Подсчитывает количество уникальных чисел из списка `a`, которые считаются
    общими с `b` по следующему правилу: число из `a` считается общим, если
    оно встречается в `b` напрямую, либо его перевёрнутая запись встречается в `b`.


    Parameters
    ----------
    a : list of int
    Список чисел A.
    b : list of int
    Список чисел B.


    Returns
    -------
    int
    Количество уникальных элементов из `a`, удовлетворяющих условию.


    Examples
    --------
    >> common_with_reversed([12, 34, 21], [21, 43])
    2
    """
    set_b = set(int(x) for x in b)
    set_b_rev = set(_rev_number(x) for x in b)
    seen = set()
    count = 0
    for x in a:
        xi = int(x)
        if xi in seen:
            continue
        if xi in set_b or xi in set_b_rev:
            count += 1
            seen.add(xi)
    return count

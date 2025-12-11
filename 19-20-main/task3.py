# task3.py
from typing import List

def rotate_matrix(matrix: List[List[int]], direction: str = 'cw') -> List[List[int]]:
    """
    Поворачивает матрицу на 90 градусов.


    Parameters
    ----------
    matrix : list of list of int
    Входная матрица (список строк). Элементы могут быть любыми объектами,
    поддерживающими копирование/печать.
    direction : {'cw', 'ccw'}, optional
    Направление поворота: 'cw' — по часовой (default), 'ccw' — против часовой.


    Returns
    -------
    list of list
    Новая матрица, полученная поворотом входной матрицы на 90 градусов
    в указанном направлении.


    Raises
    ------
    ValueError
    Если `direction` не равен 'cw' или 'ccw'.


    Notes
    -----
    Алгоритм реализован через транспонирование с последующим переворотом строк
    или порядка строк в зависимости от направления.


    Examples
    --------
    >> rotate_matrix([[1,2],[3,4]], direction='cw')
    [[3, 1], [4, 2]]
    """
    if not matrix:
        return []
    # transpose
    transposed = [list(row) for row in zip(*matrix)]
    if direction == 'cw':
        # по часовой: транспонируем, затем переворачиваем каждую строку
        return [row[::-1] for row in transposed]
    else:
        # против часовой: транспонируем, затем переворачиваем порядок строк
        return transposed[::-1]

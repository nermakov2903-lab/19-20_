# client.py
import threading
import time
import random
from datetime import datetime

def ts():
    return datetime.now().strftime("%H:%M:%S")

class ClientThread(threading.Thread):
    """
    Поток-клиент, который генерирует/отправляет запросы серверу и получает
    результаты через callback.


    Parameters
    ----------
    name : str
    Читабельное имя клиента, используемое в логах.
    request_queue : queue.Queue
    Очередь для отправки запросов на сервер (разделяемая между клиентами).
    actions : list of dict
    Список действий (сценарий) для данного клиента. Каждый элемент — словарь
    со следующими ключами:


    - 'task' : str
    Имя задачи ('rotate', 'bigint', 'common').
    - 'generate' : bool, optional
    Если True — клиент сам сгенерирует данные (матрицы/массивы).
    - 'params' : dict, optional
    Словарь параметров, специфичных для задачи (размеры, направление и т.д.).
    - 'data' : any, optional
    Явно указанные данные для отправки (если не генерировать).


    Methods
    -------
    run()
    Переопределённый метод потока; генерирует/отправляет запросы и завершает работу.
    _callback(client_name, task, result, input_data)
    Метод, вызываемый сервером при завершении обработки запроса; печатает
    входные данные и результат и сохраняет их в `self.results`.
    """
    def __init__(self, name: str, request_queue, actions):
        super().__init__(daemon=True)
        self.name = name
        self.request_queue = request_queue
        self.actions = actions
        self.results = []

    def run(self):
        print(f"{ts()} {self.name}: клиент запущен")
        time.sleep(random.uniform(0.05, 0.25))
        for action in self.actions:
            task = action['task']
            params = action.get('params', {})
            data = action.get('data')

            # генерация данных и ОБЯЗАТЕЛЬНАЯ печать (чтобы не терялось)
            if action.get('generate', False):
                if task == 'rotate':
                    n = params.get('n', 3)
                    m = params.get('m', 3)
                    matrix = [[random.randint(1,9) for _ in range(m)] for _ in range(n)]
                    data = matrix
                    print(f"{ts()} {self.name}: сгенерированы данные")
                    print("\nСгенерированная матрица:")
                    for row in matrix:
                        print(row)
                    print()
                elif task == 'bigint':
                    la = params.get('len_a', 6)
                    lb = params.get('len_b', 4)
                    a = [random.randint(0,9) for _ in range(la)]
                    b = [random.randint(0,9) for _ in range(lb)]
                    # устранение ведущих нулей для наглядности:
                    if a and a[0] == 0:
                        a[0] = random.randint(1,9)
                    if b and b[0] == 0:
                        b[0] = random.randint(1,9)
                    data = {'a': a, 'b': b}
                    print(f"{ts()} {self.name}: сгенерированы большие числа (массивы цифр):")
                    print("A =", a)
                    print("B =", b)
                    print()
                elif task == 'common':
                    la = params.get('len_a', 7)
                    lb = params.get('len_b', 6)
                    a = [random.randint(0,99) for _ in range(la)]
                    b = [random.randint(0,99) for _ in range(lb)]
                    data = {'a': a, 'b': b}
                    print(f"{ts()} {self.name}: сгенерированы массивы для поиска общих чисел")
                    print("A =", a)
                    print("B =", b)
                    print()

            # отправка запроса
            print(f"{ts()} {self.name}: отправлен запрос на {self._task_name(task)}")
            request = {
                'client': self.name,
                'task': task,
                'data': data,
                'params': params,
                'callback': self._callback
            }
            self.request_queue.put(request)

            time.sleep(random.uniform(0.2, 0.9))

        print(f"{ts()} {self.name}: выполнение завершено")

    def _callback(self, client_name, task, result, input_data):
        # Коллбек вызывается сервером — печатаем ясно: вход -> результат
        print(f"{ts()} {self.name}: получен результат для {self._task_name(task)}")
        # показываем входные данные (дублируем — полезно если очередь/параллельность меняют порядок)
        if task == 'rotate':
            print("\n(входная матрица в клиенте):")
            for row in input_data:
                print(row)
            print("\n(результат поворота):")
            for row in result:
                print(row)
            print()
        elif task == 'bigint':
            a = input_data.get('a')
            b = input_data.get('b')
            print("A =", a)
            print("B =", b)
            print("Результат (массив цифр):", result)
            try:
                print("Результат как число:", int(''.join(map(str, result))))
            except Exception:
                pass
            print()
        elif task == 'common':
            a = input_data.get('a')
            b = input_data.get('b')
            print("A =", a)
            print("B =", b)
            print("Общие числа (количество):", result)
            print()
        else:
            print("Результат:", result)
            print()

        self.results.append((task, result))

    def _task_name(self, task_key):
        mapping = {
            'rotate': 'поворот матрицы',
            'bigint': 'операция над большими числами',
            'common': 'поиск общих чисел'
        }
        return mapping.get(task_key, task_key)

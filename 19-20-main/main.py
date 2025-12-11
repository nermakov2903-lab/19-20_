# main.py
import queue
import time
import threading
from server import MatrixServer
from client import ClientThread

def main():
    """
    Точка входа в демонстрацию: создаёт очередь, запускает сервер и клиентов,
    ждёт завершения клиентов, дождётся обработки всех запросов и корректно
    завершает сервер.


    Steps
    -----
    1. Создаёт `queue.Queue()`.
    2. Создаёт и стартует `MatrixServer`.
    3. Формирует сценарии `actions` для каждого клиента.
    4. Создаёт и стартует `ClientThread` для каждого сценария.
    5. Дожидается завершения клиентов (`join()`), затем опустошения очереди.
    6. Останавливает сервер и завершает программу.


    Notes
    -----
    Важно: сначала дождаться, что клиенты отправили все запросы (join на клиентах),
    а затем подождать, пока очередь не опустеет, прежде чем останавливать сервер,
    чтобы не потерять необработанные запросы.
    """
    q = queue.Queue()
    server = MatrixServer(q)
    server.start()

    # действия клиентов — демонстрация всех трёх задач
    actions1 = [
        {'task': 'rotate', 'generate': True, 'params': {'n': 2, 'm': 2, 'direction': 'ccw'}},
        {'task': 'bigint', 'generate': True, 'params': {'len_a': 6, 'len_b': 4, 'op': 'add'}},
    ]
    actions2 = [
        {'task': 'rotate', 'generate': True, 'params': {'n': 3, 'm': 3, 'direction': 'cw'}},
        {'task': 'common', 'generate': True, 'params': {'len_a': 8, 'len_b': 7}},
    ]
    actions3 = [
        {'task': 'rotate', 'generate': True, 'params': {'n': 4, 'm': 2, 'direction': 'cw'}},
        {'task': 'bigint', 'generate': True, 'params': {'len_a': 5, 'len_b': 5, 'op': 'sub'}},
        {'task': 'common', 'generate': True, 'params': {'len_a': 6, 'len_b': 6}},
    ]

    client1 = ClientThread("Клиент1", q, actions1)
    client2 = ClientThread("Клиент2", q, actions2)
    client3 = ClientThread("Клиент3", q, actions3)

    clients = [client1, client2, client3]
    for c in clients:
        c.start()

    print(f"Запущено клиентов: {len(clients)}")
    print(f"Всего активных потоков: {threading.active_count()}\n")
    print("Наблюдайте за параллельной работой клиентов!\n")

    # дождёмся завершения клиентов (они асинхронно отправили все запросы)
    for c in clients:
        c.join()

    # даём серверу время обработать всё (надёжно — пока очередь не опустеет)
    while not q.empty():
        time.sleep(0.2)
    # чуть подождём, чтобы сервер напечатал завершающие строки результатов
    time.sleep(1.0)

    server.stop()
    # дать серверному потоку выйти
    server.join(timeout=2.0)

if __name__ == "__main__":
    main()

# server.py (diagnostic)
import threading
import queue
import time
import random
import logging
import os
import sys
from datetime import datetime
from task3 import rotate_matrix
from task4 import add_or_sub_bigints
from task8 import common_with_reversed

def ts():
    return datetime.now().strftime("%H:%M:%S")

# ------

# Создаём конфигурацию логирования
logging.basicConfig(
    filename="server.log",          # файл для логирования
    level=logging.INFO,          # уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger("app_logger")

# ---------------------------------------------------------------------

class MatrixServer(threading.Thread):
    """
    Серверный поток, который обрабатывает запросы из общей очереди.


    Parameters
    ----------
    request_queue : queue.Queue
    Очередь, в которую клиенты кладут словари-запросы.


    Attributes
    ----------
    running : bool
    Флаг, управляющий основным циклом обработки.
    processed : int
    Счётчик обработанных запросов.


    Request format
    --------------
    Ожидаемый формат словаря запроса:


    {
    'client': str, # имя клиента
    'task': str, # 'rotate'|'bigint'|'common'
    'data': any, # входные данные: матрица или {'a':..., 'b':...}
    'params': dict, # дополнительные параметры
    'callback': callable # функция для уведомления клиента
    }


    Methods
    -------
    run()
    Основной цикл: извлекает запросы из очереди, логгирует вход, вызывает
    соответствующую функцию (`rotate_matrix`, `add_or_sub_bigints`,
    `common_with_reversed`), логгирует результат и вызывает callback.
    stop()
    Останавливает цикл обработки, записывает итог в лог и вызывает
    `logging.shutdown()` для сброса буферов.
    _print_result(task, result)
    Утилитарный метод для форматированного вывода результата в лог.
    """
    def __init__(self, request_queue: queue.Queue):
        super().__init__(daemon=True)
        self.request_queue = request_queue
        self.running = True
        self.processed = 0

    def run(self):
        logger.info("Сервер: инициализирован и готов к обработке запросов")
        logger.info("="*60)
        logger.info("ДЕМОНСТРАЦИЯ МНОГОПОТОЧНОСТИ В PYTHON")
        logger.info("="*60)
        logger.info("Сервер: один поток")
        logger.info("Клиенты: каждый в отдельном потоке")
        logger.info("="*60)
        logger.info(f"Основной поток: ID {threading.get_ident()}")
        logger.info(f"Активные потоки: {threading.active_count()}\n")
        logger.info("Запуск автоматической демонстрации...")
        logger.info("Клиенты будут выполнять команды автоматически\n")

        while self.running:
            try:
                request = self.request_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            client = request.get('client')
            task = request.get('task')
            data = request.get('data')
            params = request.get('params', {})
            callback = request.get('callback')

            logger.info(f"Сервер {client}: получен запрос на {self._task_name(task)}")

            # эмуляция времени обработки
            process_time = random.uniform(0.6, 2.2)
            time.sleep(process_time)

            result = None
            try:
                if task == 'rotate':
                    direction = params.get('direction', 'cw')
                    result = rotate_matrix(data, direction=direction)
                    logger.info(f"Сервер {client}: Направление: {direction}")
                elif task == 'bigint':
                    op = params.get('op', 'add')
                    result = add_or_sub_bigints(data['a'], data['b'], op=op)
                elif task == 'common':
                    result = common_with_reversed(data['a'], data['b'])
                else:
                    result = {"error": "unknown task"}
            except Exception as e:
                result = {"error": str(e)}
                logger.exception("Ошибка при обработке запроса")

            self.processed += 1
            logger.info(f"Сервер {client}: выполнен {self._task_name(task)} (время={process_time:.2f}s)")

            # ПОЛНЫЙ вывод результата в лог
            # self._print_result(task, result)

            # вызвать callback у клиента (передаём также входные данные для удобства)
            if callable(callback):
                try:
                    callback(client, task, result, data)
                except Exception:
                    logger.exception("Ошибка в callback клиента")

    def stop(self):
        self.running = False
        logger.info(f"\nСервер обработал {self.processed} запросов")

    def _task_name(self, task_key):
        mapping = {
            'rotate': 'поворот матрицы',
            'bigint': 'операция над большими числами',
            'common': 'поиск общих чисел'
        }
        return mapping.get(task_key, task_key)

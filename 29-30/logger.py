import logging

# Создаём конфигурацию логирования
logging.basicConfig(
    filename="app.log",          # файл для логирования
    level=logging.INFO,          # уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger("app_logger")

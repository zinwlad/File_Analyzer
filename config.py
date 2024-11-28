import logging
from pathlib import Path

# Настройки логирования
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = logging.INFO
LOG_FILE = 'file_analyzer.log'

# Настройки интерфейса
WINDOW_TITLE = "Анализатор файлов"
WINDOW_SIZE = "800x600"
DEFAULT_FONT = ("Arial", 10)

# Настройки анализа
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
SUPPORTED_EXTENSIONS = {
    '.pdf': 'PDF файлы',
    '.docx': 'DOCX файлы',
    '.txt': 'Текстовые файлы'
}

# Настройки кэширования
CACHE_DIR = Path('.cache')
CACHE_EXPIRATION = 3600  # 1 час в секундах

# Создание директории для кэша, если она не существует
CACHE_DIR.mkdir(exist_ok=True)

def setup_logging():
    """Настройка системы логирования."""
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

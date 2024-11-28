from abc import ABC, abstractmethod
import logging
from typing import Dict, List, Any

class BaseAnalyzer(ABC):
    """Базовый класс для всех анализаторов файлов."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @abstractmethod
    def analyze(self) -> Dict[str, Any]:
        """
        Основной метод анализа файла.
        Должен быть реализован в каждом конкретном анализаторе.
        """
        pass
    
    def count_words(self, text: str) -> int:
        """Подсчет количества слов в тексте."""
        return len(text.split())
    
    def count_chars(self, text: str) -> int:
        """Подсчет количества символов в тексте."""
        return len(text)
    
    def format_results(self, results: Dict[str, Any]) -> str:
        """Форматирование результатов анализа."""
        formatted = []
        for key, value in results.items():
            if isinstance(value, (list, tuple)):
                formatted.append(f"\n{key}:")
                for item in value:
                    formatted.append(f"  - {item}")
            else:
                formatted.append(f"{key}: {value}")
        return "\n".join(formatted)
    
    def validate_file(self) -> bool:
        """Базовая валидация файла."""
        try:
            with open(self.file_path, 'rb') as f:
                # Проверяем, что файл существует и доступен для чтения
                f.read(1)
            return True
        except Exception as e:
            self.logger.error(f"Ошибка при валидации файла {self.file_path}: {str(e)}")
            return False

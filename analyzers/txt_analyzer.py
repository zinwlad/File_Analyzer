import chardet
from collections import Counter
from typing import Dict, Any
import re
from .base_analyzer import BaseAnalyzer


class TxtAnalyzer(BaseAnalyzer):
    """Анализатор текстовых файлов."""

    def detect_encoding(self) -> str:
        """Определение кодировки файла."""
        with open(self.file_path, 'rb') as file:
            raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

    def analyze(self) -> Dict[str, Any]:
        """Анализ текстового файла."""
        if not self.validate_file():
            return {"error": "Ошибка при открытии файла"}

        try:
            encoding = self.detect_encoding()
            with open(self.file_path, 'r', encoding=encoding) as file:
                content = file.read()

            # Базовая статистика
            lines = content.split('\n')
            words = re.findall(r'\b\w+\b', content.lower())
            
            # Расширенная статистика
            word_frequencies = Counter(words).most_common(10)
            avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
            avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
            
            # Определение пустых строк и строк с пробелами
            empty_lines = sum(1 for line in lines if not line.strip())
            whitespace_lines = sum(1 for line in lines if line.isspace())
            
            # Подсчет специальных символов
            special_chars = len(re.findall(r'[^a-zA-Zа-яА-Я0-9\s]', content))

            results = {
                "Кодировка файла": encoding,
                "Количество строк": len(lines),
                "Количество слов": len(words),
                "Количество символов": len(content),
                "Количество символов (без пробелов)": len(content.replace(" ", "")),
                "Пустые строки": empty_lines,
                "Строки, содержащие только пробелы": whitespace_lines,
                "Специальные символы": special_chars,
                "Средняя длина слова": f"{avg_word_length:.2f}",
                "Средняя длина строки": f"{avg_line_length:.2f}",
                "Топ-10 самых частых слов": [f"{word}: {count}" for word, count in word_frequencies]
            }

            return results

        except Exception as e:
            self.logger.error(f"Ошибка при анализе файла: {str(e)}")
            return {"error": f"Ошибка при анализе файла: {str(e)}"}


def analyze_txt(file_path: str) -> str:
    """Функция-обертка для обратной совместимости."""
    analyzer = TxtAnalyzer(file_path)
    results = analyzer.analyze()
    return analyzer.format_results(results)

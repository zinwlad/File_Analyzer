import fitz
from typing import Dict, Any, Set
from .base_analyzer import BaseAnalyzer


class PdfAnalyzer(BaseAnalyzer):
    """Анализатор PDF файлов."""

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.rgb_pages: Set[int] = set()
        self.cmyk_pages: Set[int] = set()
        self.grayscale_pages: Set[int] = set()
        self.font_set: Set[str] = set()
        self.font_sizes: list = []

    def analyze(self) -> Dict[str, Any]:
        """Анализ PDF файла."""
        if not self.validate_file():
            return {"error": "Ошибка при открытии файла"}

        try:
            doc = fitz.open(self.file_path)
        except Exception as e:
            self.logger.error(f"Ошибка при открытии PDF файла: {str(e)}")
            return {"error": f"Ошибка при открытии PDF файла: {str(e)}"}

        results = {
            "Количество страниц": doc.page_count,
            "Метаданные": [],
            "Статистика изображений": [],
            "Форматы изображений": "Нет данных"
        }

        try:
            # Пробуем получить метаданные
            metadata = self._extract_metadata(doc)
            results["Метаданные"] = [f"{k}: {v}" for k, v in metadata.items()]
        except Exception as e:
            self.logger.warning(f"Не удалось получить метаданные: {str(e)}")

        total_images = 0
        image_stats = {'RGB': 0, 'CMYK': 0, 'Grayscale': 0}
        image_formats = set()

        # Анализ каждой страницы
        for page_num in range(doc.page_count):
            try:
                page = doc[page_num]
                
                # Анализ изображений на странице
                try:
                    images = page.get_images(full=True)
                    for img in images:
                        total_images += 1
                        try:
                            pix = fitz.Pixmap(doc, img[0])
                            if pix.colorspace:
                                if pix.colorspace.n == 3:
                                    image_stats['RGB'] += 1
                                    self.rgb_pages.add(page_num + 1)
                                elif pix.colorspace.n == 4:
                                    image_stats['CMYK'] += 1
                                    self.cmyk_pages.add(page_num + 1)
                                elif pix.colorspace.n == 1:
                                    image_stats['Grayscale'] += 1
                                    self.grayscale_pages.add(page_num + 1)
                        except Exception as e:
                            self.logger.warning(f"Не удалось проанализировать изображение на странице {page_num + 1}: {str(e)}")
                except Exception as e:
                    self.logger.warning(f"Не удалось получить список изображений на странице {page_num + 1}: {str(e)}")

                # Анализ шрифтов на странице
                try:
                    text_dict = page.get_text("dict")
                    if 'fonts' in text_dict:
                        for font in text_dict['fonts']:
                            self.font_set.add(font.get('name', 'Неизвестный шрифт'))
                            if 'size' in font:
                                self.font_sizes.append(font['size'])
                except Exception as e:
                    self.logger.warning(f"Не удалось проанализировать шрифты на странице {page_num + 1}: {str(e)}")

            except Exception as e:
                self.logger.warning(f"Не удалось проанализировать страницу {page_num + 1}: {str(e)}")
                continue

        # Формируем результаты
        results.update({
            "Общее количество изображений": total_images,
            "RGB изображения на страницах": sorted(self.rgb_pages) if self.rgb_pages else "Нет",
            "CMYK изображения на страницах": sorted(self.cmyk_pages) if self.cmyk_pages else "Нет",
            "Grayscale изображения на страницах": sorted(self.grayscale_pages) if self.grayscale_pages else "Нет",
            "Использованные шрифты": sorted(self.font_set) if self.font_set else "Нет данных",
            "Статистика изображений": [f"{k}: {v}" for k, v in image_stats.items()],
            "Размеры шрифтов": f"Мин: {min(self.font_sizes):.1f}, Макс: {max(self.font_sizes):.1f}" if self.font_sizes else "Нет данных"
        })

        doc.close()
        return results

    def _extract_metadata(self, doc: fitz.Document) -> Dict[str, str]:
        """Извлечение метаданных документа."""
        metadata = {}
        try:
            metadata['Автор'] = doc.metadata.get('author', 'Неизвестно')
            metadata['Создатель'] = doc.metadata.get('creator', 'Неизвестно')
            metadata['Дата создания'] = doc.metadata.get('creationDate', 'Неизвестно')
            metadata['Дата модификации'] = doc.metadata.get('modDate', 'Неизвестно')
            metadata['Заголовок'] = doc.metadata.get('title', 'Неизвестно')
        except Exception as e:
            self.logger.warning(f"Ошибка при извлечении метаданных: {str(e)}")
        return metadata

    def _format_page_sizes(self, sizes) -> str:
        """Форматирование размеров страниц."""
        if not sizes:
            return "Нет данных"
        
        if all(size == sizes[0] for size in sizes):
            width, height = sizes[0]
            return f"{width:.1f} x {height:.1f} мм"
        return "Разные размеры страниц"


def analyze_pdf(file_path: str) -> str:
    """Функция-обертка для обратной совместимости."""
    analyzer = PdfAnalyzer(file_path)
    results = analyzer.analyze()
    return analyzer.format_results(results)

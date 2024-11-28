"""
Пакет analyzers предоставляет классы для анализа различных типов файлов.
"""

from .txt_analyzer import TxtAnalyzer, analyze_txt
from .pdf_analyzer import PdfAnalyzer, analyze_pdf
from .docx_analyzer import DocxAnalyzer, analyze_docx

__all__ = ['TxtAnalyzer', 'PdfAnalyzer', 'DocxAnalyzer',
           'analyze_txt', 'analyze_pdf', 'analyze_docx']

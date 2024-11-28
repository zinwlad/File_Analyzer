import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from analyzers.txt_analyzer import analyze_txt
from analyzers.pdf_analyzer import analyze_pdf
from analyzers.docx_analyzer import analyze_docx
from config import WINDOW_TITLE, WINDOW_SIZE, SUPPORTED_EXTENSIONS, setup_logging
import threading


def browse_file():
    """Открывает диалоговое окно для выбора файла и запускает анализ."""
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf"), ("DOCX files", "*.docx"), ("Text files", "*.txt")])
    if file_path:
        start_analysis(file_path)


def start_analysis(file_path):
    """Запускает процесс анализа файла в отдельном потоке."""
    extension = os.path.splitext(file_path)[1].lower()
    result_text_widget.config(state=tk.NORMAL)
    result_text_widget.delete(1.0, tk.END)
    result_text_widget.config(state=tk.DISABLED)

    # Запускаем индикатор загрузки
    progress_bar.start()

    # Запускаем анализ в отдельном потоке, чтобы не блокировать интерфейс
    thread = threading.Thread(target=analyze_file, args=(file_path, extension))
    thread.start()


def analyze_file(file_path, extension):
    """Производит анализ файла в зависимости от его расширения."""
    result_text = ""

    if extension == '.pdf':
        result_text = analyze_pdf(file_path)
    elif extension == '.docx':
        result_text = analyze_docx(file_path)
    elif extension == '.txt':
        result_text = analyze_txt(file_path)
    else:
        result_text = "Неподдерживаемый формат файла."

    # Останавливаем индикатор загрузки
    progress_bar.stop()

    # Обновляем текстовое поле с результатом
    update_result_text(result_text)


def update_result_text(result_text):
    """Обновляет текстовое поле с результатом анализа."""
    result_text_widget.config(state=tk.NORMAL)
    result_text_widget.delete(1.0, tk.END)
    result_text_widget.insert(tk.END, result_text)
    result_text_widget.config(state=tk.DISABLED)


def reset():
    """Сбрасывает результаты и очищает текстовое поле."""
    result_text_widget.config(state=tk.NORMAL)
    result_text_widget.delete(1.0, tk.END)
    result_text_widget.config(state=tk.DISABLED)


def cancel_analysis():
    """Позволяет отменить анализ файла (функционал пока заглушка)."""
    # Здесь можно добавить логику для остановки анализа
    messagebox.showinfo("Отмена", "Анализ файла был отменен.")
    progress_bar.stop()


# Настройка интерфейса
root = tk.Tk()
root.title(WINDOW_TITLE)

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

browse_button = tk.Button(frame, text="Открыть файл", command=browse_file)
browse_button.pack(side=tk.LEFT)

reset_button = tk.Button(frame, text="Сброс", command=reset)
reset_button.pack(side=tk.LEFT)

cancel_button = tk.Button(frame, text="Отмена", command=cancel_analysis)
cancel_button.pack(side=tk.LEFT)

# Поле для результатов
result_text_widget = tk.Text(root, wrap=tk.WORD, height=20, width=80)
result_text_widget.pack(padx=10, pady=10)
result_text_widget.config(state=tk.DISABLED)

# Индикатор загрузки
progress_bar = ttk.Progressbar(root, orient="horizontal", mode="indeterminate")
progress_bar.pack(fill=tk.X, padx=10, pady=10)

# Запуск основного цикла обработки событий
root.mainloop()

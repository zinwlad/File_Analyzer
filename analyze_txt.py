def analyze_txt(txt_path):
    """Анализирует TXT-файл и собирает статистику."""
    try:
        with open(txt_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        return f"Не удалось открыть TXT-файл: {e}"

    total_lines = content.count('\n')
    total_words = len(content.split())
    total_chars = len(content)

    result = []
    result.append(f"Количество строк: {total_lines}")
    result.append(f"Количество слов: {total_words}")
    result.append(f"Количество символов: {total_chars}")

    return "\n".join(result)

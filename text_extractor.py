import pdfplumber
import re
from collections import defaultdict

def extract_clean_text(pdf_path):
    
    pattern_static = "Integration Platform – Создание и управление definition json"
    pattern_toc = r"Ошибка! Используйте вкладку \"Главная\".*– \d+"

    all_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[6:]:
            page_parts = []

            # Получаем bounding boxes таблиц
            table_bboxes = [t.bbox for t in page.find_tables()]

            # Слова с координатами
            words = page.extract_words()

            # Группируем слова по Y-координате (строки)
            lines = defaultdict(list)

            for word in words:
                word_center_y = (float(word["top"]) + float(word["bottom"])) / 2
                word_center_x = (float(word["x0"]) + float(word["x1"])) / 2

                # Проверяем, находится ли слово внутри какой-либо таблицы
                inside_table = any(
                    x0 <= word_center_x <= x1 and top <= word_center_y <= bottom
                    for (x0, top, x1, bottom) in table_bboxes
                )

                if not inside_table:
                    # Группируем слова по строкам (приближённо по Y)
                    line_key = round(word_center_y, 1)
                    lines[line_key].append((float(word["x0"]), word["text"]))

            # Сортируем строки по Y, внутри строки по X
            for y in sorted(lines.keys()):
                line = " ".join(word for _, word in sorted(lines[y]))
                if pattern_static in line:
                    continue
                if re.match(pattern_toc, line):
                    continue
                page_parts.append(line)

            # Добавляем таблицы
            for table in page.extract_tables():
                for row in table:
                    row_text = " | ".join(cell.replace("\n", "").strip() if cell else "" for cell in row)
                    page_parts.append(row_text)

            all_text.append(" ".join(page_parts))

    return " ".join(all_text) 
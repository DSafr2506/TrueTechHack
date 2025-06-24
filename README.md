# PDF Text Embedding Project

Проект для извлечения текста из PDF документов, его разбиения на чанки и создания эмбеддингов для семантического поиска.

## Структура проекта

- `text_extractor.py` - модуль для извлечения текста из PDF файлов
- `text_chunker.py` - модуль для разбиения текста на чанки
- `embeddings.py` - модуль для работы с эмбеддингами
- `utils.py` - вспомогательные функции
- `config.py` - конфигурационный файл
- `cli.py` - командный интерфейс
- `tests/` - тесты
- `requirements.txt` - зависимости проекта

## Установка

1. Клонируйте репозиторий:
```bash
git clone [url-репозитория]
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Скачайте необходимые модели NLTK:
```python
import nltk
nltk.download('punkt')
```

## Использование

### Через Python API

1. Извлечение текста из PDF:
```python
from text_extractor import extract_clean_text

text = extract_clean_text("path/to/your.pdf")
```

2. Разбиение текста на чанки:
```python
from text_chunker import chunk_text_by_tokens

chunks = chunk_text_by_tokens(text, max_tokens=512, overlap=2)
```

3. Работа с эмбеддингами:
```python
from embeddings import EmbeddingManager

manager = EmbeddingManager()
embeddings = [manager.get_embedding(chunk) for chunk in chunks]

# Поиск релевантных чанков
relevant_chunks = manager.find_nearest_chunks(
    "ваш запрос",
    embeddings,
    chunks,
    num_top_chunks=3
)
```

### Через командную строку

1. Обработка PDF файла:
```bash
python cli.py process path/to/your.pdf --output data/embeddings.json
```

2. Поиск по эмбеддингам:
```bash
python cli.py search "ваш запрос" --embeddings data/embeddings.json --top-k 3
```

## Запуск тестов

```bash
python -m unittest discover tests
```

## Конфигурация

Настройки проекта можно изменить в файле `config.py`:
- Параметры извлечения текста
- Настройки чанков
- Параметры эмбеддингов
- Настройки поиска
- Пути к файлам

## Требования

- Python 3.7+
- pdfplumber
- nltk
- tiktoken
- numpy
- sentence-transformers

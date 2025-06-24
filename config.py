"""
Конфигурационный файл проекта
"""

# Настройки для извлечения текста
TEXT_EXTRACTOR_CONFIG = {
    'start_page': 6,  # Начальная страница для извлечения
    'patterns_to_remove': [
        "Integration Platform – Создание и управление definition json",
        r"Ошибка! Используйте вкладку \"Главная\".*– \d+"
    ]
}

# Настройки для чанков
CHUNKER_CONFIG = {
    'max_tokens': 512,
    'overlap': 2,
    'model_name': "cl100k_base"
}

# Настройки для эмбеддингов
EMBEDDING_CONFIG = {
    'model_name': "intfloat/multilingual-e5-small",
    'query_prompt': "query: ",
    'passage_prompt': "passage: ",
    'normalize_embeddings': True
}

# Настройки для поиска
SEARCH_CONFIG = {
    'num_top_chunks': 10,
    'min_similarity_threshold': 0.5
}

# Пути к файлам
PATHS = {
    'embeddings_file': "data/chunks_embeddings.json",
    'test_data_dir': "tests/test_data"
} 
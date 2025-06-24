import numpy as np

def find_chunk_indices(user_embedding: np.ndarray, embeddings: list, num_top_chunks: int):
    """
    Находит индексы наиболее похожих чанков.
    
    Args:
        user_embedding (np.ndarray): Эмбеддинг запроса пользователя
        embeddings (list): Список эмбеддингов
        num_top_chunks (int): Количество возвращаемых чанков
        
    Returns:
        list: Индексы наиболее похожих чанков
    """
    similarities = [cosine_similarity(user_embedding, emb) for emb in embeddings]
    sorted_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)
    return sorted_indices[:num_top_chunks]

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Вычисляет косинусное сходство между двумя векторами.
    
    Args:
        a (np.ndarray): Первый вектор
        b (np.ndarray): Второй вектор
        
    Returns:
        float: Значение косинусного сходства
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)) 
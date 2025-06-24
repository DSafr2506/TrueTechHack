import nltk
import tiktoken
import numpy as np
from nltk.tokenize import sent_tokenize

def count_tokens(text, tokenizer):
    """
    Подсчитывает количество токенов в тексте.
    
    Args:
        text (str): Входной текст
        tokenizer: Токенизатор
        
    Returns:
        int: Количество токенов
    """
    return len(tokenizer.encode(text))

def chunk_text_by_tokens(text, max_tokens=512, overlap=2, model_name="cl100k_base"):
    """
    Разбивает текст на чанки с учетом максимального количества токенов.
    
    Args:
        text (str): Входной текст
        max_tokens (int): Максимальное количество токенов в чанке
        overlap (int): Количество перекрывающихся предложений
        model_name (str): Название модели токенизации
        
    Returns:
        list: Список чанков текста
    """
    tokenizer = tiktoken.get_encoding(model_name)
    sentences = sent_tokenize(text)

    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = count_tokens(sentence, tokenizer)

        if sentence_tokens + current_tokens > max_tokens:
            words = sentence.split()

            for word in words:
                word_tokens = count_tokens(word, tokenizer)
                if current_tokens + word_tokens > max_tokens:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = current_chunk[-overlap:] if overlap else []
                    current_tokens = sum(count_tokens(w, tokenizer) for w in current_chunk)

                current_chunk.append(word)
                current_tokens += word_tokens
            continue

        if current_tokens + sentence_tokens > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = current_chunk[-overlap:] if overlap else []
            current_tokens = sum(count_tokens(w, tokenizer) for w in current_chunk)

        current_chunk.append(sentence)
        current_tokens += sentence_tokens

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def verify_chunks_integrity(original_text, chunks):
    
    reconstructed_text = " ".join(chunks)

    stats = {
        'original_length': len(original_text),
        'reconstructed_length': len(reconstructed_text),
        'position_of_first_diff': None,
        'diff_samples': []
    }

    for i, (orig_char, rec_char) in enumerate(zip(original_text, reconstructed_text)):
        if orig_char != rec_char:
            stats['position_of_first_diff'] = i
            stats['diff_samples'] = [
                original_text[max(0, i-5):i+5],
                reconstructed_text[max(0, i-5):i+5]
            ]
            return False, stats

    return True, stats 
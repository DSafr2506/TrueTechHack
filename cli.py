import argparse
import os
from text_extractor import extract_clean_text
from text_chunker import chunk_text_by_tokens
from embeddings import EmbeddingManager
from config import TEXT_EXTRACTOR_CONFIG, CHUNKER_CONFIG, EMBEDDING_CONFIG, PATHS

def setup_argparse():
    parser = argparse.ArgumentParser(description='PDF Text Embedding Project')
    subparsers = parser.add_subparsers(dest='command', help='Команды')
    
    # Команда для обработки PDF
    process_parser = subparsers.add_parser('process', help='Обработать PDF файл')
    process_parser.add_argument('pdf_path', help='Путь к PDF файлу')
    process_parser.add_argument('--output', '-o', help='Путь для сохранения эмбеддингов')
    
    # Команда для поиска
    search_parser = subparsers.add_parser('search', help='Поиск по эмбеддингам')
    search_parser.add_argument('query', help='Поисковый запрос')
    search_parser.add_argument('--embeddings', '-e', help='Путь к файлу с эмбеддингами')
    search_parser.add_argument('--top-k', type=int, default=3, help='Количество результатов')
    
    return parser

def process_pdf(pdf_path, output_path=None):
    """Обработка PDF файла и создание эмбеддингов"""
    print(f"Извлечение текста из {pdf_path}...")
    text = extract_clean_text(pdf_path)
    
    print("Разбиение текста на чанки...")
    chunks = chunk_text_by_tokens(text, **CHUNKER_CONFIG)
    
    print("Создание эмбеддингов...")
    manager = EmbeddingManager(EMBEDDING_CONFIG['model_name'])
    embeddings = [manager.get_embedding(chunk, EMBEDDING_CONFIG['passage_prompt']) 
                 for chunk in chunks]
    
    output_path = output_path or PATHS['embeddings_file']
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Сохранение эмбеддингов в {output_path}...")
    manager.save_embeddings_to_json(chunks, embeddings, output_path)
    
    return chunks, embeddings

def search_embeddings(query, embeddings_path=None, top_k=3):
    """Поиск по эмбеддингам"""
    embeddings_path = embeddings_path or PATHS['embeddings_file']
    
    print(f"Загрузка эмбеддингов из {embeddings_path}...")
    manager = EmbeddingManager(EMBEDDING_CONFIG['model_name'])
    chunks, embeddings = manager.load_embeddings_from_json(embeddings_path)
    
    print(f"Поиск по запросу: {query}")
    relevant_chunks = manager.find_nearest_chunks(
        query,
        embeddings,
        chunks,
        num_top_chunks=top_k
    )
    
    return relevant_chunks

def main():
    parser = setup_argparse()
    args = parser.parse_args()
    
    if args.command == 'process':
        process_pdf(args.pdf_path, args.output)
    elif args.command == 'search':
        results = search_embeddings(args.query, args.embeddings, args.top_k)
        print("\nРезультаты поиска:")
        print("-" * 80)
        print(results)
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 
import unittest
from text_chunker import chunk_text_by_tokens, verify_chunks_integrity
import tiktoken

class TestTextChunker(unittest.TestCase):
    def setUp(self):
        self.test_text = "Это тестовый текст. Он содержит несколько предложений. " * 10
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
    def test_chunk_text_by_tokens(self):
        chunks = chunk_text_by_tokens(self.test_text, max_tokens=50)
        # Проверяем, что получили список чанков
        self.assertIsInstance(chunks, list)
        self.assertTrue(len(chunks) > 0)
        
        # Проверяем, что каждый чанк не превышает максимальное количество токенов
        for chunk in chunks:
            tokens = len(self.tokenizer.encode(chunk))
            self.assertLessEqual(tokens, 50)
            
    def test_verify_chunks_integrity(self):
        chunks = chunk_text_by_tokens(self.test_text)
        is_valid, stats = verify_chunks_integrity(self.test_text, chunks)
        
        # Проверяем, что чанки сохраняют целостность текста
        self.assertTrue(is_valid)
        self.assertEqual(stats['original_length'], len(self.test_text))
        self.assertEqual(stats['reconstructed_length'], len(" ".join(chunks)))

if __name__ == '__main__':
    unittest.main() 
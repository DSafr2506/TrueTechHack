import unittest
from text_extractor import extract_clean_text
import os

class TestTextExtractor(unittest.TestCase):
    def setUp(self):
        # Создаем тестовый PDF файл или используем существующий
        self.test_pdf_path = "tests/test_data/test.pdf"
        
    def test_extract_clean_text(self):
        # Проверяем, что функция возвращает строку
        text = extract_clean_text(self.test_pdf_path)
        self.assertIsInstance(text, str)
        self.assertTrue(len(text) > 0)
        
    def test_clean_text_patterns(self):
        text = extract_clean_text(self.test_pdf_path)
        # Проверяем, что статические паттерны удалены
        self.assertNotIn("Integration Platform – Создание и управление definition json", text)
        # Проверяем, что TOC паттерны удалены
        self.assertFalse(any("Ошибка! Используйте вкладку \"Главная\"" in line for line in text.split("\n")))

if __name__ == '__main__':
    unittest.main() 
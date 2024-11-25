import unittest
import json
import os
from book.book import Book
from library.library import Library
import tempfile

class TestLibrary(unittest.TestCase):

    def setUp(self):
        # Создаем временный файл с рандомным именем
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file_path = os.path.join(self.temp_dir.name, 'test_library.json')
        with open(self.test_file_path, 'w', encoding='utf-8') as file:
            json.dump([], file)
        self.library = Library(self.test_file_path)
        self.book1 = Book(1, 'Title1', 'Author1', 2000, 'в наличии')
        self.book2 = Book(2, 'Title2', 'Author2', 2001, 'в наличии')
        self.library._books = [self.book1, self.book2]
        self.library._next_id = 3
        self.library.save_books()

    def tearDown(self):
        # Удаляем временный файл и директорию
        self.temp_dir.cleanup()

    def test_load_books(self):
        library = Library(self.test_file_path)
        self.assertEqual(len(library.books), 2)
        self.assertEqual(library.books[0].title, 'Title1')
        self.assertEqual(library.books[1].author, 'Author2')

    def test_get_next_id(self):
        self.assertEqual(self.library.next_id, 3)

    def test_add_book(self):
        self.library.add_book('Title3', 'Author3', 2002)
        self.assertEqual(len(self.library.books), 3)
        self.assertEqual(self.library.books[2].title, 'Title3')
        self.assertEqual(self.library.next_id, 4)

    def test_delete_book(self):
        self.assertTrue(self.library.delete_book(1))
        self.assertEqual(len(self.library.books), 1)
        self.assertFalse(self.library.delete_book(1))

    def test_search_book(self):
        results = self.library.search_book(title='Title1')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Title1')

        results = self.library.search_book(author='Author2')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, 'Author2')

    def test_update_book_status(self):
        self.assertTrue(self.library.update_book_status(1, 'нет в наличии'))
        self.assertEqual(self.library.books[0].status, 'нет в наличии')
        self.assertFalse(self.library.update_book_status(999, 'нет в наличии'))

if __name__ == '__main__':
    unittest.main()

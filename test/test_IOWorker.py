import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from library.library import Library
from main import IOWorker, main

class TestIOWorker(unittest.TestCase):

    def setUp(self):
        self.library = MagicMock(spec=Library)
        self.worker = IOWorker(self.library)

    @patch('builtins.input', side_effect=['Title', 'Author', '2020'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_book_success(self, mock_stdout, mock_input):
        self.worker.add_book()
        self.library.add_book.assert_called_once_with('Title', 'Author', 2020)
        self.assertIn("Книга 'Title' за авторством Author, 2020 года выпуска, добавлена.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['Title', 'Author', 'invalid_year'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_book_invalid_year(self, mock_stdout, mock_input):
        self.worker.add_book()
        self.assertIn("Введите корректный год", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['Title', 'Author', '2025'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_book_future_year(self, mock_stdout, mock_input):
        self.worker.add_book()
        self.assertIn("Год выпуска книги не корректен", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['1'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_delete_book_success(self, mock_stdout, mock_input):
        self.library.delete_book.return_value = True
        self.worker.delete_book()
        self.library.delete_book.assert_called_once_with(1)
        self.assertIn("Книга с id: 1 удалена.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['1'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_delete_book_not_found(self, mock_stdout, mock_input):
        self.library.delete_book.return_value = False
        self.worker.delete_book()
        self.library.delete_book.assert_called_once_with(1)
        self.assertIn("Книга с id: 1 не найдена.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['invalid_id'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_delete_book_invalid_id(self, mock_stdout, mock_input):
        self.worker.delete_book()
        self.assertIn("id введен некорректно", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['Title', 'Author', '2020'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_search_book_success(self, mock_stdout, mock_input):
        self.library.search_book.return_value = []
        self.worker.search_book()
        self.library.search_book.assert_called_once_with(title='title', author='author', year=2020)
        self.assertIn("Книг не найдено", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['Title', 'Author', 'invalid_year'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_search_book_invalid_year(self, mock_stdout, mock_input):
        self.worker.search_book()
        self.assertIn("Введите корректный год", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['1', 'в наличии'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_update_book_status_success(self, mock_stdout, mock_input):
        self.library.update_book_status.return_value = True
        self.worker.update_book_status()
        self.library.update_book_status.assert_called_once_with(1, 'в наличии')
        self.assertIn("Статус книги с id: 1 изменен на в наличии.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['1', 'invalid_status'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_update_book_status_invalid_status(self, mock_stdout, mock_input):
        self.worker.update_book_status()
        self.assertIn("Введите корректный статус", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['invalid_id', 'в наличии'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_update_book_status_invalid_id(self, mock_stdout, mock_input):
        self.worker.update_book_status()
        self.assertIn("ID не корректен", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_all_books_empty(self, mock_stdout):
        self.library.books = []
        self.worker.show_all_books()
        self.assertIn("Библиотека пуста", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_all_books_non_empty(self, mock_stdout):
        self.library.books = [MagicMock()]
        self.worker.show_all_books()
        self.assertNotIn("Библиотека пуста", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['6'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_exit(self, mock_stdout, mock_input):
        with patch('builtins.open', side_effect=lambda *args, **kwargs: StringIO()):
            with patch('os.path.exists', return_value=False):
                with self.assertRaises(SystemExit):
                    main()

if __name__ == '__main__':
    unittest.main()
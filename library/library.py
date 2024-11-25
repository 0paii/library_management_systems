import json
from book.book import Book
from typing import List


class Library:
    """
    Класс библиотеки

    Attributes:
        file_path (str): путь к файлу с данными библиотеки
        _books (list): список книг
        _next_id (int): следующий id книги

    """

    def __init__(self, file_path='library.json'):
        """
        Конструктор класса Library

        :param file_path: путь к файлу с данными библиотеки
        """
        self.file_path = file_path
        self._books = self.load_books()
        self._next_id = self.get_next_id()

    @property
    def books(self) -> List[Book]:
        """
        Property, возвращающий список книг библиотеки

        Returns:
            list: список книг
        """
        return self._books

    @property
    def next_id(self) -> int:
        """
        Property, возвращающий следующий id книги

        Returns:
            int: следующий id книги
        """
        return self._next_id

    def load_books(self) -> List[Book]:
        """
        Метод, загружающий список книг из файла.

        :return: list[book], Список книг
        """
        result = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            try:
                temp_result = json.load(file)
                for book in temp_result:
                    result.append(Book(book['id'], book['title'], book['author'], book['year'], book['status']))
                return result
            except json.JSONDecodeError:
                return result

    def get_next_id(self) -> int:
        """
        Метод, возвращающий следующий id книги.

        :return: int, следующий id книги
        """
        return max([book.book_id for book in self._books], default=0) + 1

    def save_books(self):
        """
        Метод, сохраняющий список книг в файл

        Метод проходит по списку книг, создает из них словари,
        и сохраняет их в файле, указанном в self.file_path
        """
        result = []
        with open(self.file_path, 'w', encoding='utf-8') as file:
            for book in self.books:
                result.append({
                    'id': book.book_id,
                    'title': book.title,
                    'author': book.author,
                    'year': book.year,
                    'status': book.status
                })
            json.dump(result, file, ensure_ascii=False, indent=4)

    def add_book(self, book_title: str, book_author: str, book_year: int):
        """
        Метод, добавляющий книгу в список книг.

        :param book_title: str, Название книги
        :param book_author: str, Автор книги
        :param book_year: int, Год издания книги
        """
        book = Book(self._next_id, book_title, book_author, book_year, status='в наличии')
        self._books.append(book)
        self._next_id += 1
        self.save_books()

    def delete_book(self, book_id: int) -> bool:
        """
        Метод, удаляющий книгу из списка книг.

        :param book_id: int, id книги, которую нужно удалить
        :return: bool, True если книга была удалена, False если не найдена
        """
        for book in self._books:
            if book.book_id == book_id:
                self._books.remove(book)
                self.save_books()
                return True
        return False

    def search_book(self, **kwargs) -> List[Book]:
        """
        Метод, выполняющий поиск книг по заданным критериям.

        :param kwargs: словарь, содержащий поля, по которым производится поиск
        :return: list[Book], список книг, удовлетворяющих критериям поиска
        """
        results = [book for book in self._books if book.search(**kwargs)]
        return results

    def update_book_status(self, book_id: int, new_book_status: str) -> bool:
        """
        Метод, изменяющий статус книги.

        :param book_id: int, id книги, статус которой нужно изменить
        :param new_book_status: str, новый статус книги
        :return: bool, True если книга была найдена и статус был изменен, False если не найдена
        """
        for book in self._books:
            if book.book_id == book_id:
                book.status = new_book_status
                self.save_books()
                return True
        return False

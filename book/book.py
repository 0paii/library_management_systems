class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str):
        """
        Метод __init__
        :param book_id: id книги
        :param title: название книги
        :param author: автор книги
        :param year: год издания книги
        :param status: статус книги
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        """
        Метод __str__
        :return: str
        """
        return f"ID: {self.book_id}, Название: {self.title}, Автор: {self.author}, Год издания: {self.year}, Статус: {self.status}"

    def search(self, **kwargs) -> bool:
        """
        Метод search
        :param kwargs: словарь, содержащий поля, по которым производится поиск
        :return: bool, True если книга была найдена, False если не найдена
        """
        if all(value is None for value in kwargs.values()):  # Проверка на пустой словарь
            return False
        result = True
        for key, value in kwargs.items():
            if value is not None:  # Проверка на пустоту значения
                if key == 'year' or key == 'id':
                    result = self.__dict__.get(key) == int(value) and result
                else:
                    result = self.__dict__.get(key).lower() == value.lower() and result
        return result

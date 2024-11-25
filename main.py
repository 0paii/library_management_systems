import sys
from datetime import date
from os.path import exists
from library.library import Library


class IOWorker:
    """
    Класс обработчика данных библиотеки.

    Attributes:
        library (Library): Объект библиотеки.
    """
    def __init__(self, library):
        """
        Конструктор класса IOWorker

        :param library: Объект библиотеки
        """
        self.library = library

    def add_book(self):
        """
        Метод для добавления книги в библиотеку.

        Запрашивает у пользователя название, автора и год издания книги.
        Проверяет корректность введенного года. Если данные корректны,
        добавляет книгу в библиотеку и выводит сообщение об успешном добавлении.
        В случае ошибки выводит соответствующее сообщение.

        :return: None
        """
        try:
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания: "))
            if year < 0 or date.today().year < year:
                print("\nГод выпуска книги не корректен\n")
                return
            self.library.add_book(title, author, year)
            print(f"\nКнига '{title}' "
                  f"за авторством {author}, "
                  f"{year} года выпуска, добавлена.\n")
        except AttributeError:
            print("\nДанные книги не корректны\n")
        except ValueError:
            print("\nВведите корректный год\n")

    def delete_book(self):

        """
        Метод, удаляющий книгу из списка книг.

        :return: None
        """
        try:
            book_id = int(input("Введите id книги для удаления: "))
            if self.library.delete_book(book_id):
                print(f"\nКнига с id: {book_id} удалена.\n")
            else:
                print(f"\nКнига с id: {book_id} не найдена.\n")
        except ValueError:
            print("\nid введен некорректно\n")

    def search_book(self):
        """
        Метод, выполняющий поиск книги по заданным критериям.

        Этот метод запрашивает у пользователя название, автора и год издания
        книги, которые могут быть использованы в качестве критериев поиска.
        Все параметры являются необязательными. Затем он вызывает метод
        search_book из объекта библиотеки с указанными параметрами.
        Если найдены подходящие книги, они выводятся на экран.

        :return: None
        """
        try:
            title = input("Введите название книги (опционально): ").lower()
            author = input("Введите автора книги (опционально): ").lower()
            year = input("Введите год издания книги (опционально): ")
            search_params = {
                "title": title if title else None,
                "author": author if author else None,
                "year": int(year) if year else None,
            }
            result = self.library.search_book(**search_params)
            if result:
                for book in result:
                    print(book)
            else:
                print("\nКниг не найдено\n")
        except AttributeError:
            print("\nОшибка поиска\n")
        except ValueError:
            print("\nВведите корректный год\n")

    def update_book_status(self):
        """
        Изменяет статус книги в библиотеке.

        Метод запрашивает у пользователя ID книги и новый статус ('В наличии' или 'Выдана').
        Если статус введен некорректно, выводится сообщение об ошибке.
        В противном случае, метод вызывает соответствующий метод библиотеки для изменения статуса книги.
        Если книга найдена и статус изменен успешно, выводится подтверждающее сообщение.
        Если книга с указанным ID не найдена, выводится соответствующее сообщение об ошибке.

        :return: None
        """
        try:
            book_id = int(input("Введите ID книги для изменения статуса: "))
            new_book_status = input("Введите новый статус ('В наличии' или 'Выдана'): ").lower()
            match new_book_status:
                case "d yfkbxbb":
                    new_book_status = 'в наличии'
                case "dslfyf":
                    new_book_status = 'выдана'
            if new_book_status not in ["в наличии", "выдана"]:
                print("\nВведите корректный статус\n")
            else:
                if self.library.update_book_status(book_id, new_book_status):
                    print(f"\nСтатус книги с id: {book_id} изменен на {new_book_status}.\n")
                else:
                    print(f"\nКнига с id: {book_id} не найдена.\n")
        except ValueError:
            print("\nID не корректен\n")

    def show_all_books(self):

        """
        Выводит на экран список всех книг библиотеки.

        Метод сначала проверяет, не является ли список книг пустым.
        Если он пуст, выводится сообщение об этом.
        Если в библиотеке есть книги, то они выводятся на экран.

        :return: None
        """
        if not self.library.books:
            print("\nБиблиотека пуста\n")
            return
        for book in self.library.books:
            print(book)


def main():
    """
    Главная функция программы.

    Создает объект класса Library, создает объект класса IOWorker, передавая ему
    созданный объект Library, и запускает основной цикл работы программы.

    В цикле отображается меню, пользователь выбирает пункты меню, и
    соответствующие методы объекта IOWorker вызываются.

    """
    if not exists("library.json"):
        open("library.json", "w+").close()
    library = Library()
    worker = IOWorker(library)
    while True:
        print("Меню:\n"
              "1. Добавить книгу.\n"
              "2. Удалить книгу.\n"
              "3. Изменить статус книги.\n"
              "4. Отобразить все книги.\n"
              "5. Найти книгу.\n"
              "6. Выход.\n"
              )
        choice = input("Выберите действие: ")
        match choice:
            case "1":
                worker.add_book()

            case "2":
                worker.delete_book()

            case "3":
                worker.update_book_status()

            case "4":
                worker.show_all_books()

            case "5":
                worker.search_book()

            case "6":
                sys.exit()

            case _:
                print("\nПожалуйста выберите номер из меню ниже :)\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nДля этого есть отдельная функция, пожалуйста используйте её)\n")

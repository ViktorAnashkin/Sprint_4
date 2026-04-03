import pytest
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_genre содержит добавленные книги, его длина должна быть равна 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()
    
    # тест: попытка добавления книги с названием длиннее 40 символов
    # проверяет ограничение на длину названия книги (максимум 40 символов)
    def test_add_new_book_long_name(self):
        collector = BooksCollector()
        long_name = 'Эта книга имеет очень длинное название, которое точно больше сорока символов'
        collector.add_new_book(long_name)
        assert long_name not in collector.books_genre
        
    # тест: попытка повторного добавления книги
    # проверяет, что одна и та же книга не может быть добавлена в коллекцию дважды
    def test_add_new_book_duplicate(self):
        collector = BooksCollector()
        book_name = 'Мастер и Маргарита'
        collector.add_new_book(book_name)
        collector.add_new_book(book_name)
        assert len(collector.books_genre) == 1

    # Тест проверяет корректную установку РАЗРЕШЁННЫХ жанров для существующей книги
    # Использует параметризацию для проверки нескольких допустимых жанров в одном тесте
    @pytest.mark.parametrize('valid_genre', ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии'])
    def test_set_book_genre_valid_genre(self, valid_genre):
        collector = BooksCollector()
        book_name = 'Преступление и наказание'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, valid_genre)
        assert collector.get_book_genre(book_name) == valid_genre

    # тест: установка жанра для несуществующей книги
    # проверяет, что нельзя установить жанр для книги, которой нет в коллекции
    def test_set_book_genre_nonexistent_book(self):
        collector = BooksCollector()
        collector.set_book_genre('Неизвестная книга', 'Фантастика')
        assert 'Неизвестная книга' not in collector.books_genre

    # тест: установка недопустимого жанра
    # проверяет, что жанр не устанавливается, если его нет в списке доступных жанров (genre)
    def test_set_book_genre_invalid_genre(self):
        collector = BooksCollector()
        book_name = 'Война и мир'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, 'Поэзия')
        assert collector.get_book_genre(book_name) == ''

    # тест: получение жанра существующей книги
    # проверяет корректность работы метода get_book_genre для книги с установленным жанром
    def test_get_book_genre_existing_book(self):
        collector = BooksCollector()
        book_name = 'Дюна'
        genre = 'Фантастика'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == genre

    # тест: запрос жанра для несуществующей книги
    # проверяет, что метод get_book_genre возвращает None для книги, отсутствующей в коллекции
    def test_get_book_genre_nonexistent_book(self):
        collector = BooksCollector()
        assert collector.get_book_genre('Выдуманная книга') is None

    # тест: получение книг по существующему жанру
    # проверяет работу метода get_books_with_specific_genre — возвращает список книг заданного жанра
    def test_get_books_with_specific_genre_existing(self):
        collector = BooksCollector()
        collector.add_new_book('Оно')
        collector.add_new_book('Сияние')
        collector.set_book_genre('Оно', 'Ужасы')
        collector.set_book_genre('Сияние', 'Ужасы')
        result = collector.get_books_with_specific_genre('Ужасы')
        assert result == ['Оно', 'Сияние']

    # тест: запрос книг по несуществующему жанру
    # проверяет, что метод возвращает пустой список, если жанр отсутствует в списке доступных
    def test_get_books_with_specific_genre_nonexistent(self):
        collector = BooksCollector()
        result = collector.get_books_with_specific_genre('Поэзия')
        assert result == []

    # тест: фильтрация книг для детей
    # проверяет метод get_books_for_children — возвращает только книги с жанрами без возрастного рейтинга
    def test_get_books_for_children(self):
        collector = BooksCollector()
        collector.add_new_book('Молчание ягнят')
        collector.set_book_genre('Молчание ягнят', 'Детективы')
        collector.add_new_book('Король Лев')
        collector.set_book_genre('Король Лев', 'Мультфильмы')
        collector.add_new_book('Один дома')
        collector.set_book_genre('Один дома', 'Комедии')
        result = collector.get_books_for_children()
        assert 'Молчание ягнят' not in result
        assert 'Король Лев' in result
        assert 'Один дома' in result

    # тест: попытка добавления в избранное книги, не добавленной в коллекцию
    # проверяет, что нельзя добавить в избранное книгу, отсутствующую в словаре books_genre
    def test_add_book_in_favorites_nonexistent_book(self):
        collector = BooksCollector()
        book_name = 'Неизвестная книга'
        collector.add_book_in_favorites(book_name)
        assert book_name not in collector.favorites

    # тест: получение списка избранного
    # проверяет корректность работы метода get_list_of_favorites_books
    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        favorite_books = ['Властелин колец', 'Хоббит']
        for book in favorite_books:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)
        result = collector.get_list_of_favorites_books()
        assert result == favorite_books
        
    # Тест проверяет корректность работы метода get_books_genre() класса BooksCollector.
    # Убеждается, что метод возвращает словарь с книгами и их жанрами в соответствии с установленными значениями.
    def test_get_books_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Фантастика')
        collector.add_new_book('Убийство в Восточном экспрессе')
        collector.set_book_genre('Убийство в Восточном экспрессе', 'Детективы')

        result = collector.get_books_genre()
        expected = {'Дюна': 'Фантастика', 'Убийство в Восточном экспрессе': 'Детективы'}
        assert result == expected

    # Тест проверяет корректность добавления книги в список избранного (favorites)
    # через метод add_book_in_favorites() для книги, которая уже есть в коллекции.
    def test_add_book_in_favorites_existing_book(self):
        collector = BooksCollector()
        book_name = 'Гарри Поттер'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert book_name in collector.favorites
    
    # Тест проверяет корректность добавления книги в список избранного (favorites)
    # через метод add_book_in_favorites() после предварительного добавления книги в коллекцию.
    def test_add_book_to_favorites(self):
        collector = BooksCollector()
        book_name = 'Гарри Поттер'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert book_name in collector.favorites


    # Тест проверяет корректность удаления книги из списка избранного (favorites)
    # через метод delete_book_from_favorites() после добавления книги в избранное.
    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        book_name = 'Гарри Поттер'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        assert book_name not in collector.favorites   

    # Негативная проверка: книги с наименованием 0 или длиннее 40 символов — не добавляются
    @pytest.mark.parametrize('invalid_book_name',
        ['',
         'A' * 50
        ])
    def test_add_new_book_invalid_name(self, invalid_book_name):
        collector = BooksCollector()
        collector.add_new_book(invalid_book_name)
        assert invalid_book_name not in collector.get_books_genre()
        
    # Позитивная проверка: книги с наименованием от 1 до 40 символов — успешно добавляются
    @pytest.mark.parametrize('valid_book_name', [
        'A',  # минимальная длина — 1 символ
        'Война и мир',  # обычное название
        'A' * 40  # максимальная длина — ровно 40 символов
        ])
    def test_add_new_book_valid_name(self, valid_book_name):
        collector = BooksCollector()
        collector.add_new_book(valid_book_name)
        assert valid_book_name in collector.get_books_genre()

from django.core.management import BaseCommand

from reviews.models import (User, Title, Category, Comment, Genre, GenreTitle,
                            Review)
from .load_data import (
    load_data_users,
    load_data_category,
    load_data_genre,
    load_data_title,
    load_data_genre_title,
    load_data_review,
    load_data_comment
)


ALREDY_LOADED_ERROR_MESSAGE = """
Если вам нужно перезагрузить дочерние данные из CSV-файла,
сначала удалите файл db.sqlite3, чтобы уничтожить базу данных.
Затем запустите `python manage.py миграция` для новой пустой
базы данных с таблицами"""
DB_TABLES = [User, Title, Category, Comment, Genre, GenreTitle, Review]


class Command(BaseCommand):
    help = "Загрузка данных из директории Static"

    def handle(self, *args, **options,):
        for table in DB_TABLES:
            if table.objects.exists():
                print('В базе уже есть данные.')
                print(ALREDY_LOADED_ERROR_MESSAGE)
                return

        print("Загрузка данных:")
        try:
            load_data_users()
            print('Загрузка данных пользователей окончена.')
            load_data_category()
            print('Загрузка данных категорий окончена.')
            load_data_genre()
            print('Загрузка данных жанров окончена.')
            load_data_title()
            print('Загрузка данных произведений окончена.')
            load_data_genre_title()
            print('Загрузка данных жанр-произведение окончена.')
            load_data_review()
            print('Загрузка данных откликов окончена.')
            load_data_comment()
            print('Загрузка данных комментариев окончена.')
        except ValueError:
            print('Неопределенное значение.')
        except Exception:
            print('Что-то пошло не так!')
        else:
            print('Загрузка окончена.')

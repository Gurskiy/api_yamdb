from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import (User, Title, Category, Comment, Genre, GenreTitle,
                            Review)


ALREDY_LOADED_ERROR_MESSAGE = """
Если вам нужно перезагрузить дочерние данные из CSV-файла,
сначала удалите файл db.sqlite3, чтобы уничтожить базу данных.
Затем запустите `python manage.py миграция` для новой пустой
базы данных с таблицами"""


class Command(BaseCommand):
    help = "Загрузка данных из директории Static"

    def handle(self, *args, **options,):

        if (User.objects.exists() or Title.objects.exists()
                or Category.objects.exists() or Comment.objects.exists()
                or Genre.objects.exists() or GenreTitle.objects.exists()
                or Review.objects.exists()):
            print('В базе уже есть данные.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Загрузка данных")
        try:
            for row in DictReader(open('./static/data/users.csv',
                                       encoding='utf-8')):
                child = User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                )
                child.save()
            for row in DictReader(open('./static/data/category.csv',
                                       encoding='utf-8')):
                child = Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
                child.save()
            for row in DictReader(open('./static/data/genre.csv',
                                       encoding='utf-8')):
                child = Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
                child.save()
            for row in DictReader(open('./static/data/titles.csv',
                                       encoding='utf-8')):
                child = Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(pk=row['category']),
                )
                child.save()
            for row in DictReader(open('./static/data/genre_title.csv',
                                       encoding='utf-8')):
                child = GenreTitle(
                    id=row['id'],
                    title=Title.objects.get(pk=row['title_id']),
                    genre=Genre.objects.get(pk=row['genre_id']),
                )
                child.save()
            for row in DictReader(open('./static/data/review.csv',
                                       encoding='utf-8')):
                child = Review(
                    id=row['id'],
                    title=Title.objects.get(pk=row['title_id']),
                    text=row['text'],
                    author=User.objects.get(pk=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
                child.save()
            for row in DictReader(open('./static/data/comments.csv',
                                       encoding='utf-8')):
                child = Comment(
                    id=row['id'],
                    review=Review.objects.get(pk=row['review_id']),
                    text=row['text'],
                    author=User.objects.get(pk=row['author']),
                    pub_date=row['pub_date'],
                )
                child.save()
        except ValueError:
            print('Неопределенное значение.')
        except Exception:
            print('Что-то пошло не так!')
        else:
            print('Загрузка окончена.')

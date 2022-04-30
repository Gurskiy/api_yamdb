from csv import DictReader

from reviews.models import (User, Category, Genre, Title, GenreTitle, Review,
                            Comment)


def load_data_users():
    for row in DictReader(
            open('./static/data/users.csv', encoding='utf-8')
    ):
        child = User(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            role=row['role'],
            bio=row['bio'],
        )
        child.save()


def load_data_category():
    for row in DictReader(
            open('./static/data/category.csv', encoding='utf-8')
    ):
        child = Category(
            id=row['id'],
            name=row['name'],
            slug=row['slug'],
        )
        child.save()


def load_data_genre():
    for row in DictReader(
            open('./static/data/genre.csv', encoding='utf-8')
    ):
        child = Genre(
            id=row['id'],
            name=row['name'],
            slug=row['slug'],
        )
        child.save()


def load_data_title():
    for row in DictReader(
            open('./static/data/titles.csv', encoding='utf-8')
    ):
        child = Title(
            id=row['id'],
            name=row['name'],
            year=row['year'],
            category=Category.objects.get(pk=row['category']),
        )
        child.save()


def load_data_genre_title():
    for row in DictReader(
            open('./static/data/genre_title.csv', encoding='utf-8')
    ):
        child = GenreTitle(
            id=row['id'],
            title=Title.objects.get(pk=row['title_id']),
            genre=Genre.objects.get(pk=row['genre_id']),
        )
        child.save()


def load_data_review():
    for row in DictReader(
            open('./static/data/review.csv', encoding='utf-8')
    ):
        child = Review(
            id=row['id'],
            title=Title.objects.get(pk=row['title_id']),
            text=row['text'],
            author=User.objects.get(pk=row['author']),
            score=row['score'],
            pub_date=row['pub_date'],
        )
        child.save()


def load_data_comment():
    for row in DictReader(
            open('./static/data/comments.csv', encoding='utf-8')
    ):
        child = Comment(
            id=row['id'],
            review=Review.objects.get(pk=row['review_id']),
            text=row['text'],
            author=User.objects.get(pk=row['author']),
            pub_date=row['pub_date'],
        )
        child.save()

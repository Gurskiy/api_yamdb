### Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title). 
Произведения делятся на категории: "Книги", "Фильмы", "Музыка". 
Список категорий (Category) может быть расширен.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или 
послушать музыку. В каждой категории есть произведения: книги, фильмы или 
музыка. Например, в категории "Книги" могут быть произведения 
"Винни Пух и все-все-все" и "Марсианские хроники", а в категории 
"Музыка" — песня "Давеча" группы "Насекомые" и вторая сюита Баха. 
Произведению может быть присвоен жанр из списка предустановленных 
(например, "Сказка", "Рок" или "Артхаус"). Новые жанры может создавать 
только администратор. Благодарные или возмущённые читатели оставляют к 
произведениям текстовые отзывы (Review) и выставляют произведению рейтинг.
### Технологии
Python 3.8
Django 2.2.19
### # Установка
- Установите и активируйте виртуальное окружение
```
python3 -m venv env
```
```
source env/bin/activate
```
```
python3 -m pip install --upgrade pip
```
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- В папке с файлом manage.py выполните команду:
```
\api_yamdb\api_yamdb\manage.py
```
- Выполнить migrate
```
python manage.py migrate
```
- Для загрузки данных (опционально)
```
python manage.py load_data_to_db
```
- Создайте пользователя
```
python manage.py createsuperuser
```
- (или) Сменить пароль для пользователя admin
```
python manage.py changepassword admin
```
- Запуск сервиса
```
python manage.py runserver
```
# API ресурсы:
- **AUTH**: Аутентификация.
- **USERS**: Пользователи.
- **TITLES**: Произведения, к которым пишут отзывы.
- **CATEGORIES**: Категория произведений ("Фильмы", "Книги", "Музыка").
- **GENRES**: Жанры, одно из произведений может быть присвоено к нескольким жанрам.
- **REVIEWS**: Отзывы на произведения.
- **COMMENTS**: Комментарии к отзывам.

# Алгоритм регистрации пользователей
Пользователь отправляет POST-запрос с параметром email и username на `/api/v1/auth/signup`.
YaMDB отправляет письмо с кодом подтверждения (confirm_code) на адрес email (эмуляция почтовго сервера).
Пользователь отправляет POST-запрос с параметрами email и confirmation_code на `/api/v1/auth/token/`, 
в ответе на запрос ему приходит token.
Эти операции выполняются один раз, при регистрации пользователя. 
В результате пользователь получает токен и каждый раз отправяет его при запросе.

# Пользовательские роли
- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь (user)** — может читать всё, как и Аноним, дополнительно может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии.
- **Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя плюс право удалять и редактировать любые отзывы и комментарии.
- **Администратор (admin)** — полные права на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- **Супер юзер** — те же права, что и у роли Администратор.

### Авторы
Егор Бабенко, Николай Егорченков, Павел Гурский

### License
MIT

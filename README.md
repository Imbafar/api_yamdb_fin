# Описание

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles).
    Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
    Список категорий (Category) может быть расширен администратором
(например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
    Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
    В каждой категории есть произведения: книги, фильмы или музыка.
    Произведению может быть присвоен жанр (Genre) из списка предустановленных
(например, «Сказка», «Рок» или «Артхаус»).
    Новые жанры может создавать только администратор.
    Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы
(Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число);
из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число).
    На одно произведение пользователь может оставить только один отзыв.

# Установка

1. Клонировать репозиторий и перейти в него в командной строке:
```
git clone 'https://github.com/NikitaChalykh/api_yamdb.git'
```
```
cd api_yamdb
```
2. Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source env/bin/activate
```
3. Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
4. Выполнить миграции:
```
python3 manage.py makemigrations
```
```
python3 manage.py migrate
```
5. Запустить проект:
```
python3 manage.py runserver
```

# Документация

Документация для API YaMDb доступна по адресу:
```
"http://127.0.0.1:8000/redoc/"
```

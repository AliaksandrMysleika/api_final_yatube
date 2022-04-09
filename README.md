# Yatube API
### Цель проекта Yatube API:
Создание API сервиса для авторского блогинга с возможностью создавать посты, комментировать посты, создавать тематические группы, подписываться на понравившихся авторов.


### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/AliaksandrMysleika/api_final_yatube.git
```
```
cd api_final_yatube
```
Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```
```
source env/bin/activate
```
Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:

```
python3 manage.py migrate
```
Запустить проект:

```
python3 manage.py runserver
```

### Примеры запросов:
Тип запроса|Адрес|Исходящие данные|Ответ
-----------|-----|----------------|-----
GET|```http://127.0.0.1:8000/api/v1/posts/```|*________*|[{"id":1,"author":"Fedor","text":"Hi all! Who is from Russia?","pub_date":"2021-07-23T16:18:28.221740Z","image":null,"group":null},{"id":2,"author":"Aliaksandr","text":"Hello world! Who gonna visit Europe this summer?","pub_date":"2021-07-23T16:19:43.542882Z","image":null,"group":null},]
POST|```http://127.0.0.1:8000/api/v1/posts/```|{"text": "Hello world!"}|{"id":21,"author":"Fedor","text":"Hello world!","pub_date":"2021-07-24T21:42:23.363226Z","image":null,"group":null}
GET|```http://127.0.0.1:8000/api/v1/posts/5/comments/```|*________*|[{"id":1,"author":"Aliaksandr","text":"Yo, man, awesome place! Is it Sabaudia beach on last photo?","created":"2021-07-23T16:29:25.038881Z","post":5},{"id":2,"author":"Fedor","text":"Yes, you're right!)","created":"2021-07-23T16:57:35.219288Z","post":5}]
POST|```http://127.0.0.1:8000/api/v1/posts/5/comments/```|{"text": "I'll visit this beach next year!"}|{"id":3,"author":"John","text":"I'll visit this beach next year!","created":"2021-07-24T21:56:03.166573Z","post":5}
POST|```http://127.0.0.1:8000/api/v1/follow/```|{"following": "Fedor"}|[{"id":4,"user":"John","following":"Fedor"}]

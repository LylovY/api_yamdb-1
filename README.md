# Api для проекта Yamdb

![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)
![](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=Swagger&logoColor=white)
![](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white)


Yamdb - проект, собирающий отзывы пользователей на произведения. Сами произведения в Yamdb не хранятся. Yamdb поддерживает следующий функционал:

- Публикование отзывов
- Комментирование отзывов
- Регистрация пользователей
- Изменение пользователями своих профилей, отзывов и комментариев

## Пользовательские роли

- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django обладает всеми правами администратора

Api предоставляет полноценный доступ к функционалу Yatube

## Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AlexanderZug/api_yamdb.git
```

```
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:


```
python3 -m venv env

source env/bin/activate

python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

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



## Примеры

http://127.0.0.1:8000/api/v1/users/

GET
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
```

POST
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```


http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/

GET
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2022-08-14T14:15:22Z"
      }
    ]
  }
]
```

POST
```
{
  "text": "string",
  "score": 1
}
```

http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/

GET
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2022-08-14T14:15:22Z"
      }
    ]
  }
]
```

POST
```
{
  "text": "string"
}
```

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/-SQLite-464646?style=flat-square&logo=SQLite)](https://www.sqlite.org/)
[![html](https://img.shields.io/badge/-html-464646?style=flat-square&logo=html)](https://www.w3.org/html/)
[![css](https://img.shields.io/badge/-css-464646?style=flat-square&logo=css)](https://www.w3.org/Style/CSS/)

# Социальная сеть для публикаций постов SocialNetwork

---
## Описание проекта

Это проект социальной сети, её название - SocialNetwork
Как и любая социальная сеть она много, что умеет. Вы можете размещать информацию о себе, своих интересах/хобби,
или просто делиться своими мыслями/чувствами/переживаниями/идеями.
Публикуйте свои посты, пишите тексты, делитесь фотографиями, комментируйте другие посты, подписывайтесь на интересующих вас авторов,
выбирайте в приоритетах интересующие вас группы, делайте что хотите, и что вам нравится!

---
## Технологии
* Python 3.9
* Django 2.2.16
* HTML & CSS
* СУБД SQLite

---
## Установка и запуск

Для MacOs и Linux вместо python использовать python3

**1. Клонировать репозиторий:**
```
git clone https://github.com/KazikovAP/hw05_final.git
```

**2. Перейти в папку проекта:**
```
cd /hw05_final/
```

**3. Cоздать и активировать виртуальное окружение:**
```
python -m venv venv
```

Для Windows:
```
source venv/Scripts/activate
```

Для MacOs/Linux:
```
source venv/bin/activate
```

**4. Установить зависимости из файла requirements.txt:**
- Обновить пакетный менеджер pip
```
python -m pip install --upgrade pip
```

- Установить зависимости
```
pip install -r requirements.txt
```

**5. Создать и запустить миграции:**
- Перейти в папку yatube
```
cd /yatube/
```

- Создать миграции
```
python manage.py makemigrations
```

- Применить миграции
```
python manage.py migrate
```

**6. Запустить сервер:**
```
python manage.py runserver
```

> После выполнения вышеперечисленных инструкций проект доступен по адресу http://127.0.0.1:8000/

---
## Разработал:
[Aleksey Kazikov](https://github.com/KazikovAP)

---
## Лицензия:
[MIT](https://opensource.org/licenses/MIT)


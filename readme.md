# TeamFinder

TeamFinder — веб-приложение для поиска единомышленников и формирования команд для совместной разработки проектов.

Пользователи могут создавать проекты, просматривать профили других участников, присоединяться к интересующим проектам, добавлять проекты в избранное и управлять собственным профилем.

## Основные возможности

* регистрация и авторизация пользователей по email;
* создание и редактирование проектов;
* просмотр списка проектов с пагинацией;
* просмотр профилей пользователей;
* редактирование профиля пользователя;
* автоматическая генерация аватара при регистрации;
* участие в проектах;
* добавление проектов в избранное;
* просмотр списка избранных проектов;
* смена пароля;
* административная панель Django;
* фильтрация пользователей в соответствии с требованиями варианта №1.

---

## Технологии

### Backend

* Python 3.10
* Django 5
* PostgreSQL
* Pillow

### Инфраструктура

* Docker
* Docker Compose

---

## Запуск проекта

### 1. Клонирование репозитория

```bash
git clone https://github.com/Lexor19/team-finder-ad.git
cd team-finder
```

### 2. Создание файла окружения

Создайте файл `.env` в корне проекта.

Пример содержимого:

```env
SECRET_KEY=your_secret_key

DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=team_finder
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

---

### 3. Запуск PostgreSQL

Запустите контейнер с базой данных:

```bash
docker compose up -d
```

Проверить состояние контейнеров:

```bash
docker ps
```

Остановить контейнеры:

```bash
docker compose down
```

---

### 4. Установка зависимостей

Создайте виртуальное окружение:

```bash
python -m venv venv
```

Активируйте его.

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

---

### 5. Выполнение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Создание администратора

```bash
python manage.py createsuperuser
```

---

### 7. Запуск проекта

```bash
python manage.py runserver
```

После запуска приложение будет доступно по адресу:

```text
http://127.0.0.1:8000/
```

### Автор
Мануковский Александр
Почта: Lexorrr@yandex.ru
---

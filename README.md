# Foodgram
Foodgram - готовый к деплою сайт по добавлению рецептов.

## Стек
 - python 3.11
 - django 3.2
 - djangorestframework 3.12.4
 - react
 - nginx 1.19.3

## Установка
Настройка окружения
```bash
git clone https://github.com/donartemiy/foodgram-project-react.git

# Backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Заполнить переменные окружения по аналогии с файлом .env_example, переименовать файл
vi .env_exmaple
mv .env_exmaple .env

cd backend/foodgram
python manage.py migrate
python manage.py createsuperuser
```

## Запуск проекта
```bash
# Frontend&nginx
cd infra
docker compose up --build

# Запуск backend
cd backend/foodgram
python manage.py runserver
```

# Доступные страницы
- Документация доступна по адресу:
http://127.0.0.1/api/docs/
- Сайт доступен по адресу:
http://127.0.0.1/
- Админка сайта:
http://127.0.0.1/admin/

# Автор
- donartemiy

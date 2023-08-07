# Foodgram
Foodgram - готовый к деплою сайт по добавлению рецептов.

## Стек
 - python 3.11
 - django 3.2
 - djangorestframework 3.12.4
 - react
 - nginx 1.19.3

## Локальная установка без БД
### Настройка окружения
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

### Запуск проекта
```bash
# Frontend&nginx
cd infra
docker compose up --build

# Запуск backend
cd backend/foodgram
python manage.py runserver
```

## Delpoy на сервер
### Проект состоит из четырех контейнеров
1. backend
- python 3.9
- django 3.2.3
- gunicorn 20.1.0
2. frontend
- react
3. gateway
- nginx 1.22.1
4. db
- postgres 13

## Как развернуть проект Foodgram
1. Требуется docker v3
2. Из корня репозитория скачать: 2.1. Файл "docker-compose.production.yml" 2.2. Файл ".env.example"
3. Переименовать .env.example в .env
4. Рекомендуется указать собственные значения для переменных
5. Собрать контейнеры и запуститть

```
sudo docker compose -f docker-compose.production.yml up -d
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```
6. Доступ к сайту предоставляется через порт 8080.

## Загрузка готовых данных в БД
```
sudo docker compose -f docker-compose.production.yml ps
sudo docker exec -it foodgram-backend-1 bash
python manage.py loaddata data/ingredient.json
```

# Доступные страницы
- Документация доступна по адресу:
http://127.0.0.1/api/docs/
- Сайт доступен по адресу:
http://127.0.0.1/
- Админка сайта:
http://127.0.0.1/admin/

## Данные для ревьюера
"username": "Alex",
"password": "Al12345678",
"email": "alex@mail.ru"

https://premiumsite.ddns.net/
https://premiumsite.ddns.net/admin/
158.160.7.157

# Автор
- donartemiy

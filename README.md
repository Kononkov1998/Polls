# Polls - API для системы опросов пользователей
Для запуска необходим Docker.

Процесс запуска:
1. С помощью командной строки открыть папку с проектом
2. Выполнить команду "docker-compose up -d"
3. Выполнить команду "docker exec -it polling_back_1 python manage.py migrate"

Создать администратора можно командой "docker exec -it polling_back_1 python manage.py createsuperuser".

Создать рядового пользователя можно в панели администратора.


Адрес API: http://localhost:8000/

Документация: http://localhost:8000/api/

Панель администратора: http://localhost:8000/admin/ 

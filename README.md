
проект доступен
[http://dima699699.pythonanywhere.com/admin/](http://dima699699.pythonanywhere.com/admin/)

<br>
Доступ:
Phone number: +7123456789
Password: 1234 

дока:

[http://dima699699.pythonanywhere.com/redoc/](http://dima699699.pythonanywhere.com/redoc/)

[http://dima699699.pythonanywhere.com/swagger/](http://dima699699.pythonanywhere.com/swagger/)

<details>
<summary>
Запуск в docker
</summary>
Коллекция в posman  local_host.postman_collection

```bash
    git clone git@github.com:Not-user-1984/referral_system.git
    cd dev
    docker compose up -d --build
    docker exec -it backend python manage.py migrate
    docker exec -it backend python manage.py createsuperuser 
```
</details>

<br>

Cделано через кастом модели users django,
можно посмотреть всех пользователей и их ивайты через админку.

Создавать через posman.

Импорт коллекции в папке posman
файл dev_host.postman_collection

``` bash
post-запрос
http://dima699699.pythonanywhere.com/users/api/request_phone_number/   ввод телефона и получение кода.
запрос json
{
    "phone_number": "Номер начинаться должен  +7 и 11 цифр"
}


post-запрос
http://dima699699.pythonanywhere.com/users/api/request_phone_number/  активация и получение токена
запрос json
{
    "phone_number": "+7234567970",
    "code": "2057"
}


post-запрос
http://dima699699.pythonanywhere.com/users/api/activate_invite_code/ активация чужого ивайта
(что активировать надо  Headers ввести раний полученый токен)
запрос json
{
    "invite_code": "10JPKp"
}


get-запрос
http://dima699699.pythonanywhere.com/users/api/invited-users/
(в Headers ввести раний полученый токен)
ответ json
[
    {
        "phone_number": "+7234567979"
    },
    {
        "phone_number": "+7234567976"
    },
    {
        "phone_number": "+7234567972"
    }
]

get-запрос
http://dima699699.pythonanywhere.com/users/api/user_profile/
(в Headers ввести раний полученый токен)
профиль пользователя
ответ json
{
    "phone_number": "+7234567970",
    "invite_code": "85NZtH",
    "activated_invite_code": null
}

```

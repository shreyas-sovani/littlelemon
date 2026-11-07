Little Lemon restaurant API
Back-end developer capstone project

Run the project
1. python -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. Create the MySQL database: CREATE DATABASE littlelemon;
5. Set DB_USER and DB_PASSWORD if they are not root with an empty password.
6. python manage.py migrate
7. python manage.py runserver
8. Open http://127.0.0.1:8000

The site is served by Django templates and static files:
/
/about/
/menu/
/book/
/bookings/

API paths
/api/menu/
/api/menu/<id>/
/api/bookings/
/api/bookings/<id>/
/api/registration/
/api/token/login/
/auth/users/
/auth/token/login/

Test these paths in Insomnia. Use a JSON body and the header Content-Type: application/json.

1. Register a user
POST http://127.0.0.1:8000/api/registration/
{
  "username": "guest",
  "password": "LittleLemon#2026",
  "email": "guest@littlelemon.com"
}

The response contains auth_token. The same user can also be created with POST /auth/users/.

2. Log in and get a token
POST http://127.0.0.1:8000/api/token/login/
{
  "username": "guest",
  "password": "LittleLemon#2026"
}

Djoser login is the same body at POST /auth/token/login/.
Copy auth_token from the response.

3. Send the token on booking requests
Header: Authorization: Token <auth_token>

4. Menu API, open to GET, POST, PUT, and DELETE
GET http://127.0.0.1:8000/api/menu/
POST http://127.0.0.1:8000/api/menu/
{
  "name": "Greek Salad",
  "price": 12,
  "menu_item_description": "Fresh salad with feta and olives"
}
GET http://127.0.0.1:8000/api/menu/1/
PUT http://127.0.0.1:8000/api/menu/1/
DELETE http://127.0.0.1:8000/api/menu/1/

5. Table booking API, token required for every method
GET http://127.0.0.1:8000/api/bookings/
POST http://127.0.0.1:8000/api/bookings/
{
  "first_name": "Ada",
  "reservation_date": "2026-11-08",
  "reservation_slot": 18
}
GET http://127.0.0.1:8000/api/bookings/1/
PUT http://127.0.0.1:8000/api/bookings/1/
DELETE http://127.0.0.1:8000/api/bookings/1/

A GET to /api/bookings/ without the Authorization header returns 401.

MySQL
The default database engine is django.db.backends.mysql, database name littlelemon, host 127.0.0.1, port 3306.
Set DB_ENGINE=sqlite only if MySQL is not installed. python manage.py test uses that when you run:
DB_ENGINE=sqlite python manage.py test

Unit tests
DB_ENGINE=sqlite python manage.py test

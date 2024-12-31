# SIMPLE CRUD API WITH DJANGO REST FRAMEWORK
[Django REST framework](http://www.django-rest-framework.org/) is a powerful and flexible toolkit for building Web APIs.

## Requirements
- Python 3.9
- Django 5.1.4
- Django REST Framework

## Installation
After you cloned the repository, you want to create a virtual environment, so you have a clean python installation.
You can do this by running the command
```
python -m venv env
```

After this, it is necessary to activate the virtual environment, you can get more information about this [here](https://docs.python.org/3/tutorial/venv.html)

You can install all the required dependencies by running
```
pip install -r requirements.txt
```

## Structure
In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods - GET, POST, PATCH, DELETE. Endpoints should be logically organized around _collections_ and _elements_, both of which are resources.

In our case, we have one single resource, `products`, so we will use the following URLS - `/products/` and `/products/<id>` for collections and elements, respectively:

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`products` | GET | READ | Get all products
`products/:id` | GET | READ | Get a single product
`products`| POST | CREATE | Create a new product
`products/:id` | PATCH | UPDATE | Update a product
`products/:id` | DELETE | DELETE | Delete a product

## Use
First, we have to start up Django's development server.
```
python manage.py runserver
```
Only authenticated users can use the API services, for that reason if we try this:
```
http  http://127.0.0.1:8000/api/v1/products/
```
we get:
```
{
    "detail": "Authentication credentials were not provided."
}
```
Instead, if we try to access with credentials:
```
http http://127.0.0.1:8000/api/v1/products/3 "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE2MjA4Mjk1LCJqdGkiOiI4NGNhZmMzMmFiZDA0MDQ2YjZhMzFhZjJjMmRiNjUyYyIsInVzZXJfaWQiOjJ9.NJrs-sXnghAwcMsIWyCvE2RuGcQ3Hiu5p3vBmLkHSvM"
```
we get the product with id = 3
```
{
  "id": 4, "name": "The product", "quantity": 3, "owner": "test@gmail.com", "total_price": "3456.00", "created_at": "2024-12-31T17:00:01.630647+03:30", "updated_at": "2024-12-31T17:00:01.630670+03:30"
}
```

## Create users and Tokens

First we need to create a user, so we can receive a token
```
http POST http://127.0.0.1:8000/api/v1/auth/authentication/ email="email@email.com" password1="PASSWORD"
```
after that, we get the token
```
{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNjI5MjMyMSwianRpIjoiNGNkODA3YTlkMmMxNDA2NWFhMzNhYzMxOTgyMzhkZTgiLCJ1c2VyX2lkIjozfQ.hP1wPOPvaPo2DYTC9M1AuOSogdRL_mGP30CHsbpf4zA",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE2MjA2MjIxLCJqdGkiOiJjNTNlNThmYjE4N2Q0YWY2YTE5MGNiMzhlNjU5ZmI0NSIsInVzZXJfaWQiOjN9.Csz-SgXoItUbT3RgB3zXhjA2DAv77hpYjqlgEMNAHps"
}
```
We got two tokens, the access token will be used to authenticated all the requests we need to make, this access token will expire after some time.
We can use the refresh token to request a need access token.

requesting new access token
```
http http://127.0.0.1:8000/api/v1/auth/token/refresh/ refresh_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNjI5MjMyMSwianRpIjoiNGNkODA3YTlkMmMxNDA2NWFhMzNhYzMxOTgyMzhkZTgiLCJ1c2VyX2lkIjozfQ.hP1wPOPvaPo2DYTC9M1AuOSogdRL_mGP30CHsbpf4zA"
```
and we will get a new access token
```
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE2MjA4Mjk1LCJqdGkiOiI4NGNhZmMzMmFiZDA0MDQ2YjZhMzFhZjJjMmRiNjUyYyIsInVzZXJfaWQiOjJ9.NJrs-sXnghAwcMsIWyCvE2RuGcQ3Hiu5p3vBmLkHSvM"
}
```


The API has some restrictions:
-   The products are always associated with a creator (user who created it).
-   Only authenticated users may create and see their products.
-   Only the owner of a product or manager may update or delete it.
-   The API doesn't allow unauthenticated requests.

### Commands
```
Get all products
http http://127.0.0.1:8000/api/v1/products/ "Authorization: Bearer {YOUR_TOKEN}" 
Get a single product
http GET http://127.0.0.1:8000/api/v1/products/{product_id}/ "Authorization: Bearer {YOUR_TOKEN}" 
Create a new product
http POST http://127.0.0.1:8000/api/v1/products/ "Authorization: Bearer {YOUR_TOKEN}"
Full update a product
http PUT http://127.0.0.1:8000/api/v1/products/{product_id}/ "Authorization: Bearer {YOUR_TOKEN}"
Partial update a product
http PATCH http://127.0.0.1:8000/api/v1/products/{product_id}/ "Authorization: Bearer {YOUR_TOKEN}"
Delete a product
http DELETE http://127.0.0.1:8000/api/v1/products/{product_id}/ "Authorization: Bearer {YOUR_TOKEN}"
```

### Pagination
The API supports pagination, by default responses have a page_size=20 but if you want change that you can pass through params page_size={your_page_size_number}
```
http http://127.0.0.1:8000/api/v1/products/?page=1 "Authorization: Bearer {YOUR_TOKEN}"
http http://127.0.0.1:8000/api/v1/products/?page=3 "Authorization: Bearer {YOUR_TOKEN}"
http http://127.0.0.1:8000/api/v1/products/?page=3&page_size=15 "Authorization: Bearer {YOUR_TOKEN}"
```

### Filters
The API supports filtering, you can filter by the attributes of a product like this
```
http http://127.0.0.1:8000/api/v1/products/?created_at__gt=2019&created_at__lt=2022 "Authorization: Bearer {YOUR_TOKEN}"
http http://127.0.0.1:8000/api/v1/products/?total_price__gte=2000&total_price__lte=3000 "Authorization: Bearer {YOUR_TOKEN}"
```

## Running Tests and Checking Coverage

### Running Tests
To ensure that your application is working correctly, you can run the test suite using Django's built-in testing framework. Use the following command:

```bash
python manage.py test
```

### Getting coverage
To measure the test coverage of your code, you can use the coverage.py tool. Generate an HTML coverage report for a detailed view:

```bash
coverage html
```



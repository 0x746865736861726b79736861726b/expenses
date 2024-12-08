# Expenses test app

## How to start
Clone this repo:

    $ git clone git@github.com:0x746865736861726b79736861726b/expenses.git
    $ cd expenses/

Build containers:

    $ docker-compose.yml build --no-cache

Run migrations:

    $ docker-compose.yml run web poetry run apps/manage.py migrate

Run unittests:

    $ docker-compose.yml run web poetry run apps/manage.py tests expenses
    $ docker-compose.yml run web petry run apps/manage.py tests users

For using seeded data for database entityes you can use:

    docker-compose run web poetry run python apps/manage.py loaddata apps/users/fixtures/users.json
    docker-compose run web poetry run python apps/manage.py loaddata apps/expenses/fixtures/expenses.json 

If you want mannyaly add superuser and edit some data like add new users

    docker-compose run web poetry run python apps/manage.py createsuperuser

then you can access admin dashboard 0.0.0.0:8000/admin

## Expenses API
#### Swagger 0.0.0.0:8000/docs/
#### Raw API documented here
**You can use raw api or via swagger (/docs/)**

### `GET /api/`
Retrieve a list of all expenses.

#### Description:
This endpoint returns all expenses from the database.

#### Request Example:
```bash
GET /api/

[
  {
    "id": 1,
    "user": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Rent",
    "amount": 1200.00,
    "date": "2024-01-15",
    "category": "Housing"
  },
  {
    "id": 2,
    "user": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Groceries",
    "amount": 150.00,
    "date": "2024-01-20",
    "category": "Food"
  }
]

```
#### Response Example:
```bash
[
  {
    "id": 1,
    "user": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Rent",
    "amount": 1200.00,
    "date": "2024-01-15",
    "category": "Housing"
  },
  {
    "id": 2,
    "user": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Groceries",
    "amount": 150.00,
    "date": "2024-01-20",
    "category": "Food"
  }
]
```
#### Possible Errors:

- 400 Bad Request — Invalid query parameters or filters.
- 500 Internal Server Error — Unexpected error on the server.

### `POST /api/`

Create a new expense.
### Description:

This endpoint allows you to create a new expense.
#### Request Body:
```bash
{
  "user": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Rent",
  "amount": 1200.00,
  "date": "2024-01-15",
  "category": "Housing"
}

```
#### Response Example:

```bash
{
  "id": 1,
  "user": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Rent",
  "amount": 1200.00,
  "date": "2024-01-15",
  "category": "Housing"
}

```
#### Possible Errors:

 - 400 Bad Request — Invalid or missing fields in the request.
 - 422 Unprocessable Entity — Validation errors.

### `GET /api/{id}/`

Retrieve a single expense by its ID.
### Description:

This endpoint retrieves the details of an expense by its unique ID.
#### Request Example:
```bash
GET /api/23e4567-e89b-12d3-a456-426614174000/
```
#### Response Example:
```bash
{
  "id": 1,
  "user": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Rent",
  "amount": 1200.00,
  "date": "2024-01-15",
  "category": "Housing"
}

```
#### Possible Errors:
 - 404 Not Found — Expense with the given ID does not exist.

### `PUT /api/{id}/`

Update an existing expense by its ID.
### Description:

This endpoint allows you to update an existing expense.
#### Request Body:
```bash
{
  "user": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Updated Rent",
  "amount": 1300.00,
  "date": "2024-01-16",
  "category": "Housing"
}

```
#### Response Body:
```bash
{
  "id": 1,
  "user": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Updated Rent",
  "amount": 1300.00,
  "date": "2024-01-16",
  "category": "Housing"
}

```
#### Possible Errors:

 - 400 Bad Request — Invalid or missing fields in the request.
 - 404 Not Found — Expense with the given ID does not exist.

### `PATCH /api/{id}/`

Partially update an existing expense by its ID.
### Description:

This endpoint allows you to partially update an existing expense (only fields that are provided in the request will be updated).
#### Request Body:
```bash
{
  "amount": 1400.00
}

```
#### Response Body:
```bash
{
  "id": 1,
  "user": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Rent",
  "amount": 1400.00,
  "date": "2024-01-15",
  "category": "Housing"
}

```
#### Possible Errors:

 - 400 Bad Request — Invalid or missing fields in the request.
 - 404 Not Found — Expense with the given ID does not exist.

#### Request Example:

```bash

POST /expenses/summary/
Content-Type: application/json

{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "month": 1
}
```

#### Response Example:
```bash
[
  {
    "category": "Housing",
    "total_amount": 1200.00
  },
  {
    "category": "Food",
    "total_amount": 150.00
  }
]
```
#### Possible Errors:

 - 400 Bad Request — Invalid request parameters or validation errors.
 - 404 Not Found — User or expense category not found.

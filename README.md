# Expenses test app

## How to start
Clone this repo:

    $ git clone git@github.com:0x746865736861726b79736861726b/expenses.git
    $ cd expenses/

Build containers:

    $ docker-compose.yml build --no-cache

Run migrations:

    $ docker-compose.yml run web poetry run apps/manage.py migrate


## Expenses API

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
### `POST /api/filter/`
Filter expenses by `user_id` and date range.

#### Description:
This endpoint allows you to filter expenses based on `user_id`, `start_date`, and `end_date`. You need to provide these parameters in the request, and you will receive a list of expenses that match the criteria.

#### Request Parameters:
- `user_id` (UUID) — required, the user ID to filter expenses.
- `start_date` (Date in `YYYY-MM-DD` format) — required, the start date of the date range.
- `end_date` (Date in `YYYY-MM-DD` format) — required, the end date of the date range.

#### Request Example:
```bash
POST /api/filter/
Content-Type: application/json

{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
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
 - 400 Bad Request — Invalid request parameters or validation errors.
### POST /expenses/summary/

Get the total expenses per category for a user in a given month.
### Description:

This endpoint allows you to get total expenses per category for a specific user in the provided month.
### Request Parameters:

- user_id (UUID) — required, the user ID to calculate the expenses for.
 - month (Integer) — required, the month for which you need the summary (from 1 to 12).

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

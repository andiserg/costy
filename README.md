<p align="center">
      <a href="https://ibb.co/KyLXkwW"><img src="https://i.ibb.co/9YVNLtW/full-logo.png" alt="full-logo" border="0"></a>
</p>

<p align="center">
   <img src="https://img.shields.io/badge/python-3.10-green" alt="Python Version">
   <img src="https://img.shields.io/badge/fastapi-red" alt="Python Version">
   <img src="https://img.shields.io/badge/sqlalchemy-orange" alt="Python Version">
   <img src="https://img.shields.io/badge/docker-blue" alt="Python Version">
</p>

## Про проект

Адаптивний сервіс для класифікації та моніторингу персональних витрат.
Має CRUD операції для керування операціями та категоріями.
Створює персональну статистику витрат, яку можна візуалізувати у діаграмах.
Дозволяє створювати обмеження на витрати по категоріям.
Має можливість синхронізуватись з банками (Monobank) для отримання витрат у реальному часі.

## Про розробку

Проектування проекту відбувалось по принципу DDD та чистої архітектури.
Він поділений на шари бізнес-логіки, доменів, адаптерів та інфраструктури.
За допомогою Dependency Injection вдалось побудувати правильну ієрархію залежностей:
```
Domain <- Uses cases <- adapters <- infrastructure
```
Де стрілками показана залежність шару від іншого.
Тобто, інфраструктура залежить від вищих шарів, адаптери від бізнес логіки та доменів,
бізнес логіка тільки від доменів а домени це незалежні частини програмного продукту.

Розроблявся додаток за принципом TDD, де спочатчку для правильного проектування структур і алгоритмів
розроблялись тести, де формувались вимоги до коду, а потім розроблявся сам код щоб ці вимоги задовольнити.

Для автоматичних тестів та розгортання був застосований GitHub Actions. Для контейнеризації був застосований Docker.


## Документація

### `GET` `/users/` - get current user info

**Headers**
```
Authorization: <token_type> <access_token>
```

**Status codes:**

|  Status Code  |  Description  |
|:-------------:|:-------------:|
|     `200`     |      Ok       |
|     `401`     | Unauthorized  |

**Response:**
```
{
  "id": int,
  "email": string,
}
```
---
### `POST` `/users/` - create user

**Request data:**
```
{
  "email": string,
  "password": string,
}
```

**Status codes:**

| Status Code |    Description    |
|:-----------:|:-----------------:|
|    `201`    |      Created      |
|    `422`    | Validation Error  |

**Response data:**
```
{
  "id": int,
  "email": string,
}
```
---
### `POST` `/token/` - login for access token

**Request data:**
```
{
  "username": string (email),
  "password": string,
}
```

**Status codes:**

| Status Code |   Description    |
|:-----------:|:----------------:|
|    `200`    |        Ok        |
|    `422`    | Validation Error |

**Response data:**
```
{
  "access_token": "string",
  "token_type": "string"
}
```
---
### `POST` `/operations/` - create operation

**Headers**
```
Authorization: <token_type> <access_token>
```

**Request data:**
```
{
  "amount": int,
  "description": "string",
  "source_type": "string",
  "time": int,
  "category_id": int
}
```

**Status codes:**

| Status Code |    Description    |
|:-----------:|:-----------------:|
|    `201`    |      Created      |
|    `422`    | Validation Error  |

**Response data:**
```
{
  "id": int,
  "amount": int,
  "description": "string",
  "source_type": "string",
  "time": int,
  "category_id": int,
  "subcategory_id": int
}
```
---
### `GET` `/operations/` - get list of operations

**Headers**
```
Authorization: <token_type> <access_token>
```

**Request parameters:**
```
from_time: int
to_time: int
```

**Status codes:**

| Status Code |    Description    |
|:-----------:|:-----------------:|
|    `200`    |      Created      |
|    `422`    | Validation Error  |

**Response data:**
```
[
  {
    "amount": int,
    "description": "string",
    "source_type": "string",
    "time": int,
    "category_id": int,
    "id": int,
    "subcategory_id": int
  }
]
```
---
### `GET` `/bankapi/` - get list of connected banks names

**Headers**
```
Authorization: <token_type> <access_token>
```
**Status codes:**

| Status Code | Description |
|:-----------:|:-----------:|
|    `200`    |     Ok      |


**Response data:**
```
[
  "string"
]
```
---
### `DELETE` `/bankapi/` - delete record of connect to bank

**Headers**
```
Authorization: <token_type> <access_token>
```

**Request parameters:**
```
bank_name: string
```

**Status codes:**

| Status Code |   Description    |
|:-----------:|:----------------:|
|    `204`    |    No content    |
|    `422`    | Validation Error |

---
### `GET` `/bankapi/costs/` - update costs by banks API

**Headers**
```
Authorization: <token_type> <access_token>
```

**Status codes:**

| Status Code | Description |
|:-----------:|:-----------:|
|    `200`    |     Ok      |
---
### `GET` `/statistic/` - get statistic

**Headers**
```
Authorization: <token_type> <access_token>
```

**Request parameters:**
```
from_time: int
to_time: int
```

**Status codes:**

| Status Code |    Description    |
|:-----------:|:-----------------:|
|    `200`    |      Created      |

**Response data:**
```
{
  "costs_sum": 0,
  "categories_costs": {},
  "costs_num_by_days": {},
  "costs_sum_by_days": {}
}
```
---
### `POST` `/categories/` - create category

**Headers**
```
Authorization: <token_type> <access_token>
```

**Request data:**
```
{
  "name": "string",
  "icon_name": "string",
  "icon_color": "string"
}
```

**Status codes:**

| Status Code |    Description    |
|:-----------:|:-----------------:|
|    `201`    |      Created      |
|    `422`    | Validation Error  |

**Response data:**
```
{
  "name": "string",
  "id": int,
  "user_id": int,
  "type": "string",
  "icon_name": "string",
  "icon_color": "string",
  "parent_id": int
}
```
---
### `GET` `/categories/` - get list of categories

**Headers**
```
Authorization: <token_type> <access_token>
```

**Status codes:**

| Status Code |   Description    |
|:-----------:|:----------------:|
|    `200`    |        Ok        |

**Response data:**
```
[
  {
    "name": "string",
    "id": int,
    "user_id": int,
    "type": "string",
    "icon_name": "string",
    "icon_color": "string",
    "parent_id": int
  }
]
```

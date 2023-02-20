# Nextjs + FastAPI

FastAPI 認証付き 家計簿 🏠

*全編AsyncSession*


## TODO

- [x] auth
  - [x] AsyncSession での token, JWT authentication 作成
  - [x] AsyncSession Test
  - [x] Depends(get_active_user) 早めに作成

- conftest
  - いい感じのconftest の使い方を考える


## Models

```python
class User:
   username: str
   email: str
   password: str


class Category:
   id: int
   name: str
   user: User


class Household:
   id: int
   amount: int
   registered_at: datatime
   category: Category
   user: User
```


## Relations

```text
User (1)     : (n) Category
User (1)     : (n) Household
Category (1) : (n) Household
```


## Endpoint

- Models
  - [ ] User
  - [ ] Category
  - [ ] Household

- Schemas
  - [ ] User
  - [ ] Category
  - [ ] Household

- Auths
  - [x] POST /token

- Routing
  - users
    - [x] GET   /users
    - [x] GET   /users/:user_id
    - [x] POST  /users
    - [x] PATCH /users
    - [x] DEL   /users

  - categories
    - [x] GET   /categories
    - [x] POST  /categories
    - [x] GET   /categories/:category_id
    - [x] PATCH /categories/:category_id
    - [x] DEL   /categories/:category_id

  - households
    - [ ] GET   /households
    - [ ] POST  /households
    - [ ] GET   /households/:household_id
    - [ ] PATCH /households/:household_id
    - [ ] DEL   /households/:household_id

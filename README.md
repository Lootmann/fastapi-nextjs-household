# Nextjs + FastAPI

FastAPI 認証付き 家計簿 🏠

*全編AsyncSession*

## TODO

- auth
  - AsyncSession での token, JWT authentication 作成
  - Depends(get_active_user) 早めに作成

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

class Household:
   id: int
   amount: int
   registered_at: datatime
   category: Category
   user: User
```


## Endpoint

- auths
  - [ ] POST /login
  - [ ] POST /token

- users
  - [ ] GET   /users
  - [ ] GET   /users/:user_id
  - [ ] POST  /users
  - [ ] PATCH /users
  - [ ] DEL   /users

- categories
  - [ ] GET   /categories
  - [ ] POST  /categories
  - [ ] GET   /categories/:category_id
  - [ ] PATCH /categories/:category_id
  - [ ] DEL   /categories/:category_id

- households
  - [ ] GET   /households
  - [ ] POST  /households
  - [ ] GET   /households/:household_id
  - [ ] PATCH /households/:household_id
  - [ ] DEL   /households/:household_id

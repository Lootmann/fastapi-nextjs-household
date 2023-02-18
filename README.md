# Nextjs + FastAPI

FastAPI 認証付き 家計簿 🏠

*全編AsyncSession*


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

- categories
  - [ ] GET /categories
  - [ ] POST /categories
  - [ ] GET /categories/:category_id
  - [ ] PATCH /categories/:category_id
  - [ ] DEL /categories/:category_id

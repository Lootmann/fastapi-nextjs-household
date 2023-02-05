# Nextjs + FastAPI

FastAPI 認証付き 家計簿 🏠


## Models

```python
class User:
   name: str
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

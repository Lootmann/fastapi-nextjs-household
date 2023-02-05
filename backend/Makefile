run:
	python3 -m uvicorn api.main:app --reload

test:
	python3 -m pytest -v

migrate:
	python3 -m api.migrate_db

docs:
	google-chrome http://127.0.0.1:8000/docs

req:
	pip freeze > requirements.txt

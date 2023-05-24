lint:
	black .
	isort .

test:
	poetry run -m pytest

release:
	poetry publish

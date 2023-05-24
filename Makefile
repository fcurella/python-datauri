lint:
	black .
	isort .

test:
	poetry run -m pytest

release:
	poetry build
	poetry publish

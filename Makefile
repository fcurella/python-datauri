lint:
	black .
	isort .
	mypy --install-types --non-interactive --config mypy.ini datauri
	check-manifest

test:
	python -m pytest

release:
	check-manifest
	rm -rf build dist
	python setup.py sdist bdist_wheel
	twine upload dist/*

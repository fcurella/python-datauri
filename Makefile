lint:
	black .
	isort .
	mypy --install-types --non-interactive --config mypy.ini datauri
	check-manifest

test:
	python -m pytest  --pdb

release:
	check-manifest
	rm -rf build dist
	python -m build
	twine upload dist/*


test:
	poetry run coverage run -m pytest
	poetry run coverage report -m

format:
	poetry run ruff format


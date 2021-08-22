check: mypy flake8 pylint pytest

mypy:
	mypy --no-incremental --disallow-incomplete-defs --follow-imports skip *.py

flake8:
	flake8 *.py

pylint:
	pylint *.py

pytest:
	pytest test.py

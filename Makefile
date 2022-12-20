.PHONY: release test annotate


artifacts: test build


prepforbuild:
	pip install build


build:
	python -m build


test-release:
	twine upload --repository testpypi dist/*


release:
	twine upload --repository pypi dist/*


test:
	pytest tests/


init:
	pip install -r requirements.txt


test-v:
	pytest -v


test-cov-unit:
	pytest --cov-report html --cov=neoteroi tests


test-cov:
	pytest --cov-report html --cov=neoteroi


format:
	isort neoteroi
	isort tests
	black neoteroi
	black tests

.PHONY: release test annotate


artifacts: test
	python setup.py sdist


prepforbuild:
	pip install --upgrade twine setuptools wheel


testrelease:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*


release: artifacts
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*


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

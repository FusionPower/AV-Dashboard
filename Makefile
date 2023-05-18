install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint --disable=R,C *.py

format:
	black *.py

test:
	python -m pytest -vv --cov=.
	
all: install lint test

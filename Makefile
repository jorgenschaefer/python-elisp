test:
	python -Qwarnall -3 -tt -W error -m unittest discover elisp

parser:
	grako elisp/elisp.ebnf > elisp/parser.py

coverage:
	coverage run -m unittest discover
	coverage report -m --fail-under=95

clean:
	find ./* -name '*.pyc' -delete
	find ./* -name __pycache__ -delete
	rm -rf .coverage build/ dist/ elisp.egg-info/


clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +


test:
	python main.py retail_25k.dat 4
	
test-1:
	python main.py min.dat 3
	
test-2:
	python main.py retail.dat 2

run:
	python main.py retail.dat $(sigma)
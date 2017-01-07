
clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +


test-1:
	clean-pyc:
	python main.py retail_25k.dat 4
	
test-2:
	clean-pyc:
	python main.py min.dat 3
	
test-3:
	clean-pyc:
	python main.py retail.dat 2

run:
	clean-pyc:
	python main.py retail.dat $(sigma)
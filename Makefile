install:
	pip install --editable . --upgrade 

experiment:
	python gopoints/run_experiment.py local_results -c configs/experiment.ini

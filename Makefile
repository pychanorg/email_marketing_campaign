.PHONY: cli_demo test 

cli_demo:
	rm -f output/*.json output/errors.csv
	python send_email_cli.py input/email_template.json input/customers.csv output/ output/errors.csv
	@echo
	# use true to suppress errors e.g. json files not found
	cat output/*.json || true  
	@echo
	@echo
	# use true to suppress errors e.g. error file not found
	cat output/errors.csv || true  

test:
	autopep8 -i *.py
	flake8 *.py

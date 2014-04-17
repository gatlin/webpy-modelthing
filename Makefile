example: example.sql
	virtualenv ve
	ve/bin/pip install -r requirements.txt
	sqlite3 example.db < example.sql

cleanexample: example.db ve
	rm example.db
	rm -r ve
	rm *.pyc

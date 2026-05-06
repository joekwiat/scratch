python connect.py --run-query recent_queries  | head -n 20 > examples/queries.csv
python analyze.py examples/queries.csv > examples/grouped_queries.csv

.PHONY: local demo

# Run a demonstration of the local SQLite interface
local: demo

# Execute demo_check.py which exercises repository functions against a local DB
demo:
	python demo_check.py

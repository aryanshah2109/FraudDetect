# Python Interpreter
PYTHON = python

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "make install            - Install dependancies"
	@echo "make train              - Train model"
	@echo "make run                - Run API "
	@echo "make clean              - Remove artifacts"

# Install dependancies
.PHONY: install
install:
	pip install -r requirements.txt


# Train model
.PHONY: train
train:
	$(PYTHON) test.py 

# Run API
.PHONY: run
run:
	$(PYTHON) app/app.py

# Clean artifacts
.PHONY: clean
clean:
	rm -rf artifacts/*
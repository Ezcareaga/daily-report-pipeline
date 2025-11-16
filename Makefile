.PHONY: install install-dev test test-cov clean demo help

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install all dependencies (prod + dev)"
	@echo "  make test         - Run tests"
	@echo "  make test-cov     - Run tests with coverage report"
	@echo "  make demo         - Run demo script"
	@echo "  make clean        - Remove cache and temporary files"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=src --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

demo:
	python demo/demo_report.py

clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Cleaned cache files"
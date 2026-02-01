.PHONY: help install dev test coverage lint format type-check clean all

help:
	@echo "Context Guardian Development"
	@echo ""
	@echo "Commands:"
	@echo "  make install      - Install package"
	@echo "  make dev          - Install with dev dependencies"
	@echo "  make test         - Run pytest"
	@echo "  make coverage     - Generate coverage report"
	@echo "  make lint         - Run ruff linter"
	@echo "  make format       - Format code with ruff and black"
	@echo "  make type-check   - Run type checking"
	@echo "  make clean        - Remove build artifacts and cache"
	@echo "  make all          - Run all checks (test, lint, type-check)"
	@echo ""

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest -v

coverage:
	pytest --cov=src/context_guardian --cov-report=html --cov-report=term
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	ruff check src/ tests/

format:
	ruff check --fix src/ tests/
	ruff format src/ tests/

type-check:
	mypy src/context_guardian

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name *.egg-info -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name build -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name dist -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned up build artifacts and cache"

all: lint type-check test
	@echo "✓ All checks passed!"

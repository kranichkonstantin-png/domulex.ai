# Backend Tests

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run specific test
pytest tests/test_api.py::test_health_check

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

## Test Structure

- `conftest.py` - Pytest fixtures and configuration
- `test_api.py` - API endpoint tests
- `test_models.py` - Pydantic model validation tests  
- `test_services.py` - Service layer tests (PDF parser, scrapers)

## Coverage Report

After running with `--cov-report=html`, open `htmlcov/index.html` in your browser.

## CI/CD Integration

Tests are automatically run on GitHub Actions for every push and pull request.

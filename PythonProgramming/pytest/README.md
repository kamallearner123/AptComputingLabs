# Pytest Demo Project

This project demonstrates various pytest features and testing patterns.

## Project Structure

```
pytest-demo/
├── src/
│   ├── calculator.py          # Simple calculator class
│   ├── user_manager.py        # User management system
│   └── utils.py              # Utility functions
├── tests/
│   ├── test_calculator.py    # Basic tests
│   ├── test_user_manager.py  # Fixtures and parametrize
│   ├── test_utils.py         # Exception testing
│   └── conftest.py           # Shared fixtures
├── requirements.txt
└── README.md
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_calculator.py

# Run tests with coverage
pytest --cov=src

# Run tests with HTML coverage report
pytest --cov=src --cov-report=html
```

## Features Demonstrated

1. **Basic Testing** - Simple unit tests
2. **Fixtures** - Setup and teardown
3. **Parametrized Tests** - Testing multiple inputs
4. **Exception Testing** - Testing error conditions
5. **Mocking** - Testing with mocked dependencies
6. **Test Coverage** - Code coverage analysis

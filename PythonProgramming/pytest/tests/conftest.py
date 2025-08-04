"""
Shared fixtures for all tests.
This file is automatically discovered by pytest.
"""
import pytest
import tempfile
import os
from src.user_manager import UserManager, User


@pytest.fixture
def calculator():
    """Provide a Calculator instance for tests."""
    from src.calculator import Calculator
    return Calculator()


@pytest.fixture
def user_manager():
    """Provide a UserManager instance for tests."""
    return UserManager()


@pytest.fixture
def sample_user():
    """Provide a sample user for tests."""
    return User("john_doe", "john@example.com", 25)


@pytest.fixture
def multiple_users():
    """Provide multiple users for tests."""
    return [
        User("alice", "alice@example.com", 30),
        User("bob", "bob@example.com", 25),
        User("charlie", "charlie@example.com", 35),
    ]


@pytest.fixture
def temp_json_file():
    """Provide a temporary JSON file for testing."""
    # Create a temporary file
    fd, path = tempfile.mkstemp(suffix='.json')
    
    # Write some test data
    test_data = {"name": "test", "value": 42}
    with os.fdopen(fd, 'w') as f:
        import json
        json.dump(test_data, f)
    
    yield path
    
    # Cleanup
    os.unlink(path)


@pytest.fixture
def temp_directory():
    """Provide a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

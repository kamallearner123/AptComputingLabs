#!/usr/bin/env python3
"""
Demo script to showcase the pytest project functionality.
Run this to see the classes in action before running tests.
"""

from src.calculator import Calculator
from src.user_manager import UserManager, User
from src.utils import is_palindrome, fibonacci, calculate_average, format_name


def demo_calculator():
    """Demonstrate calculator functionality."""
    print("=== Calculator Demo ===")
    calc = Calculator()
    
    print(f"2 + 3 = {calc.add(2, 3)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    print(f"5 * 6 = {calc.multiply(5, 6)}")
    print(f"15 / 3 = {calc.divide(15, 3)}")
    print(f"2^4 = {calc.power(2, 4)}")
    print(f"√16 = {calc.square_root(16)}")
    
    # Demonstrate error handling
    try:
        calc.divide(10, 0)
    except ValueError as e:
        print(f"Error caught: {e}")
    
    print()


def demo_user_manager():
    """Demonstrate user management functionality."""
    print("=== User Manager Demo ===")
    manager = UserManager()
    
    # Create and add users
    users = [
        User("alice", "alice@example.com", 25),
        User("bob", "bob@example.com", 30),
        User("charlie", "charlie@example.com", 35),
    ]
    
    for user in users:
        manager.add_user(user)
        print(f"Added user: {user}")
    
    print(f"\nTotal users: {len(manager.get_all_users())}")
    
    # Deactivate a user
    manager.deactivate_user("bob")
    print(f"Active users: {len(manager.get_active_users())}")
    
    # Filter by age
    young_users = manager.get_users_by_age_range(20, 30)
    print(f"Users aged 20-30: {[u.username for u in young_users]}")
    
    print()


def demo_utils():
    """Demonstrate utility functions."""
    print("=== Utils Demo ===")
    
    # Palindrome test
    test_words = ["racecar", "hello", "A man a plan a canal Panama"]
    for word in test_words:
        result = is_palindrome(word)
        print(f"'{word}' is palindrome: {result}")
    
    # Fibonacci
    print(f"\nFibonacci(10) = {fibonacci(10)}")
    
    # Average
    numbers = [1, 2, 3, 4, 5]
    avg = calculate_average(numbers)
    print(f"Average of {numbers} = {avg}")
    
    # Name formatting
    name1 = format_name("John", "Doe")
    name2 = format_name("Jane", "Smith", "Dr.")
    print(f"Name 1: {name1}")
    print(f"Name 2: {name2}")
    
    print()


if __name__ == "__main__":
    print("Pytest Demo Project - Functionality Showcase")
    print("=" * 50)
    
    demo_calculator()
    demo_user_manager()
    demo_utils()
    
    print("Demo completed! Now run 'pytest' to see the tests in action.")
    print("Try these commands:")
    print("  pytest -v                    # Verbose test output")
    print("  pytest --cov=src            # Run with coverage")
    print("  pytest tests/test_calculator.py  # Run specific test file")
    print("  pytest -k 'test_add'        # Run tests matching pattern")

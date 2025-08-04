"""
Utility functions to demonstrate various testing scenarios.
"""
import json
import os
from typing import List, Dict, Any


def is_palindrome(text: str) -> bool:
    """Check if a string is a palindrome."""
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    
    # Remove spaces and convert to lowercase
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]


def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    
    if n < 0:
        raise ValueError("Input must be non-negative")
    
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b


def read_json_file(filepath: str) -> Dict[Any, Any]:
    """Read and parse a JSON file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")


def write_json_file(data: Dict[Any, Any], filepath: str) -> None:
    """Write data to a JSON file."""
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=2)
    except Exception as e:
        raise IOError(f"Failed to write file: {e}")


def calculate_average(numbers: List[float]) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        raise ValueError("List cannot be empty")
    
    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("All elements must be numbers")
    
    return sum(numbers) / len(numbers)


def format_name(first_name: str, last_name: str, title: str = None) -> str:
    """Format a person's name."""
    if not first_name or not last_name:
        raise ValueError("First name and last name are required")
    
    if title:
        return f"{title} {first_name} {last_name}"
    return f"{first_name} {last_name}"

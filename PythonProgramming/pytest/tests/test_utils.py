"""
Tests for utility functions demonstrating exception testing and mocking.
"""
import pytest
import os
import tempfile
from unittest.mock import patch, mock_open
from src.utils import (
    is_palindrome, fibonacci, read_json_file, write_json_file,
    calculate_average, format_name
)


class TestPalindrome:
    """Test palindrome function."""
    
    @pytest.mark.parametrize("text,expected", [
        ("racecar", True),
        ("A man a plan a canal Panama", True),
        ("race a car", False),
        ("hello", False),
        ("", True),  # Empty string is considered palindrome
        ("a", True),
    ])
    def test_is_palindrome(self, text, expected):
        """Test palindrome detection with various inputs."""
        assert is_palindrome(text) == expected
    
    def test_is_palindrome_with_non_string_raises_error(self):
        """Test that non-string input raises TypeError."""
        with pytest.raises(TypeError, match="Input must be a string"):
            is_palindrome(123)


class TestFibonacci:
    """Test Fibonacci function."""
    
    @pytest.mark.parametrize("n,expected", [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (10, 55),
    ])
    def test_fibonacci(self, n, expected):
        """Test Fibonacci calculation with various inputs."""
        assert fibonacci(n) == expected
    
    def test_fibonacci_with_negative_raises_error(self):
        """Test that negative input raises ValueError."""
        with pytest.raises(ValueError, match="Input must be non-negative"):
            fibonacci(-1)
    
    def test_fibonacci_with_non_integer_raises_error(self):
        """Test that non-integer input raises TypeError."""
        with pytest.raises(TypeError, match="Input must be an integer"):
            fibonacci(3.5)


class TestJsonFileOperations:
    """Test JSON file operations."""
    
    def test_read_json_file(self, temp_json_file):
        """Test reading a valid JSON file."""
        data = read_json_file(temp_json_file)
        assert data == {"name": "test", "value": 42}
    
    def test_read_nonexistent_file_raises_error(self):
        """Test that reading non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            read_json_file("/nonexistent/path/file.json")
    
    def test_read_invalid_json_raises_error(self, temp_directory):
        """Test that reading invalid JSON raises ValueError."""
        # Create a file with invalid JSON
        invalid_json_file = os.path.join(temp_directory, "invalid.json")
        with open(invalid_json_file, 'w') as f:
            f.write("{ invalid json }")
        
        with pytest.raises(ValueError, match="Invalid JSON format"):
            read_json_file(invalid_json_file)
    
    def test_write_json_file(self, temp_directory):
        """Test writing data to JSON file."""
        test_data = {"test": "data", "number": 123}
        output_file = os.path.join(temp_directory, "output.json")
        
        write_json_file(test_data, output_file)
        
        # Verify the file was written correctly
        assert os.path.exists(output_file)
        written_data = read_json_file(output_file)
        assert written_data == test_data
    
    @patch("builtins.open", side_effect=IOError("Permission denied"))
    def test_write_json_file_io_error(self, mock_file):
        """Test that IOError during write raises IOError."""
        with pytest.raises(IOError, match="Failed to write file"):
            write_json_file({"test": "data"}, "/invalid/path.json")


class TestCalculateAverage:
    """Test average calculation function."""
    
    @pytest.mark.parametrize("numbers,expected", [
        ([1, 2, 3, 4, 5], 3.0),
        ([10, 20, 30], 20.0),
        ([5], 5.0),
        ([1.5, 2.5, 3.5], 2.5),
        ([-1, 0, 1], 0.0),
    ])
    def test_calculate_average(self, numbers, expected):
        """Test average calculation with various inputs."""
        assert calculate_average(numbers) == expected
    
    def test_calculate_average_empty_list_raises_error(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError, match="List cannot be empty"):
            calculate_average([])
    
    def test_calculate_average_non_numeric_raises_error(self):
        """Test that non-numeric values raise TypeError."""
        with pytest.raises(TypeError, match="All elements must be numbers"):
            calculate_average([1, 2, "3", 4])


class TestFormatName:
    """Test name formatting function."""
    
    def test_format_name_without_title(self):
        """Test formatting name without title."""
        result = format_name("John", "Doe")
        assert result == "John Doe"
    
    def test_format_name_with_title(self):
        """Test formatting name with title."""
        result = format_name("John", "Doe", "Dr.")
        assert result == "Dr. John Doe"
    
    @pytest.mark.parametrize("first_name,last_name", [
        ("", "Doe"),
        ("John", ""),
        ("", ""),
        (None, "Doe"),
        ("John", None),
    ])
    def test_format_name_missing_names_raises_error(self, first_name, last_name):
        """Test that missing names raise ValueError."""
        with pytest.raises(ValueError, match="First name and last name are required"):
            format_name(first_name, last_name)

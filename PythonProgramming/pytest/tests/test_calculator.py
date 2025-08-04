"""
Tests for the Calculator class demonstrating basic pytest functionality.
"""
import pytest
from src.calculator import Calculator


class TestCalculator:
    """Test class for Calculator."""
    
    def test_add_positive_numbers(self, calculator):
        """Test adding positive numbers."""
        result = calculator.add(2, 3)
        assert result == 5
    
    def test_add_negative_numbers(self, calculator):
        """Test adding negative numbers."""
        result = calculator.add(-2, -3)
        assert result == -5
    
    def test_add_mixed_numbers(self, calculator):
        """Test adding positive and negative numbers."""
        result = calculator.add(5, -3)
        assert result == 2
    
    def test_subtract(self, calculator):
        """Test subtraction."""
        result = calculator.subtract(10, 4)
        assert result == 6
    
    def test_multiply(self, calculator):
        """Test multiplication."""
        result = calculator.multiply(3, 4)
        assert result == 12
    
    def test_multiply_by_zero(self, calculator):
        """Test multiplication by zero."""
        result = calculator.multiply(5, 0)
        assert result == 0
    
    def test_divide(self, calculator):
        """Test division."""
        result = calculator.divide(10, 2)
        assert result == 5.0
    
    def test_divide_by_zero_raises_error(self, calculator):
        """Test that division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calculator.divide(10, 0)
    
    def test_power(self, calculator):
        """Test power calculation."""
        result = calculator.power(2, 3)
        assert result == 8
    
    def test_power_with_invalid_input(self, calculator):
        """Test power with invalid input types."""
        with pytest.raises(TypeError, match="Both arguments must be numbers"):
            calculator.power("2", 3)
    
    def test_square_root(self, calculator):
        """Test square root calculation."""
        result = calculator.square_root(9)
        assert result == 3.0
    
    def test_square_root_negative_raises_error(self, calculator):
        """Test that square root of negative number raises ValueError."""
        with pytest.raises(ValueError, match="Cannot calculate square root of negative number"):
            calculator.square_root(-4)
    
    # Parametrized test example
    @pytest.mark.parametrize("a,b,expected", [
        (1, 1, 2),
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
        (100, 200, 300),
    ])
    def test_add_parametrized(self, calculator, a, b, expected):
        """Test addition with multiple parameter sets."""
        assert calculator.add(a, b) == expected
    
    @pytest.mark.parametrize("dividend,divisor,expected", [
        (10, 2, 5.0),
        (15, 3, 5.0),
        (7, 2, 3.5),
        (0, 5, 0.0),
    ])
    def test_divide_parametrized(self, calculator, dividend, divisor, expected):
        """Test division with multiple parameter sets."""
        assert calculator.divide(dividend, divisor) == expected

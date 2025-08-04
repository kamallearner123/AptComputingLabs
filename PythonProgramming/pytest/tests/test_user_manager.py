"""
Tests for the UserManager class demonstrating fixtures and complex scenarios.
"""
import pytest
from src.user_manager import UserManager, User


class TestUser:
    """Test the User class."""
    
    def test_user_creation(self):
        """Test creating a user."""
        user = User("testuser", "test@example.com", 30)
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.age == 30
        assert user.is_active is True
    
    def test_user_without_age(self):
        """Test creating a user without age."""
        user = User("testuser", "test@example.com")
        assert user.age is None


class TestUserManager:
    """Test the UserManager class."""
    
    def test_add_user(self, user_manager, sample_user):
        """Test adding a user."""
        added_user = user_manager.add_user(sample_user)
        assert added_user == sample_user
        assert user_manager.get_user("john_doe") == sample_user
    
    def test_add_duplicate_user_raises_error(self, user_manager, sample_user):
        """Test that adding duplicate user raises error."""
        user_manager.add_user(sample_user)
        
        duplicate_user = User("john_doe", "different@example.com")
        with pytest.raises(ValueError, match="User 'john_doe' already exists"):
            user_manager.add_user(duplicate_user)
    
    def test_add_user_with_invalid_email_raises_error(self, user_manager):
        """Test that adding user with invalid email raises error."""
        invalid_user = User("testuser", "invalid-email")
        with pytest.raises(ValueError, match="Invalid email format"):
            user_manager.add_user(invalid_user)
    
    def test_get_nonexistent_user_returns_none(self, user_manager):
        """Test getting a non-existent user returns None."""
        assert user_manager.get_user("nonexistent") is None
    
    def test_remove_user(self, user_manager, sample_user):
        """Test removing a user."""
        user_manager.add_user(sample_user)
        user_manager.remove_user("john_doe")
        assert user_manager.get_user("john_doe") is None
    
    def test_remove_nonexistent_user_raises_error(self, user_manager):
        """Test that removing non-existent user raises error."""
        with pytest.raises(KeyError, match="User 'nonexistent' not found"):
            user_manager.remove_user("nonexistent")
    
    def test_get_all_users(self, user_manager, multiple_users):
        """Test getting all users."""
        for user in multiple_users:
            user_manager.add_user(user)
        
        all_users = user_manager.get_all_users()
        assert len(all_users) == 3
        assert all(user in all_users for user in multiple_users)
    
    def test_get_active_users(self, user_manager, multiple_users):
        """Test getting only active users."""
        for user in multiple_users:
            user_manager.add_user(user)
        
        # Deactivate one user
        user_manager.deactivate_user("bob")
        
        active_users = user_manager.get_active_users()
        assert len(active_users) == 2
        assert all(user.is_active for user in active_users)
    
    def test_deactivate_user(self, user_manager, sample_user):
        """Test deactivating a user."""
        user_manager.add_user(sample_user)
        user_manager.deactivate_user("john_doe")
        
        user = user_manager.get_user("john_doe")
        assert user.is_active is False
    
    def test_deactivate_nonexistent_user_raises_error(self, user_manager):
        """Test that deactivating non-existent user raises error."""
        with pytest.raises(KeyError, match="User 'nonexistent' not found"):
            user_manager.deactivate_user("nonexistent")
    
    def test_get_users_by_age_range(self, user_manager):
        """Test filtering users by age range."""
        users = [
            User("young", "young@example.com", 20),
            User("middle", "middle@example.com", 30),
            User("old", "old@example.com", 40),
            User("no_age", "no_age@example.com"),  # No age
        ]
        
        for user in users:
            user_manager.add_user(user)
        
        # Get users between 25 and 35
        filtered_users = user_manager.get_users_by_age_range(25, 35)
        assert len(filtered_users) == 1
        assert filtered_users[0].username == "middle"
    
    @pytest.mark.parametrize("email,expected", [
        ("valid@example.com", True),
        ("another.valid@domain.org", True),
        ("invalid-email", False),
        ("missing@domain", False),
        ("@example.com", False),
        ("user@", False),
    ])
    def test_email_validation(self, user_manager, email, expected):
        """Test email validation with various inputs."""
        result = user_manager._is_valid_email(email)
        assert result == expected

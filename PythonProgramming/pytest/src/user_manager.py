"""
User management system to demonstrate fixtures and more complex testing scenarios.
"""


class User:
    """Represents a user in the system."""
    
    def __init__(self, username, email, age=None):
        self.username = username
        self.email = email
        self.age = age
        self.is_active = True
    
    def __repr__(self):
        return f"User(username='{self.username}', email='{self.email}')"


class UserManager:
    """Manages users in the system."""
    
    def __init__(self):
        self.users = {}
    
    def add_user(self, user):
        """Add a user to the system."""
        if user.username in self.users:
            raise ValueError(f"User '{user.username}' already exists")
        
        if not self._is_valid_email(user.email):
            raise ValueError("Invalid email format")
        
        self.users[user.username] = user
        return user
    
    def get_user(self, username):
        """Get a user by username."""
        return self.users.get(username)
    
    def remove_user(self, username):
        """Remove a user from the system."""
        if username not in self.users:
            raise KeyError(f"User '{username}' not found")
        
        del self.users[username]
    
    def get_all_users(self):
        """Get all users."""
        return list(self.users.values())
    
    def get_active_users(self):
        """Get all active users."""
        return [user for user in self.users.values() if user.is_active]
    
    def deactivate_user(self, username):
        """Deactivate a user."""
        if username not in self.users:
            raise KeyError(f"User '{username}' not found")
        
        self.users[username].is_active = False
    
    def get_users_by_age_range(self, min_age, max_age):
        """Get users within an age range."""
        return [
            user for user in self.users.values() 
            if user.age is not None and min_age <= user.age <= max_age
        ]
    
    def _is_valid_email(self, email):
        """Basic email validation."""
        return "@" in email and "." in email.split("@")[-1]

from sqlalchemy.orm import Session
from sqlalchemy import or_
from .base_controller import BaseController
from epic_events.models.user import User
from epic_events.utils.display import print_success, print_error


class UserController(BaseController):
    def create_user(self, full_name, email, password, department, current_user):
        """Create a new user (management only)"""
        try:
            self.check_permission(current_user, 'management')

            # Check if user already exists
            existing_user = self.db.query(User).filter(
                or_(User.email == email)
            ).first()

            if existing_user:
                return print_error(f"User with email {email} already exists")

            # Validate department
            valid_departments = ['management', 'sales', 'support']
            if department not in valid_departments:
                return print_error(f"Invalid department. Must be one of: {', '.join(valid_departments)}")

            # Create new user
            new_user = User(
                full_name=full_name,
                email=email,
                department=department
            )
            new_user.set_password(password)

            self.db.add(new_user)
            if self.commit_changes():
                return print_success(f"User {full_name} created successfully with {department} role")
            return print_error("Failed to create user")

        except PermissionError as e:
            return print_error(str(e))
        except Exception as e:
            return print_error(self.handle_error(e, "creating user"))

    def update_user(self, user_id, current_user, **kwargs):
        """Update user information (management only)"""
        try:
            self.check_permission(current_user, 'management')

            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return print_error("User not found")

            # Update fields
            for key, value in kwargs.items():
                if hasattr(user, key) and value is not None:
                    if key == 'password':
                        user.set_password(value)
                    else:
                        setattr(user, key, value)

            if self.commit_changes():
                return print_success(f"User {user.full_name} updated successfully")
            return print_error("Failed to update user")

        except PermissionError as e:
            return print_error(str(e))
        except Exception as e:
            return print_error(self.handle_error(e, "updating user"))

    def get_all_users(self, current_user):
        """Get all users (management only)"""
        try:
            self.check_permission(current_user, 'management')
            users = self.db.query(User).all()
            return users
        except PermissionError as e:
            print_error(str(e))
            return []
        except Exception as e:
            print_error(self.handle_error(e, "fetching users"))
            return []

    def get_user_by_id(self, user_id, current_user):
        """Get specific user by ID (management only)"""
        try:
            self.check_permission(current_user, 'management')
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                print_error("User not found")
                return None
            return user
        except PermissionError as e:
            print_error(str(e))
            return None
        except Exception as e:
            print_error(self.handle_error(e, "fetching user"))
            return None

    def delete_user(self, user_id, current_user):
        """Delete a user (management only)"""
        try:
            self.check_permission(current_user, 'management')

            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return print_error("User not found")

            # Prevent deleting yourself
            if user.id == current_user.id:
                return print_error("Cannot delete your own account")

            # Check if user has clients, contracts, or events
            if user.clients or user.contracts or user.events:
                return print_error("Cannot delete user with assigned clients, contracts, or events")

            self.db.delete(user)
            if self.commit_changes():
                return print_success(f"User {user.full_name} deleted successfully")
            return print_error("Failed to delete user")

        except PermissionError as e:
            return print_error(str(e))
        except Exception as e:
            return print_error(self.handle_error(e, "deleting user"))


# Create a global instance
user_controller = UserController()
from sqlalchemy.orm import Session
from epic_events.utils.database import get_db
from epic_events.utils.session import session_manager
from epic_events.utils.permissions import has_management_permission, has_sales_permission, has_support_permission
import sentry_sdk


class BaseController:
    def __init__(self):
        self.db = next(get_db())

    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()

    def has_permission(self, user, required_permission):
        """Check if user has required permission"""
        permission_map = {
            'management': has_management_permission,
            'sales': has_sales_permission,
            'support': has_support_permission
        }

        if required_permission in permission_map:
            return permission_map[required_permission](user)
        return False

    def check_permission(self, user, required_permission):
        """Check permission and raise exception if not authorized"""
        if not self.has_permission(user, required_permission):
            raise PermissionError(f"User does not have {required_permission} permission")

    def handle_error(self, error, context=""):
        """Handle errors and log to Sentry"""
        error_msg = f"Error {context}: {str(error)}"
        sentry_sdk.capture_exception(error)
        return error_msg

    def commit_changes(self):
        """Commit changes to database with error handling"""
        try:
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            self.handle_error(e, "committing changes")
            return False
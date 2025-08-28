import json
import os
from datetime import datetime, timedelta


class SessionManager:
    def __init__(self, session_file='.session'):
        self.session_file = session_file
        self.current_user = None
        self.session_data = {}

    def create_session(self, user):
        """Create a new session for authenticated user"""
        self.current_user = user
        self.session_data = {
            'user_id': user.id,
            'email': user.email,
            'department': user.department,
            'login_time': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(hours=8)).isoformat()
        }
        self._save_session()

    def load_session(self):
        """Load existing session from file"""
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    self.session_data = json.load(f)

                # Check if session is expired
                expires_at = datetime.fromisoformat(self.session_data['expires_at'])
                if datetime.now() > expires_at:
                    self.clear_session()
                    return False

                return True
            except (json.JSONDecodeError, KeyError):
                self.clear_session()
                return False
        return False

    def clear_session(self):
        """Clear current session"""
        self.current_user = None
        self.session_data = {}
        if os.path.exists(self.session_file):
            os.remove(self.session_file)

    def _save_session(self):
        """Save session to file"""
        with open(self.session_file, 'w') as f:
            json.dump(self.session_data, f)

    def get_current_user_id(self):
        """Get current user ID from session"""
        return self.session_data.get('user_id')

    def get_current_department(self):
        """Get current user department from session"""
        return self.session_data.get('department')


# Global session manager instance
session_manager = SessionManager()
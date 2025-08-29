from epic_events.utils.database import get_db
from epic_events.utils.auth import authenticate_user
from epic_events.utils.session import session_manager
from epic_events.models.user import User


def login(email: str, password: str):
    """Authenticate user and create session if successful"""
    db = next(get_db())
    try:
        user = authenticate_user(email, password, db)
        if user:
            session_manager.create_session(user)
            return user
        return None
    except Exception as e:
        raise e
    finally:
        db.close()


def logout():
    """Clear current session"""
    session_manager.clear_session()


def get_current_user():
    """Get current user from session"""
    if session_manager.current_user:
        return session_manager.current_user

    if session_manager.load_session():
        db = next(get_db())
        try:
            user_id = session_manager.get_current_user_id()
            if user_id:
                user = db.query(User).filter(User.id == user_id).first()
                session_manager.current_user = user
                return user
        finally:
            db.close()
    return None


def require_auth(func):
    """Decorator to require authentication for commands"""

    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            print("Please login first. Use: python main.py auth")
            return
        return func(*args, **kwargs, current_user=user)

    return wrapper

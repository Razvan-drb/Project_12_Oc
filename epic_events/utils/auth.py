from sqlalchemy.orm import Session
from epic_events.models.user import User


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if user and user.check_password(password):
        return user
    return None

def get_current_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
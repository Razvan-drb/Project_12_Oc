#!/usr/bin/env python3

from config import Config
from epic_events.models import User
from epic_events.utils.database import init_db, get_db


def test_database_connection():
    """Test database connection and basic operations"""
    print("Testing database connection...")
    print(f"Database URL: {Config.DATABASE_URL}")

    # Initialize database
    init_db()
    print("Database initialized successfully!")

    # Test creating a user
    db = next(get_db())
    try:
        test_user = User(
            full_name="Test User",
            email="test@epicevents.com",
            department="management"
        )
        test_user.set_password("testpassword")

        db.add(test_user)
        db.commit()
        print("Test user created successfully!")

        # Verify user can be retrieved
        user_from_db = db.query(User).filter_by(email="test@epicevents.com").first()
        if user_from_db and user_from_db.check_password("testpassword"):
            print("User authentication test passed!")
        else:
            print("User authentication test failed!")

    except Exception as e:
        print(f"Error during test: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    test_database_connection()
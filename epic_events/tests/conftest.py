import pytest
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from epic_events.utils.database import Base
from epic_events.models.user import User
from epic_events.models.client import Client

# Use in-memory database for tests
TEST_DATABASE_URL = 'sqlite:///:memory:'
test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope='session', autouse=True)
def create_test_tables():
    """Create all tables once for the test session"""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(autouse=True)
def setup_test_data():
    """Set up test data before each test"""
    db = TestingSessionLocal()
    try:
        # Clean any existing data
        db.query(Client).delete()
        db.query(User).delete()

        # Create test users
        management_user = User(
            full_name="Test Manager",
            email="test_manager@epicevents.com",
            department="management"
        )
        management_user.set_password("test123")
        db.add(management_user)

        sales_user = User(
            full_name="Test Sales",
            email="test_sales@epicevents.com",
            department="sales"
        )
        sales_user.set_password("test123")
        db.add(sales_user)

        support_user = User(
            full_name="Test Support",
            email="test_support@epicevents.com",
            department="support"
        )
        support_user.set_password("test123")
        db.add(support_user)

        # Create test clients
        client1 = Client(
            full_name="Test Client 1",
            email="client1@test.com",
            phone="+1234567890",
            company_name="Test Company 1",
            commercial_contact_id=sales_user.id
        )
        db.add(client1)

        client2 = Client(
            full_name="Test Client 2",
            email="client2@test.com",
            phone="+0987654321",
            company_name="Test Company 2",
            commercial_contact_id=sales_user.id
        )
        db.add(client2)

        db.commit()
    finally:
        db.close()


@pytest.fixture
def db_session():
    """Provide a clean database session for each test"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # No need to rollback since we're using a new session each time


# Monkey patch the get_db function to use our test session
from epic_events.utils import database

original_get_db = database.get_db


def test_get_db():
    """Override get_db to use test session"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Apply the patch for the test session
database.get_db = test_get_db
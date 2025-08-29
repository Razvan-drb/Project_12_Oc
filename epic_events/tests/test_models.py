import pytest
from epic_events.models.user import User
from epic_events.models.client import Client
from epic_events.models.contract import Contract
from epic_events.models.event import Event


def test_user_model_creation(db_session):
    """Test User model creation and password hashing"""
    user = User(
        full_name="John Doe",
        email="john@test.com",
        department="sales"
    )
    user.set_password("securepassword")

    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.check_password("securepassword") == True
    assert user.check_password("wrongpassword") == False


def test_client_model(db_session):
    """Test Client model and relationships"""
    # Create user first
    user = User(full_name="Sales Person", email="sales@test.com", department="sales")
    user.set_password("test")
    db_session.add(user)
    db_session.commit()

    client = Client(
        full_name="Test Client",
        email="client@test.com",
        phone="+123456789",
        company_name="Test Company",
        commercial_contact_id=user.id
    )

    db_session.add(client)
    db_session.commit()

    assert client.id is not None
    assert client.commercial_contact_id == user.id

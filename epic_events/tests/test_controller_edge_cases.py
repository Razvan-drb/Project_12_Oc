import pytest
from epic_events.controllers.auth_controller import login
from epic_events.controllers.client_controller import client_controller
from epic_events.controllers.contract_controller import contract_controller
from epic_events.controllers.event_controller import event_controller
from epic_events.controllers.user_controller import user_controller


def test_client_controller_edge_cases(db_session):
    """Test edge cases for ClientController"""
    user = login("test_manager@epicevents.com", "test123")

    # Test creating client with duplicate email/phone
    from epic_events.models.client import Client
    existing_client = db_session.query(Client).first()
    if existing_client:
        result = client_controller.create_client(
            "Duplicate Client",
            existing_client.email,  # Duplicate email
            "+9999999999",
            "Test Co",
            user
        )
        # Should print error about duplicate email

    # Test updating non-existent client
    result = client_controller.update_client(9999, user, full_name="Non-existent")
    # Should print error about client not found

    # Test deleting non-existent client
    result = client_controller.delete_client(9999, user)
    # Should print error about client not found


def test_contract_controller_edge_cases(db_session):
    """Test edge cases for ContractController"""
    user = login("test_manager@epicevents.com", "test123")

    # Test creating contract for non-existent client
    result = contract_controller.create_contract(9999, 1000.0, user)
    # Should print error about client not found

    # Test updating non-existent contract
    result = contract_controller.update_contract(9999, user, is_signed=True)
    # Should print error about contract not found


def test_event_controller_edge_cases(db_session):
    """Test edge cases for EventController"""
    user = login("test_manager@epicevents.com", "test123")

    # Test creating event for non-existent contract
    from datetime import datetime
    result = event_controller.create_event(
        9999,  # Non-existent contract
        "Test Event",
        datetime.now(),
        datetime.now(),
        "Test Location",
        100,
        "Test notes",
        user
    )
    # Should print error about contract not found

    # Test assigning support to non-existent event
    result = event_controller.assign_support_contact(9999, 1, user)
    # Should print error about event not found

    # Test assigning non-existent support user
    events = event_controller.get_all_events(user)
    if events:
        result = event_controller.assign_support_contact(events[0].id, 9999, user)
        # Should print error about invalid support contact


def test_user_controller_edge_cases(db_session):
    """Test edge cases for UserController"""
    user = login("test_manager@epicevents.com", "test123")

    # Test creating user with duplicate email
    from epic_events.models.user import User
    existing_user = db_session.query(User).first()
    if existing_user:
        result = user_controller.create_user(
            "Duplicate User",
            existing_user.email,  # Duplicate email
            "password",
            "sales",
            user
        )
        # Should print error about duplicate email

    # Test updating non-existent user
    result = user_controller.update_user(9999, user, full_name="Non-existent")
    # Should print error about user not found

    # Test deleting non-existent user
    result = user_controller.delete_user(9999, user)
    # Should print error about user not found

    # Test deleting self (should fail)
    result = user_controller.delete_user(user.id, user)
    # Should print error about cannot delete own account
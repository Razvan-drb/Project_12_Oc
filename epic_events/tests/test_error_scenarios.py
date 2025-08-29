import pytest
from epic_events.controllers.auth_controller import login
from epic_events.controllers.client_controller import client_controller
from epic_events.controllers.contract_controller import contract_controller
from epic_events.controllers.event_controller import event_controller
from epic_events.controllers.user_controller import user_controller


def test_permission_denied_scenarios():
    """Test permission denied scenarios"""
    # Sales user trying to access management functions
    sales_user = login("test_sales@epicevents.com", "test123")

    # Sales should not be able to access user management
    users = user_controller.get_all_users(sales_user)
    assert users == []  # Should return empty list due to permission error

    # Sales should not be able to create contracts
    result = contract_controller.create_contract(1, 1000.0, sales_user)
    # Should print permission error

    # Support user trying to access sales functions
    support_user = login("test_support@epicevents.com", "test123")

    # Support should not be able to create clients
    result = client_controller.create_client("Test", "test@test.com", "+123", "Test Co", support_user)
    # Should print permission error


def test_nonexistent_entities():
    """Test handling of non-existent entities"""
    user = login("test_manager@epicevents.com", "test123")

    # Non-existent client
    client = client_controller.get_client_by_id(9999, user)
    assert client is None

    # Non-existent contract
    contract = contract_controller.get_contract_by_id(9999, user)
    assert contract is None

    # Non-existent event
    event = event_controller.get_event_by_id(9999, user)
    assert event is None

    # Non-existent user
    user_obj = user_controller.get_user_by_id(9999, user)
    assert user_obj is None


def test_authentication_failures():
    """Test various authentication failure scenarios"""
    # Invalid login
    user = login("invalid@email.com", "wrongpassword")
    assert user is None

    # Empty credentials
    user = login("", "")
    assert user is None
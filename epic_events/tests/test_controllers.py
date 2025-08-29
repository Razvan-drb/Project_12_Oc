import pytest
from epic_events.controllers.client_controller import client_controller
from epic_events.controllers.auth_controller import login


def test_client_creation(db_session):
    """Test client creation with proper permissions"""
    # Login as sales user (can create clients)
    user = login("test_sales@epicevents.com", "test123")

    # The controller prints the message but returns None
    # We need to check if the client was actually created
    from epic_events.models.client import Client

    # Count clients before creation
    initial_count = db_session.query(Client).count()

    # Create client
    client_controller.create_client(
        "New Client", "new@client.com", "+123456", "Client Co", user
    )

    # Count clients after creation
    final_count = db_session.query(Client).count()

    # Verify client was created
    assert final_count == initial_count + 1

    # Verify the new client exists
    new_client = db_session.query(Client).filter_by(email="new@client.com").first()
    assert new_client is not None
    assert new_client.full_name == "New Client"


def test_permission_checks(db_session):
    """Test role-based permission checks"""
    from epic_events.utils.permissions import has_management_permission, has_sales_permission

    # Login as sales user
    sales_user = login("test_sales@epicevents.com", "test123")
    assert has_sales_permission(sales_user) == True
    assert has_management_permission(sales_user) == False

    # Login as management user
    management_user = login("test_manager@epicevents.com", "test123")
    assert has_management_permission(management_user) == True

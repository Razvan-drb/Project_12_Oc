from epic_events.controllers.auth_controller import login
from epic_events.controllers.contract_controller import contract_controller
from epic_events.controllers.event_controller import event_controller
from epic_events.controllers.user_controller import user_controller


def test_contract_controller_final(db_session):
    """Final comprehensive test for ContractController"""
    user = login("test_manager@epicevents.com", "test123")

    # Test create_contract with valid data
    from epic_events.models.client import Client
    client = db_session.query(Client).first()
    if client:
        contract_controller.create_contract(client.id, 5000.0, user)
        # Should print success message

    # Test get_my_contracts (sales perspective)
    sales_user = login("test_sales@epicevents.com", "test123")
    my_contracts = contract_controller.get_my_contracts(sales_user)
    assert isinstance(my_contracts, list)

    # Test update_contract with various fields
    contracts = contract_controller.get_all_contracts(user)
    if contracts:
        # Update amount
        contract_controller.update_contract(contracts[0].id, user, total_amount=6000.0)

        # Update amount due
        contract_controller.update_contract(contracts[0].id, user, amount_due=3000.0)

        # Update signed status
        contract_controller.update_contract(contracts[0].id, user, is_signed=True)


def test_event_controller_final(db_session):
    """Final comprehensive test for EventController"""
    user = login("test_manager@epicevents.com", "test123")

    # Test create_event with valid data
    from epic_events.models.contract import Contract
    from epic_events.models.client import Client
    from datetime import datetime, timedelta

    contract = db_session.query(Contract).first()
    if not contract:
        # Create a contract first if none exists
        client = db_session.query(Client).first()
        if client:
            new_contract = Contract(
                client_id=client.id,
                commercial_contact_id=client.commercial_contact_id,
                total_amount=5000.0,
                amount_due=5000.0,
                is_signed=True
            )
            db_session.add(new_contract)
            db_session.commit()
            contract = new_contract

    if contract:
        event_controller.create_event(
            contract.id,
            "Test Event Final",
            datetime.now() + timedelta(days=7),
            datetime.now() + timedelta(days=7, hours=4),
            "Test Location Final",
            150,
            "Test notes final",
            user
        )
        # Should print success message

    # Test get_my_events for different user types
    sales_user = login("test_sales@epicevents.com", "test123")
    sales_events = event_controller.get_my_events(sales_user)
    assert isinstance(sales_events, list)

    support_user = login("test_support@epicevents.com", "test123")
    support_events = event_controller.get_my_events(support_user)
    assert isinstance(support_events, list)

    # Test update_event with various fields
    events = event_controller.get_all_events(user)
    if events:
        event_controller.update_event(events[0].id, user, name="Updated Event Name")
        event_controller.update_event(events[0].id, user, attendees=200)
        event_controller.update_event(events[0].id, user, notes="Updated notes")


def test_user_controller_final(db_session):
    """Final comprehensive test for UserController"""
    user = login("test_manager@epicevents.com", "test123")

    # Test create_user with valid data
    user_controller.create_user(
        "Final Test User",
        "finaluser@test.com",
        "password123",
        "support",
        user
    )
    # Should print success message

    # Test update_user with various fields
    users = user_controller.get_all_users(user)
    if users:
        # Update name
        user_controller.update_user(users[0].id, user, full_name="Updated User Name")

        # Update email
        user_controller.update_user(users[0].id, user, email="updated@test.com")

        # Update department
        user_controller.update_user(users[0].id, user, department="sales")

        # Update password
        user_controller.update_user(users[0].id, user, password="newpassword123")


def test_auth_controller_final():
    """Final comprehensive test for AuthController"""
    # Test logout functionality
    from epic_events.controllers.auth_controller import logout

    # First login to create a session
    user = login("test_manager@epicevents.com", "test123")
    assert user is not None

    # Test logout
    logout()

    # Test get_current_user after logout
    from epic_events.controllers.auth_controller import get_current_user
    current_user = get_current_user()
    assert current_user is None

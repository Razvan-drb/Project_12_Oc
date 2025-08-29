import pytest
from epic_events.controllers.auth_controller import login
from epic_events.controllers.client_controller import client_controller
from epic_events.controllers.contract_controller import contract_controller
from epic_events.controllers.event_controller import event_controller
from epic_events.controllers.user_controller import user_controller


def test_client_controller_comprehensive(db_session):
    """Test all ClientController methods"""
    user = login("test_manager@epicevents.com", "test123")

    # Test get_all_clients
    clients = client_controller.get_all_clients(user)
    assert isinstance(clients, list)

    # Test get_my_clients (as sales user)
    sales_user = login("test_sales@epicevents.com", "test123")
    my_clients = client_controller.get_my_clients(sales_user)
    assert isinstance(my_clients, list)

    # Test get_client_by_id with existing client
    if clients:
        client = client_controller.get_client_by_id(clients[0].id, user)
        assert client is not None

    # Test get_client_by_id with non-existent client
    client = client_controller.get_client_by_id(9999, user)
    assert client is None

    # Test update_client
    if clients:
        result = client_controller.update_client(clients[0].id, user, full_name="Updated Name")
        # The controller prints success but returns None

    # Test delete_client (management only)
    if clients:
        result = client_controller.delete_client(clients[0].id, user)
        # The controller prints success but returns None


def test_contract_controller_comprehensive(db_session):
    """Test all ContractController methods"""
    user = login("test_manager@epicevents.com", "test123")

    # Test all getter methods
    contracts = contract_controller.get_all_contracts(user)
    assert isinstance(contracts, list)

    unsigned = contract_controller.get_unsigned_contracts(user)
    assert isinstance(unsigned, list)

    unpaid = contract_controller.get_unpaid_contracts(user)
    assert isinstance(unpaid, list)

    # Test get_contract_by_id
    if contracts:
        contract = contract_controller.get_contract_by_id(contracts[0].id, user)
        assert contract is not None

    # Test update_contract
    if contracts:
        result = contract_controller.update_contract(contracts[0].id, user, is_signed=True)
        # Controller prints success


def test_event_controller_comprehensive(db_session):
    """Test all EventController methods"""
    user = login("test_manager@epicevents.com", "test123")

    # Test all getter methods
    events = event_controller.get_all_events(user)
    assert isinstance(events, list)

    no_support = event_controller.get_events_without_support(user)
    assert isinstance(no_support, list)

    my_events = event_controller.get_my_events(user)
    assert isinstance(my_events, list)

    # Test get_event_by_id
    if events:
        event = event_controller.get_event_by_id(events[0].id, user)
        assert event is not None

    # Test update_event
    if events:
        result = event_controller.update_event(events[0].id, user, notes="Test notes")
        # Controller prints success


def test_user_controller_comprehensive(db_session):
    """Test all UserController methods"""
    user = login("test_manager@epicevents.com", "test123")

    # Test get_all_users
    users = user_controller.get_all_users(user)
    assert isinstance(users, list)
    assert len(users) > 0

    # Test get_user_by_id
    if users:
        user_obj = user_controller.get_user_by_id(users[0].id, user)
        assert user_obj is not None

    # Test create_user (management only)
    result = user_controller.create_user("New User", "newuser@test.com", "password", "sales", user)
    # Controller prints success

    # Test update_user
    if users:
        result = user_controller.update_user(users[0].id, user, full_name="Updated Name")
        # Controller prints success
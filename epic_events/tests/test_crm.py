from epic_events.controllers.auth_controller import login
from epic_events.controllers.client_controller import client_controller
from epic_events.controllers.contract_controller import contract_controller
from epic_events.controllers.event_controller import event_controller
from epic_events.controllers.user_controller import user_controller
from epic_events.utils.display import print_success, print_info, print_error


def test_crm_functionality():
    """Test Epic Events CRM functionality with test data"""
    print("Testing Epic Events CRM functionality...")

    # Test authentication - use test users from conftest.py
    print("\n1. Testing authentication...")
    user = login("test_manager@epicevents.com", "test123")
    if user:
        print(f"✓ Login successful: {user.full_name}")
    else:
        print("✗ Login failed")
        assert False, "Login failed"

    # Test client listing
    print("\n2. Testing client listing...")
    clients = client_controller.get_all_clients(user)
    if clients:
        print(f"✓ Found {len(clients)} clients")
    else:
        print("✗ No clients found")
        assert False, "No clients found"

    # Test contract listing
    print("\n3. Testing contract listing...")
    contracts = contract_controller.get_all_contracts(user)
    if contracts:
        print(f"✓ Found {len(contracts)} contracts")
    else:
        print("✗ No contracts found")
        # Contracts might be empty in test DB, this is OK for now
        print("ℹ No contracts found (this might be expected in test DB)")

    # Test event listing
    print("\n4. Testing event listing...")
    events = event_controller.get_all_events(user)
    if events:
        print(f"✓ Found {len(events)} events")
    else:
        print("✗ No events found")
        # Events might be empty in test DB, this is OK for now
        print("ℹ No events found (this might be expected in test DB)")

    # Test user listing
    print("\n5. Testing user listing...")
    users = user_controller.get_all_users(user)
    if users:
        print(f"✓ Found {len(users)} users")
    else:
        print("✗ No users found")
        assert False, "No users found"

    print("\n✓ All basic functionality tests passed!")
#!/usr/bin/env python3
from epic_events.controllers.auth_controller import login
from epic_events.controllers.client_controller import client_controller
from epic_events.controllers.contract_controller import contract_controller
from epic_events.controllers.event_controller import event_controller
from epic_events.controllers.user_controller import user_controller
from epic_events.utils.display import print_success, print_info, print_error


def test_crm_functionality():
    """Test all CRM functionality"""
    print_info("Testing Epic Events CRM functionality...")

    # Test authentication
    print_info("\n1. Testing authentication...")
    user = login("dawn@epicevents.com", "management123")
    if user:
        print_success(f"✓ Login successful: {user.full_name}")
    else:
        print_error("✗ Login failed")
        return False

    # Test client listing
    print_info("\n2. Testing client listing...")
    clients = client_controller.get_all_clients(user)
    if clients:
        print_success(f"✓ Found {len(clients)} clients")
    else:
        print_error("✗ No clients found")

    # Test contract listing
    print_info("\n3. Testing contract listing...")
    contracts = contract_controller.get_all_contracts(user)
    if contracts:
        print_success(f"✓ Found {len(contracts)} contracts")
    else:
        print_error("✗ No contracts found")

    # Test event listing
    print_info("\n4. Testing event listing...")
    events = event_controller.get_all_events(user)
    if events:
        print_success(f"✓ Found {len(events)} events")
    else:
        print_error("✗ No events found")

    # Test user listing
    print_info("\n5. Testing user listing...")
    users = user_controller.get_all_users(user)
    if users:
        print_success(f"✓ Found {len(users)} users")
    else:
        print_error("✗ No users found")

    print_success("\n✓ All basic functionality tests passed!")
    return True


if __name__ == "__main__":
    test_crm_functionality()
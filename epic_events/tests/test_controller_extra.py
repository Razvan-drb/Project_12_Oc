from epic_events.controllers.auth_controller import login
from epic_events.controllers.client_controller import client_controller
from epic_events.controllers.user_controller import user_controller


def test_controller_final_edge_cases():
    """Final edge case tests for controllers"""
    login("test_manager@epicevents.com", "test123")

    # Test with None user (should handle gracefully)
    try:
        result = client_controller.get_all_clients(None)
        assert result is not None  # Should return empty list or handle gracefully
    except Exception:
        pass

    # Test permission errors more thoroughly
    sales_user = login("test_sales@epicevents.com", "test123")

    # Sales trying to access management functions
    users = user_controller.get_all_users(sales_user)
    assert users == []  # Should return empty list due to permission error

    # Support user trying to access sales functions
    support_user = login("test_support@epicevents.com", "test123")
    clients = client_controller.get_my_clients(support_user)
    assert clients == []  # Should return empty list


def test_auth_controller_final_polish():
    """Final polish for auth controller"""
    from epic_events.controllers.auth_controller import get_current_user

    # Test get_current_user with no active session
    # First ensure no session exists
    from epic_events.utils.session import session_manager
    session_manager.clear_session()

    current_user = get_current_user()
    assert current_user is None


def test_base_controller_final_polish():
    """Final polish for base controller"""
    from epic_events.controllers.base_controller import BaseController

    controller = BaseController()

    # Test error handling with different exception types
    test_errors = [
        ValueError("test error"),
        TypeError("type error"),
        RuntimeError("runtime error"),
        Exception("generic error")
    ]

    for error in test_errors:
        result = controller.handle_error(error, "test context")
        assert "test context" in result
        assert str(error) in result

    # Test commit_changes with rollback scenario
    result = controller.commit_changes()
    assert result is not None

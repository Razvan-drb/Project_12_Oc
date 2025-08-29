import pytest
from epic_events.controllers.base_controller import BaseController
from epic_events.controllers.auth_controller import login


def test_base_controller_functionality():
    """Test BaseController methods"""
    user = login("test_manager@epicevents.com", "test123")

    # Create controller instance
    controller = BaseController()

    # Test has_permission
    assert controller.has_permission(user, 'management') == True
    assert controller.has_permission(user, 'sales') == False
    assert controller.has_permission(user, 'support') == False

    # Test check_permission (should not raise for management)
    try:
        controller.check_permission(user, 'management')
        assert True  # Should not raise
    except PermissionError:
        assert False  # Should not raise for management

    # Test check_permission (should raise for sales when user is management)
    try:
        controller.check_permission(user, 'sales')
        assert False  # Should raise
    except PermissionError:
        assert True  # Expected to raise

    # Test handle_error
    error_msg = controller.handle_error(ValueError("Test error"), "test context")
    assert "Test error" in error_msg
    assert "test context" in error_msg

    # Test commit_changes (will rollback since we're in test)
    result = controller.commit_changes()
    assert result is not None  # Should return True or False
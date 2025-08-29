from epic_events.controllers.base_controller import BaseController
from epic_events.controllers.auth_controller import login


def test_base_controller_functionality():
    """Test BaseController methods"""
    user = login("test_manager@epicevents.com", "test123")

    # Create controller instance
    controller = BaseController()

    # Test has_permission
    assert controller.has_permission(user, 'management')
    assert not controller.has_permission(user, 'sales')
    assert not controller.has_permission(user, 'support')

    try:
        controller.check_permission(user, 'management')
        assert True
    except PermissionError:
        assert False

    try:
        controller.check_permission(user, 'sales')
        assert False
    except PermissionError:
        assert True

    # Test handle_error
    error_msg = controller.handle_error(ValueError("Test error"), "test context")
    assert "Test error" in error_msg
    assert "test context" in error_msg

    result = controller.commit_changes()
    assert result is not None

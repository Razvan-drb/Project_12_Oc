from epic_events.controllers.auth_controller import login, get_current_user


def test_successful_login(db_session):
    """Test successful authentication"""
    user = login("test_manager@epicevents.com", "test123")
    assert user is not None
    assert user.email == "test_manager@epicevents.com"
    assert user.department == "management"


def test_failed_login(db_session):
    """Test failed authentication"""
    user = login("nonexistent@test.com", "wrongpassword")
    assert user is None


def test_get_current_user(db_session):
    """Test getting current user from session"""
    # First login to create session
    user = login("test_manager@epicevents.com", "test123")
    assert user is not None

    # Test getting current user
    current_user = get_current_user()
    assert current_user is not None
    assert current_user.email == "test_manager@epicevents.com"

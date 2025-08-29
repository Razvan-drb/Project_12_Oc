import click
from epic_events.controllers.auth_controller import login as auth_login, logout, get_current_user
from epic_events.utils.display import print_success, print_error, print_info, print_warning


@click.group()
def auth_group():
    """Authentication commands"""
    pass


@auth_group.command()
@click.option('--email', prompt=True, help='User email')
@click.option('--password', prompt=True, hide_input=True, help='User password')
def login(email, password):
    """Authenticate user"""
    print(f"DEBUG: Email received: '{email}'")
    print(f"DEBUG: Password received: '{password}'")

    user = auth_login(email, password)  # Use the renamed import
    if user:
        print_success(f"Welcome, {user.full_name} ({user.department})!")
    else:
        print_error("Authentication failed!")


@auth_group.command(name='logout')
def logout_cmd():  # Also rename this to avoid potential conflicts
    """Logout current user"""
    logout()
    print_success("Logged out successfully")


@auth_group.command()
def status():
    """Show current authentication status"""
    user = get_current_user()
    if user:
        print_info(f"Logged in as: {user.full_name} ({user.department})")
    else:
        print_warning("Not authenticated")

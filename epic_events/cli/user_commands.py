import click
from epic_events.controllers.user_controller import user_controller
from epic_events.utils.display import display_table, print_info, print_error
from epic_events.controllers.auth_controller import require_auth


@click.group()
def user_group():
    """User management commands (management only)"""
    pass


@user_group.command(name='list')
@require_auth
def list_users(current_user):
    """List all users (management only)"""
    users = user_controller.get_all_users(current_user)
    if users is None:
        return

    if not users:
        print_info("No users found")
        return

    display_table(
        title="All Users",
        data=users,
        columns=['ID', 'Full Name', 'Email', 'Department', 'Created At']
    )


@user_group.command(name='create')
@click.option('--name', prompt='Full name', help='User full name')
@click.option('--email', prompt='Email', help='User email')
@click.option('--password', prompt='Password', hide_input=True, help='User password')
@click.option('--department', prompt='Department (management/sales/support)', help='User department')
@require_auth
def create_user(name, email, password, department, current_user):
    """Create a new user (management only)"""
    user_controller.create_user(name, email, password, department, current_user)


@user_group.command(name='view')
@click.argument('user_id', type=int)
@require_auth
def view_user(user_id, current_user):
    """View user details (management only)"""
    user = user_controller.get_user_by_id(user_id, current_user)
    if user is None:
        return

    display_table(
        title=f"User Details - {user.full_name}",
        data=[user],
        columns=['ID', 'Full Name', 'Email', 'Department', 'Created At', 'Updated At']
    )


@user_group.command(name='update')
@click.argument('user_id', type=int)
@click.option('--name', help='New full name')
@click.option('--email', help='New email')
@click.option('--password', help='New password')
@click.option('--department', help='New department')
@require_auth
def update_user(user_id, name, email, password, department, current_user):
    """Update user information (management only)"""
    update_data = {}
    if name:
        update_data['full_name'] = name
    if email:
        update_data['email'] = email
    if password:
        update_data['password'] = password
    if department:
        update_data['department'] = department

    if not update_data:
        print_error("No update data provided. Use options like --name, --email, etc.")
        return

    user_controller.update_user(user_id, current_user, **update_data)


@user_group.command(name='delete')
@click.argument('user_id', type=int)
@require_auth
def delete_user(user_id, current_user):
    """Delete a user (management only)"""
    user_controller.delete_user(user_id, current_user)

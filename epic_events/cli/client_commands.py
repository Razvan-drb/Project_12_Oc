import click
from epic_events.controllers.client_controller import client_controller
from epic_events.utils.permissions import has_sales_permission
from epic_events.utils.display import display_table, print_info, print_error
from epic_events.controllers.auth_controller import require_auth


@click.group()
def client_group():
    """Client management commands"""
    pass


@client_group.command(name='list')
@click.option('--mine', is_flag=True, help='Show only my clients')
@require_auth
def list_clients(mine, current_user):
    """List all clients or only my clients"""
    if mine:
        if not has_sales_permission(current_user):
            print_error("Only sales team can view 'my clients'")
            return
        clients = client_controller.get_my_clients(current_user)
        title = "My Clients"
    else:
        clients = client_controller.get_all_clients(current_user)
        title = "All Clients"

    if not clients:
        print_info("No clients found")
        return

    display_table(
        title=title,
        data=clients,
        columns=['ID', 'Full Name', 'Email', 'Company', 'Commercial Contact.Full Name', 'Created At']
    )


@client_group.command(name='create')
@click.option('--name', prompt='Client full name', help='Client full name')
@click.option('--email', prompt='Client email', help='Client email')
@click.option('--phone', prompt='Client phone', help='Client phone')
@click.option('--company', prompt='Client company', help='Client company name')
@require_auth
def create_client(name, email, phone, company, current_user):
    """Create a new client"""
    client_controller.create_client(name, email, phone, company, current_user)


@client_group.command(name='view')
@click.argument('client_id', type=int)
@require_auth
def view_client(client_id, current_user):
    """View client details"""
    client = client_controller.get_client_by_id(client_id, current_user)
    if client is None:
        return

    display_table(
        title=f"Client Details - {client.full_name}",
        data=[client],
        columns=['ID', 'Full Name', 'Email', 'Phone', 'Company', 'Commercial Contact.Full Name', 'Created At', 'Updated At']
    )


@client_group.command(name='update')
@click.argument('client_id', type=int)
@click.option('--name', help='New full name')
@click.option('--email', help='New email')
@click.option('--phone', help='New phone')
@click.option('--company', help='New company name')
@require_auth
def update_client(client_id, name, email, phone, company, current_user):
    """Update client information"""
    update_data = {}
    if name:
        update_data['full_name'] = name
    if email:
        update_data['email'] = email
    if phone:
        update_data['phone'] = phone
    if company:
        update_data['company_name'] = company

    if not update_data:
        print_error("No update data provided. Use options like --name, --email, etc.")
        return

    client_controller.update_client(client_id, current_user, **update_data)


@client_group.command(name='delete')
@click.argument('client_id', type=int)
@require_auth
def delete_client(client_id, current_user):
    """Delete a client (management only)"""
    client_controller.delete_client(client_id, current_user)

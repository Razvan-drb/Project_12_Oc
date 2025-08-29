import click
from epic_events.controllers.contract_controller import contract_controller
from epic_events.utils.permissions import has_sales_permission
from epic_events.utils.display import display_table, print_info, print_error
from epic_events.controllers.auth_controller import require_auth


@click.group()
def contract_group():
    """Contract management commands"""
    pass


@contract_group.command(name='create')
@click.option('--client-id', type=int, required=True, help='Client ID')
@click.option('--amount', type=float, required=True, help='Total contract amount')
@require_auth
def create_contract(client_id, amount, current_user):
    """Create a new contract (management only)"""
    contract_controller.create_contract(client_id, amount, current_user)


@contract_group.command(name='list')
@click.option('--unsigned', is_flag=True, help='Show only unsigned contracts')
@click.option('--unpaid', is_flag=True, help='Show only unpaid contracts')
@click.option('--mine', is_flag=True, help='Show only my contracts (sales)')
@require_auth
def list_contracts(unsigned, unpaid, mine, current_user):
    """List contracts with various filters"""
    if mine:
        if not has_sales_permission(current_user):
            print_error("Only sales team can view 'my contracts'")
            return
        contracts = contract_controller.get_my_contracts(current_user)
        title = "My Contracts"
    elif unsigned:
        contracts = contract_controller.get_unsigned_contracts(current_user)
        title = "Unsigned Contracts"
    elif unpaid:
        contracts = contract_controller.get_unpaid_contracts(current_user)
        title = "Unpaid Contracts"
    else:
        contracts = contract_controller.get_all_contracts(current_user)
        title = "All Contracts"

    if not contracts:
        print_info("No contracts found")
        return

    display_table(
        title=title,
        data=contracts,
        columns=['ID', 'Client.Full Name', 'Total Amount', 'Amount Due', 'Is Signed', 'Commercial Contact.Full Name',
                 'Created At']
    )


@contract_group.command(name='view')
@click.argument('contract_id', type=int)
@require_auth
def view_contract(contract_id, current_user):
    """View contract details"""
    contract = contract_controller.get_contract_by_id(contract_id, current_user)
    if contract is None:
        return

    display_table(
        title=f"Contract Details - ID {contract.id}",
        data=[contract],
        columns=['ID', 'Client.Full Name', 'Total Amount', 'Amount Due', 'Is Signed', 'Commercial Contact.Full Name',
                 'Created At']
    )


@contract_group.command(name='update')
@click.argument('contract_id', type=int)
@click.option('--amount', type=float, help='New total amount')
@click.option('--amount-due', type=float, help='New amount due')
@click.option('--signed/--unsigned', default=None, help='Mark contract as signed/unsigned')
@require_auth
def update_contract(contract_id, amount, amount_due, signed, current_user):
    """Update contract information"""
    update_data = {}
    if amount is not None:
        update_data['total_amount'] = amount
    if amount_due is not None:
        update_data['amount_due'] = amount_due
    if signed is not None:
        update_data['is_signed'] = signed

    if not update_data:
        print_error("No update data provided. Use options like --amount, --amount-due, etc.")
        return

    contract_controller.update_contract(contract_id, current_user, **update_data)

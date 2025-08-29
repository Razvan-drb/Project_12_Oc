from .base_controller import BaseController
from epic_events.models.contract import Contract
from epic_events.models.client import Client
from epic_events.utils.display import print_success, print_error
from epic_events.utils.permissions import can_access_client


class ContractController(BaseController):
    def create_contract(self, client_id, total_amount, current_user):
        """Create a new contract (management only)"""
        try:
            self.check_permission(current_user, 'management')

            # Check if client exists
            client = self.db.query(Client).filter(Client.id == client_id).first()
            if not client:
                return print_error("Client not found")

            # Create new contract
            new_contract = Contract(
                client_id=client_id,
                total_amount=total_amount,
                amount_due=total_amount,  # Initially, all amount is due
                is_signed=False,
                commercial_contact_id=client.commercial_contact_id
            )

            self.db.add(new_contract)
            if self.commit_changes():
                return print_success(f"Contract created successfully for client {client.full_name}")
            return print_error("Failed to create contract")

        except PermissionError as e:
            return print_error(str(e))
        except Exception as e:
            return print_error(self.handle_error(e, "creating contract"))

    def update_contract(self, contract_id, current_user, **kwargs):
        """Update contract information"""
        try:
            contract = self.db.query(Contract).filter(Contract.id == contract_id).first()
            if not contract:
                return print_error("Contract not found")

            # Check permissions
            if current_user.department == 'sales':
                # Sales can only update contracts for their clients
                if contract.client.commercial_contact_id != current_user.id:
                    return print_error("You can only update contracts for your clients")
                # Sales can only update certain fields
                allowed_fields = ['is_signed']
                for key in kwargs.keys():
                    if key not in allowed_fields:
                        return print_error(f"Sales team cannot update {key}")

            # Update fields
            for key, value in kwargs.items():
                if hasattr(contract, key) and value is not None:
                    setattr(contract, key, value)

            if self.commit_changes():
                return print_success("Contract updated successfully")
            return print_error("Failed to update contract")

        except Exception as e:
            return print_error(self.handle_error(e, "updating contract"))

    def get_all_contracts(self, current_user):
        """Get all contracts"""
        try:
            contracts = self.db.query(Contract).all()
            return contracts
        except Exception as e:
            print_error(self.handle_error(e, "fetching contracts"))
            return []

    def get_contract_by_id(self, contract_id, current_user):
        """Get specific contract by ID"""
        try:
            contract = self.db.query(Contract).filter(Contract.id == contract_id).first()
            if not contract:
                print_error("Contract not found")
                return None

            # Check if user has access to this client's data
            if not can_access_client(current_user, contract.client):
                print_error("Access denied to this contract")
                return None

            return contract
        except Exception as e:
            print_error(self.handle_error(e, "fetching contract"))
            return None

    def get_unsigned_contracts(self, current_user):
        """Get all unsigned contracts"""
        try:
            contracts = self.db.query(Contract).filter(Contract.is_signed.is_(False)).all()
            return contracts
        except Exception as e:
            print_error(self.handle_error(e, "fetching unsigned contracts"))
            return []

    def get_unpaid_contracts(self, current_user):
        """Get all contracts with amount due > 0"""
        try:
            contracts = self.db.query(Contract).filter(Contract.amount_due > 0).all()
            return contracts
        except Exception as e:
            print_error(self.handle_error(e, "fetching unpaid contracts"))
            return []

    def get_my_contracts(self, current_user):
        """Get contracts for current user's clients"""
        try:
            if not self.has_permission(current_user, 'sales'):
                print_error("Sales permission required")
                return []

            contracts = self.db.query(Contract).join(Client).filter(
                Client.commercial_contact_id == current_user.id
            ).all()
            return contracts
        except Exception as e:
            print_error(self.handle_error(e, "fetching user's contracts"))
            return []


# Create a global instance
contract_controller = ContractController()

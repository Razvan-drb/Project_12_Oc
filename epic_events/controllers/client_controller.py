from sqlalchemy.orm import Session
from sqlalchemy import or_
from .base_controller import BaseController
from epic_events.models.client import Client
from epic_events.models.user import User
from epic_events.utils.permissions import can_access_client
from epic_events.utils.display import print_success, print_error, print_warning


class ClientController(BaseController):
    def create_client(self, full_name, email, phone, company_name, current_user):
        """Create a new client (sales team only)"""
        try:
            self.check_permission(current_user, 'sales')

            # Check if client already exists
            existing_client = self.db.query(Client).filter(
                or_(Client.email == email, Client.phone == phone)
            ).first()

            if existing_client:
                return print_error(f"Client with email {email} or phone {phone} already exists")

            # Create new client
            new_client = Client(
                full_name=full_name,
                email=email,
                phone=phone,
                company_name=company_name,
                commercial_contact_id=current_user.id
            )

            self.db.add(new_client)
            if self.commit_changes():
                return print_success(f"Client {full_name} created successfully")
            return print_error("Failed to create client")

        except PermissionError as e:
            return print_error(str(e))
        except Exception as e:
            return print_error(self.handle_error(e, "creating client"))


    def update_client(self, client_id, current_user, **kwargs):
        """Update client information"""
        try:
            # Get the client
            client = self.db.query(Client).filter(Client.id == client_id).first()
            if not client:
                return print_error("Client not found")

            # Check permissions - sales can only update their own clients
            if current_user.department == 'sales' and client.commercial_contact_id != current_user.id:
                return print_error("You can only update your own clients")

            # Update fields
            for key, value in kwargs.items():
                if hasattr(client, key) and value is not None:
                    setattr(client, key, value)

            if self.commit_changes():
                return print_success(f"Client {client.full_name} updated successfully")
            return print_error("Failed to update client")

        except Exception as e:
            return print_error(self.handle_error(e, "updating client"))


    def get_all_clients(self, current_user):
        """Get all clients (read-only access for all)"""
        try:
            clients = self.db.query(Client).all()
            return clients
        except Exception as e:
            print_error(self.handle_error(e, "fetching clients"))
            return []


    def get_client_by_id(self, client_id, current_user):
        """Get specific client by ID with permission check"""
        try:
            client = self.db.query(Client).filter(Client.id == client_id).first()
            if not client:
                print_error("Client not found")
                return None

            if not can_access_client(current_user, client):
                print_error("Access denied to this client")
                return None

            return client
        except Exception as e:
            print_error(self.handle_error(e, "fetching client"))
            return None

    def get_my_clients(self, current_user):
        """Get clients assigned to current sales user"""
        try:
            if not self.has_permission(current_user, 'sales'):
                print_error("Sales permission required")
                return []

            clients = self.db.query(Client).filter(
                Client.commercial_contact_id == current_user.id
            ).all()
            return clients
        except Exception as e:
            print_error(self.handle_error(e, "fetching user's clients"))
            return []

    def delete_client(self, client_id, current_user):
        """Delete a client (management only)"""
        try:
            self.check_permission(current_user, 'management')

            client = self.db.query(Client).filter(Client.id == client_id).first()
            if not client:
                return print_error("Client not found")

            # Check if client has contracts or events
            if client.contracts or client.events:
                return print_error("Cannot delete client with existing contracts or events")

            self.db.delete(client)
            if self.commit_changes():
                return print_success(f"Client {client.full_name} deleted successfully")
            return print_error("Failed to delete client")

        except PermissionError as e:
            return print_error(str(e))
        except Exception as e:
            return print_error(self.handle_error(e, "deleting client"))


# Create a global instance
client_controller = ClientController()
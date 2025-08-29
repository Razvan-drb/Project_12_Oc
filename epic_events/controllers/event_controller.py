from .base_controller import BaseController
from epic_events.models.event import Event
from epic_events.models.contract import Contract
from epic_events.models.client import Client
from epic_events.models.user import User
from epic_events.utils.display import print_success, print_error
from epic_events.utils.permissions import can_access_client


class EventController(BaseController):
    def create_event(self, contract_id, name, start_date, end_date, location, attendees, notes, current_user):
        """Create a new event (sales team only)"""
        try:
            self.check_permission(current_user, 'sales')

            # Check if contract exists and is signed
            contract = self.db.query(Contract).filter(Contract.id == contract_id).first()
            if not contract:
                return print_error("Contract not found")

            if not contract.is_signed:
                return print_error("Cannot create event for unsigned contract")

            # Check if user has access to this client
            if not can_access_client(current_user, contract.client):
                return print_error("Access denied to this client's contracts")

            # Create new event
            new_event = Event(
                contract_id=contract_id,
                client_id=contract.client_id,
                name=name,
                start_date=start_date,
                end_date=end_date,
                location=location,
                attendees=attendees,
                notes=notes,
                support_contact_id=None  # Initially no support contact assigned
            )

            self.db.add(new_event)
            if self.commit_changes():
                return print_success(f"Event '{name}' created successfully")
            return print_error("Failed to create event")

        except PermissionError as e:
            return print_error(str(e))
        except Exception as e:
            return print_error(self.handle_error(e, "creating event"))

    def update_event(self, event_id, current_user, **kwargs):
        """Update event information"""
        try:
            event = self.db.query(Event).filter(Event.id == event_id).first()
            if not event:
                return print_error("Event not found")

            # Check permissions based on department
            if current_user.department == 'sales':
                # Sales can only update events for their clients
                if event.client.commercial_contact_id != current_user.id:
                    return print_error("You can only update events for your clients")
                # Sales can only update certain fields
                allowed_fields = ['name', 'start_date', 'end_date', 'location', 'attendees', 'notes']
                for key in kwargs.keys():
                    if key not in allowed_fields:
                        return print_error(f"Sales team cannot update {key}")

            elif current_user.department == 'support':
                # Support can only update events assigned to them
                if event.support_contact_id != current_user.id:
                    return print_error("You can only update events assigned to you")
                # Support can only update certain fields
                allowed_fields = ['notes']
                for key in kwargs.keys():
                    if key not in allowed_fields:
                        return print_error(f"Support team cannot update {key}")

            # Update fields
            for key, value in kwargs.items():
                if hasattr(event, key) and value is not None:
                    setattr(event, key, value)

            if self.commit_changes():
                return print_success("Event updated successfully")
            return print_error("Failed to update event")

        except Exception as e:
            return print_error(self.handle_error(e, "updating event"))

    def assign_support_contact(self, event_id, support_contact_id, current_user):
        """Assign support contact to event (management only)"""
        try:
            self.check_permission(current_user, 'management')

            event = self.db.query(Event).filter(Event.id == event_id).first()
            if not event:
                return print_error("Event not found")

            # Check if support contact exists and is in support department
            support_contact = self.db.query(User).filter(
                User.id == support_contact_id,
                User.department == 'support'
            ).first()

            if not support_contact:
                return print_error("Invalid support contact ID or user is not in support department")

            event.support_contact_id = support_contact_id
            if self.commit_changes():
                return print_success(f"Support contact {support_contact.full_name} assigned to event")
            return print_error("Failed to assign support contact")

        except PermissionError as e:
            return print_error(str(e))
        except Exception as e:
            return print_error(self.handle_error(e, "assigning support contact"))

    def get_all_events(self, current_user):
        """Get all events"""
        try:
            events = self.db.query(Event).all()
            return events
        except Exception as e:
            print_error(self.handle_error(e, "fetching events"))
            return []

    def get_event_by_id(self, event_id, current_user):
        """Get specific event by ID"""
        try:
            event = self.db.query(Event).filter(Event.id == event_id).first()
            if not event:
                print_error("Event not found")
                return None

            # Check if user has access to this client's data
            if not can_access_client(current_user, event.client):
                print_error("Access denied to this event")
                return None

            return event
        except Exception as e:
            print_error(self.handle_error(e, "fetching event"))
            return None

    def get_events_without_support(self, current_user):
        """Get all events without support contact assigned"""
        try:
            events = self.db.query(Event).filter(Event.support_contact_id.is_(None)).all()
            return events
        except Exception as e:
            print_error(self.handle_error(e, "fetching events without support"))
            return []

    def get_my_events(self, current_user):
        """Get events assigned to current user"""
        try:
            if current_user.department == 'support':
                events = self.db.query(Event).filter(Event.support_contact_id == current_user.id).all()
            elif current_user.department == 'sales':
                events = self.db.query(Event).join(Client).filter(
                    Client.commercial_contact_id == current_user.id
                ).all()
            else:
                events = self.get_all_events(current_user)

            return events
        except Exception as e:
            print_error(self.handle_error(e, "fetching user's events"))
            return []


# Create a global instance
event_controller = EventController()

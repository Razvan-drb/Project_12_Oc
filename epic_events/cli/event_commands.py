import click
from datetime import datetime
from epic_events.controllers.event_controller import event_controller
from epic_events.utils.display import display_table, print_info, print_error
from epic_events.controllers.auth_controller import require_auth


@click.group()
def event_group():
    """Event management commands"""
    pass


@event_group.command(name='create')
@click.option('--contract-id', type=int, required=True, help='Contract ID')
@click.option('--name', required=True, help='Event name')
@click.option('--start-date', required=True, help='Start date (YYYY-MM-DD HH:MM)')
@click.option('--end-date', required=True, help='End date (YYYY-MM-DD HH:MM)')
@click.option('--location', required=True, help='Event location')
@click.option('--attendees', type=int, required=True, help='Number of attendees')
@click.option('--notes', help='Event notes')
@require_auth
def create_event(contract_id, name, start_date, end_date, location, attendees, notes, current_user):
    """Create a new event (sales only)"""
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
        end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M')
    except ValueError:
        print_error("Invalid date format. Use: YYYY-MM-DD HH:MM")
        return

    event_controller.create_event(contract_id, name, start_date, end_date, location, attendees, notes, current_user)


@event_group.command(name='list')
@click.option('--no-support', is_flag=True, help='Show events without support contact')
@click.option('--mine', is_flag=True, help='Show only my events')
@require_auth
def list_events(no_support, mine, current_user):
    """List events with various filters"""
    if no_support:
        events = event_controller.get_events_without_support(current_user)
        title = "Events Without Support"
    elif mine:
        events = event_controller.get_my_events(current_user)
        title = "My Events"
    else:
        events = event_controller.get_all_events(current_user)
        title = "All Events"

    if not events:
        print_info("No events found")
        return

    display_table(
        title=title,
        data=events,
        columns=['ID', 'Name', 'Client.Full Name', 'Start Date', 'End Date', 'Location', 'Support Contact.Full Name',
                 'Attendees']
    )


@event_group.command(name='view')
@click.argument('event_id', type=int)
@require_auth
def view_event(event_id, current_user):
    """View event details"""
    event = event_controller.get_event_by_id(event_id, current_user)
    if event is None:
        return

    display_table(
        title=f"Event Details - {event.name}",
        data=[event],
        columns=['ID', 'Name', 'Client.Full Name', 'Start Date', 'End Date', 'Location', 'Support Contact.Full Name',
                 'Attendees', 'Notes', 'Created At']
    )


@event_group.command(name='update')
@click.argument('event_id', type=int)
@click.option('--name', help='New event name')
@click.option('--start-date', help='New start date (YYYY-MM-DD HH:MM)')
@click.option('--end-date', help='New end date (YYYY-MM-DD HH:MM)')
@click.option('--location', help='New location')
@click.option('--attendees', type=int, help='New number of attendees')
@click.option('--notes', help='New notes')
@require_auth
def update_event(event_id, name, start_date, end_date, location, attendees, notes, current_user):
    """Update event information"""
    update_data = {}

    if name:
        update_data['name'] = name
    if start_date:
        try:
            update_data['start_date'] = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
        except ValueError:
            print_error("Invalid start date format. Use: YYYY-MM-DD HH:MM")
            return
    if end_date:
        try:
            update_data['end_date'] = datetime.strptime(end_date, '%Y-%m-%d %H:%M')
        except ValueError:
            print_error("Invalid end date format. Use: YYYY-MM-DD HH:MM")
            return
    if location:
        update_data['location'] = location
    if attendees is not None:
        update_data['attendees'] = attendees
    if notes is not None:
        update_data['notes'] = notes

    if not update_data:
        print_error("No update data provided. Use options like --name, --start-date, etc.")
        return

    event_controller.update_event(event_id, current_user, **update_data)


@event_group.command(name='assign-support')
@click.argument('event_id', type=int)
@click.option('--support-id', type=int, required=True, help='Support user ID')
@require_auth
def assign_support(event_id, support_id, current_user):
    """Assign support contact to event (management only)"""
    event_controller.assign_support_contact(event_id, support_id, current_user)

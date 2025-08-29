from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def display_table(title, data, columns):
    """Display data in a formatted table"""
    if not data:
        console.print(f"[yellow]No {title.lower()} found[/yellow]")
        return

    table = Table(title=title, box=box.ROUNDED)

    # Add columns
    for column in columns:
        table.add_column(column, style="cyan")

    # Add rows
    for item in data:
        row_data = []
        for column in columns:
            # Handle nested attributes (e.g., client.commercial_contact.full_name)
            value = item
            for attr in column.lower().split('.'):
                if hasattr(value, attr):
                    value = getattr(value, attr)
                else:
                    value = "N/A"
                    break
            row_data.append(str(value) if value else "None")

        table.add_row(*row_data)

    console.print(table)


def print_success(message):
    """Print success message"""
    console.print(f"[green]✓ {message}[/green]")


def print_error(message):
    """Print error message"""
    console.print(f"[red]✗ {message}[/red]")


def print_warning(message):
    """Print warning message"""
    console.print(f"[yellow]! {message}[/yellow]")


def print_info(message):
    """Print info message"""
    console.print(f"[blue]ℹ {message}[/blue]")

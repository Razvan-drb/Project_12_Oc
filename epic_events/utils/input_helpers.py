from rich.prompt import Prompt, Confirm

from epic_events.utils.display import print_error


def get_required_input(prompt_text, field_name):
    """Get required input with validation"""
    while True:
        value = Prompt.ask(f"[cyan]{prompt_text}[/cyan]")
        if value.strip():
            return value.strip()
        print_error(f"{field_name} is required")


def get_email_input(prompt_text):
    """Get email input with basic validation"""
    while True:
        email = Prompt.ask(f"[cyan]{prompt_text}[/cyan]")
        if '@' in email and '.' in email:
            return email.strip()
        print_error("Please enter a valid email address")


def get_phone_input(prompt_text):
    """Get phone input"""
    phone = Prompt.ask(f"[cyan]{prompt_text}[/cyan]")
    return phone.strip()


def get_choice_input(prompt_text, choices):
    """Get choice from list of options"""
    return Prompt.ask(
        f"[cyan]{prompt_text}[/cyan]",
        choices=choices,
        default=choices[0]
    )


def confirm_action(message):
    """Confirm an action"""
    return Confirm.ask(f"[yellow]{message}[/yellow]")

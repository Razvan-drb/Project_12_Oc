#!/usr/bin/env python3
import click
import sentry_sdk
from config import Config
from epic_events.cli import auth_commands, client_commands, contract_commands, event_commands, user_commands

# Initialize Sentry only if DSN is provided
if Config.SENTRY_DSN and Config.SENTRY_DSN.strip():
    try:
        sentry_sdk.init(
            dsn=Config.SENTRY_DSN,
            traces_sample_rate=1.0,
        )
        print("Sentry initialized successfully")
    except Exception as e:
        print(f"Failed to initialize Sentry: {e}")
else:
    print("Sentry not configured - running without error monitoring")

@click.group()
def cli():
    """Epic Events CRM - Command Line Interface"""
    pass

# Add all command groups
cli.add_command(auth_commands.auth_commands, name='auth')
cli.add_command(client_commands.client_commands, name='clients')
cli.add_command(contract_commands.contract_commands, name='contracts')
cli.add_command(event_commands.event_commands, name='events')
cli.add_command(user_commands.user_commands, name='users')

if __name__ == '__main__':
    cli()
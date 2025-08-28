#!/usr/bin/env python3
import click
import sentry_sdk
from config import Config
from epic_events.cli import auth_group, client_group, contract_group, event_group, user_group

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
cli.add_command(auth_group, name='auth')
cli.add_command(client_group, name='clients')
cli.add_command(contract_group, name='contracts')
cli.add_command(event_group, name='events')
cli.add_command(user_group, name='users')

if __name__ == '__main__':
    cli()
import pytest
from click.testing import CliRunner
from main import cli


def test_cli_auth_login():
    """Test CLI auth login command"""
    runner = CliRunner()

    # Test with prompts
    result = runner.invoke(cli, ['auth', 'login'], input='test_manager@epicevents.com\ntest123\n')
    assert result.exit_code == 0
    assert "Welcome" in result.output


def test_cli_client_list():
    """Test CLI clients list command"""
    runner = CliRunner()

    # First login, then list clients
    result = runner.invoke(cli, ['auth', 'login', '--email', 'test_manager@epicevents.com', '--password', 'test123'])
    assert result.exit_code == 0

    result = runner.invoke(cli, ['clients', 'list'])
    assert result.exit_code == 0
    assert "Clients" in result.output
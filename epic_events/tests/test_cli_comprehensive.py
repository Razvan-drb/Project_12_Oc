import pytest
from click.testing import CliRunner


def test_cli_comprehensive():
    """Test comprehensive CLI functionality"""
    from main import cli
    runner = CliRunner()

    # Test auth commands
    result = runner.invoke(cli, ['auth', 'login', '--email', 'test_manager@epicevents.com', '--password', 'test123'])
    assert result.exit_code == 0

    result = runner.invoke(cli, ['auth', 'status'])
    assert result.exit_code == 0

    # Test clients commands
    result = runner.invoke(cli, ['clients', 'list'])
    assert result.exit_code == 0

    # Test contracts commands
    result = runner.invoke(cli, ['contracts', 'list'])
    assert result.exit_code == 0

    # Test events commands
    result = runner.invoke(cli, ['events', 'list'])
    assert result.exit_code == 0

    # Test users commands (management only)
    result = runner.invoke(cli, ['users', 'list'])
    assert result.exit_code == 0

    # Test logout
    result = runner.invoke(cli, ['auth', 'logout'])
    assert result.exit_code == 0
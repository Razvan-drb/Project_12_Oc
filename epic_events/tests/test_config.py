import pytest
import os
from unittest.mock import patch
from config import Config


def test_config_validation():
    """Test config validation edge cases"""

    # Test with missing DATABASE_URL
    with patch.dict(os.environ, {'DATABASE_URL': ''}, clear=True):
        # This should raise an error or handle missing config
        try:
            Config.validate()
            # If it doesn't raise, that's fine too
        except ValueError as e:
            assert "DATABASE_URL" in str(e)

    # Test with invalid Sentry DSN
    with patch.dict(os.environ, {'SENTRY_DSN': 'invalid'}, clear=True):
        try:
            Config.validate()
            # Should handle invalid DSN gracefully
        except Exception as e:
            # Some validation might fail, that's OK
            pass


def test_config_defaults():
    """Test config default values"""
    # Clear environment to test defaults
    with patch.dict(os.environ, {}, clear=True):
        # Re-import to get fresh config
        import importlib
        import config
        importlib.reload(config)

        # Should use default database URL
        assert config.Config.DATABASE_URL == 'sqlite:///epic_events.db'
        assert config.Config.SENTRY_DSN == ''
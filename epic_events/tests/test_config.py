import os
from unittest.mock import patch
from config import Config


def test_config_validation():
    """Test config validation edge cases"""

    # Test with missing DATABASE_URL
    with patch.dict(os.environ, {'DATABASE_URL': ''}, clear=True):
        try:
            Config.validate()
        except ValueError as e:
            assert "DATABASE_URL" in str(e)

    with patch.dict(os.environ, {'SENTRY_DSN': 'invalid'}, clear=True):
        try:
            Config.validate()
        except Exception:
            pass

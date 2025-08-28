import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///epic_events.db')
    SENTRY_DSN = os.getenv('SENTRY_DSN', '')

    @classmethod
    def validate(cls):
        """Validate that required environment variables are set"""
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is required")

        # Sentry DSN is optional for development
        if not cls.SENTRY_DSN:
            print("Warning: SENTRY_DSN not set. Error logging will be limited to console.")


# Validate configuration on import
Config.validate()
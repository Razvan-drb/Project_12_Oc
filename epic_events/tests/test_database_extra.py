import pytest
from epic_events.utils.database import get_db, init_db


def test_database_final_coverage():
    """Final tests for database utilities"""

    # Test init_db multiple times (should be idempotent)
    init_db()
    init_db()  # Should work without errors

    # Test get_db generator behavior
    db_gen = get_db()
    db1 = next(db_gen)
    assert db1 is not None

    # Test that generator completes
    try:
        next(db_gen)  # Should raise StopIteration
        assert False, "Generator should have completed"
    except StopIteration:
        pass  # Expected behavior

    # Test multiple get_db calls
    db_gen2 = get_db()
    db2 = next(db_gen2)
    assert db2 is not None
    try:
        next(db_gen2)
    except StopIteration:
        pass
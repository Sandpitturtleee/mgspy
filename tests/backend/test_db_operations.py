import datetime

import pytest

from backend.db_operations import DbOperations
from tests.data.data import player_profiles_test_db, player_activity_test_db

DB_NAME_TEST = "mgspy_test"


@pytest.fixture(scope="module")
def db():
    """Setup and teardown a database connection for the test session."""
    db_ops = DbOperations(db_name=DB_NAME_TEST)
    conn = db_ops.connect_to_db()
    yield db_ops, conn
    conn.close()


@pytest.fixture(autouse=True)
def cleanup_tables(db):
    """Cleanup tables before each test."""
    db_ops, conn = db
    db_ops.delete_data(conn, 'activity_data')
    db_ops.delete_data(conn, 'profile_data')
    yield


def test_insert_and_select_activity_data(db):
    db_ops, conn = db
    activity = player_activity_test_db
    db_ops.insert_activity_data(conn, activity)
    rows = db_ops.select_data(conn, "activity_data")
    assert len(rows) == len(activity)
    assert rows[0][0:3] == (7667949, 155201, datetime.datetime(2025, 1, 1, 12, 0))
    assert rows[len(rows) - 1][:3] == (9519329, 247700, datetime.datetime(2025, 1, 1, 12, 0))


def test_delete_activity_data(db):
    db_ops, conn = db
    activity = player_activity_test_db
    db_ops.insert_activity_data(conn, activity)
    db_ops.delete_data(conn, "activity_data", "profile = 7667949")
    db_ops.delete_data(conn, "activity_data", "profile = 9519329")
    rows = db_ops.select_data(conn, "activity_data")
    assert len(rows) == len(activity) - 2
    assert rows[0][0:3] != (7667949, 155201, datetime.datetime(2025, 1, 1, 12, 0))
    assert rows[len(rows) - 1][:3] != (9519329, 247700, datetime.datetime(2025, 1, 1, 12, 0))


def test_insert_and_select_profile_data(db):
    db_ops, conn = db
    profiles = player_profiles_test_db
    db_ops.insert_profile_data(conn, profiles)
    rows = db_ops.select_data(conn, "profile_data")
    assert len(rows) == len(profiles)
    assert rows[0][:6] == (5111553, 155755, 'Charmed', 129, 'None', '#berufs')
    assert rows[len(rows) - 1][:6] == (973998, 68470, 'łelełęłęłeł', 64, 'None', '#berufs')


def test_delete_profile_data(db):
    db_ops, conn = db
    profiles = player_profiles_test_db
    db_ops.insert_profile_data(conn, profiles)
    db_ops.delete_data(conn, "profile_data", "profile = 5111553")
    rows = db_ops.select_data(conn, "profile_data")
    assert len(rows) == 7


def test_select_data_with_where_clause(db):
    db_ops, conn = db
    profiles = player_profiles_test_db
    db_ops.insert_profile_data(conn, profiles)
    rows = db_ops.select_data(
        conn,
        table="profile_data",
        where_clause="profile = 5111553",
    )
    assert rows[0][:6] == (5111553, 155755, 'Charmed', 129, 'None', '#berufs')

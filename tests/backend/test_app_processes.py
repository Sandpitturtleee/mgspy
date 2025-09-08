import threading
import time
import pytest

from backend.app_processes import AppProcesses
from backend.db_operations import DbOperations
from tests.data.data import player_activity_test, player_activity_test_short

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


@pytest.fixture
def app_processes():
    app_processes = AppProcesses(db_name="mgspy_test")
    app_processes.scrap_player_activity_interval = 5  # Fast for test
    app_processes.save_player_activity_interval = 10
    app_processes.app_run_time = 21
    return app_processes


def test_scrap_player_activity(app_processes):
    collected_activity = []
    control_event = threading.Event()

    thread = threading.Thread(
        target=app_processes.scrap_player_activity,
        args=(collected_activity, control_event)
    )
    thread.start()

    time.sleep(10)
    control_event.set()
    thread.join(timeout=2)

    assert isinstance(collected_activity, list)
    assert len(collected_activity) >= 1
    entry = collected_activity[0]
    assert isinstance(entry, dict)
    for key in ("profile", "char", "datetime"):
        assert key in entry


def test_save_player_activity(app_processes, db):
    db_ops, conn = db

    collected_activity = player_activity_test
    control_event = threading.Event()

    thread = threading.Thread(
        target=app_processes.save_player_activity,
        args=(collected_activity, control_event)
    )
    thread.start()

    time.sleep(20)
    control_event.set()
    thread.join(timeout=2)

    activities = db_ops.select_data(conn, 'activity_data')
    assert len(activities) >= 1
    assert len(activities) == 55
    assert collected_activity == []

    first_row = activities[0]
    last_row = activities[len(activities) - 1]
    assert first_row[0] == 7667949
    assert first_row[1] == 155201
    assert str(first_row[2]).startswith("2025-01-01")
    assert last_row[0] == 9519329
    assert last_row[1] == 247700
    assert str(last_row[2]).startswith("2025-01-01")


def test_scrap_and_save_profile_data(app_processes, db):
    db_ops, conn = db

    collected_activity = player_activity_test_short
    db_ops.insert_activity_data(
        db_connection=conn, player_activity=collected_activity
    )

    app_processes.scrap_and_save_profile_data()

    results_activity = db_ops.select_data(conn, 'activity_data')
    results_profiles = db_ops.select_data(conn, 'profile_data')

    # Create set of (profile, char) in activity_data
    activity_pairs = {(row[0], row[1]) for row in results_activity}
    profile_pairs = {(row[0], row[1]) for row in results_profiles}

    # Each pair in activity_data is present in profile_data
    assert activity_pairs <= profile_pairs, (
        f"Missing profile/char pairs: {activity_pairs - profile_pairs}"
    )


def test_process_app(app_processes, db):
    db_ops, conn = db

    app_processes.process_app()
    time.sleep(1)
    results_activity = db_ops.select_data(conn, 'activity_data')

    assert len(results_activity) >= 1

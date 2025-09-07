import pytest
import psycopg2
from psycopg2.extensions import connection
from backend.db_operations import DbOperations  # <-- Replace with actual module path


@pytest.fixture
def db_ops():
    return DbOperations()


def make_fake_cursor(mocker, rowcount=3, fetch_result=None):
    mock_cursor = mocker.MagicMock()
    mock_cursor.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = fetch_result or []
    mock_cursor.rowcount = rowcount
    return mock_cursor


def make_fake_conn(mocker, cursor=None):
    mock_conn = mocker.MagicMock()
    mock_conn.cursor.return_value = cursor if cursor else make_fake_cursor(mocker)
    return mock_conn


def test_connect_to_db_success(mocker, db_ops):
    fake_conn = "CONN"
    mocker.patch('psycopg2.connect', return_value=fake_conn)
    conn = db_ops.connect_to_db(max_retries=1)
    assert conn == fake_conn


def test_connect_to_db_retries_and_fails(mocker, db_ops):
    mocker.patch('psycopg2.connect', side_effect=psycopg2.OperationalError)
    with pytest.raises(Exception, match="Database not available after retries!"):
        db_ops.connect_to_db(max_retries=2, delay=0)


def test_insert_activity_data(mocker, db_ops):
    fake_conn = make_fake_conn(mocker)
    player_activity = [
        {"profile": 5111553, "char": 155755, "datetime": "2025-01-01 12:00:00"},
        {"profile": 973998, "char": 116256, "datetime": "2025-01-01 12:00:00"},
    ]
    db_ops.insert_activity_data(fake_conn, player_activity)
    assert fake_conn.cursor.return_value.execute.call_count == len(player_activity)
    fake_conn.commit.assert_called_once()


def test_insert_profile_data(mocker, db_ops):
    fake_conn = make_fake_conn(mocker)
    profile_data = [
        {'profile': '5111553', 'char': '155755', 'nick': 'Charmed', 'lvl': '129', 'world': '#berufs'},
        {'profile': '973998', 'char': '116256', 'nick': 'Brovvar', 'lvl': '64', 'world': '#berufs'},
    ]
    db_ops.insert_profile_data(fake_conn, profile_data)
    assert fake_conn.cursor.return_value.execute.call_count == len(profile_data)
    fake_conn.commit.assert_called_once()


def test_select_data(mocker, db_ops):
    fake_cursor = make_fake_cursor(mocker, fetch_result=[(1, 2), (3, 4)])
    fake_conn = make_fake_conn(mocker, cursor=fake_cursor)
    out = db_ops.select_data(fake_conn, 'table', columns='a,b')
    assert out == [(1, 2), (3, 4)]


def test_select_data_with_where(mocker, db_ops):
    fake_cursor = make_fake_cursor(mocker, fetch_result=[(1,)])
    fake_conn = make_fake_conn(mocker, cursor=fake_cursor)
    out = db_ops.select_data(fake_conn, 'test', columns='a', where_clause='id=%s', params=(10,))
    fake_conn.cursor.return_value.execute.assert_called_with('SELECT a FROM test WHERE id=%s', (10,))
    assert out == [(1,)]


def test_delete_data(mocker, db_ops):
    fake_cursor = make_fake_cursor(mocker, rowcount=2)
    fake_conn = make_fake_conn(mocker, cursor=fake_cursor)
    db_ops.delete_data(fake_conn, 'foo', where_clause='id=%s', params=(1,))
    fake_conn.cursor.return_value.execute.assert_called_with('DELETE FROM foo WHERE id=%s', (1,))
    fake_conn.commit.assert_called_once()


def test_delete_data_no_where(mocker, db_ops):
    fake_cursor = make_fake_cursor(mocker, rowcount=3)
    fake_conn = make_fake_conn(mocker, cursor=fake_cursor)
    db_ops.delete_data(fake_conn, 'bar')
    fake_conn.cursor.return_value.execute.assert_called_with('DELETE FROM bar', None)
    fake_conn.commit.assert_called_once()

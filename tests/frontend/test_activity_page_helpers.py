import pytest
from datetime import datetime, timedelta
import io
import matplotlib.pyplot as plt

from frontend.activity_page_helpers import ActivityPageHelpers


@pytest.fixture
def profile_char():
    # Example returned row for profile & char based on nick.
    return [('5111553', '155755')]


@pytest.fixture
def activity_data():
    # Example activity: 3 time points in one hour.
    base = datetime(2023, 1, 1, 12, 0, 0)
    return [
        ('5111553', '155755', base),
        ('5111553', '155755', base + timedelta(minutes=13)),
        ('5111553', '155755', base + timedelta(minutes=42)),
    ]


@pytest.fixture
def helpers_and_db(mocker):
    mock_db_cls = mocker.patch('frontend.activity_page_helpers.DbOperations', autospec=True)
    mock_db_instance = mock_db_cls.return_value
    mock_db_instance.connect_to_db.return_value = 'mock_conn'
    helpers = ActivityPageHelpers()
    mock_db_instance.select_data.reset_mock()
    return helpers, mock_db_instance


def test_get_player_activity_found(helpers_and_db, profile_char, activity_data):
    helpers, db = helpers_and_db
    db.select_data.side_effect = [profile_char, activity_data]
    nick = "Sold"
    start_date = datetime(2023, 1, 1, 12, 0, 0)
    result = helpers.get_player_activity(nick, start_date)
    assert result == [dt for _, _, dt in activity_data]
    assert helpers.start_date == start_date
    assert helpers.end_date == start_date + timedelta(hours=1)
    assert db.select_data.call_count == 2


def test_get_player_activity_not_found(helpers_and_db):
    helpers, db = helpers_and_db
    db.select_data.side_effect = [None]
    result = helpers.get_player_activity("TEST", datetime.now())
    assert result is None


def test_generate_intervals(helpers_and_db):
    helpers, db = helpers_and_db
    helpers.start_date = datetime(2025, 1, 1, 12, 0, 0)
    helpers.end_date = datetime(2025, 1, 1, 12, 5, 0)
    helpers.interval_minutes = 1
    intervals = helpers.generate_intervals()
    assert intervals == [
        datetime(2025, 1, 1, 12, 0),
        datetime(2025, 1, 1, 12, 1),
        datetime(2025, 1, 1, 12, 2),
        datetime(2025, 1, 1, 12, 3),
        datetime(2025, 1, 1, 12, 4),
        datetime(2025, 1, 1, 12, 5)
    ]


def test_activity_presence_array():
    intervals = [
        datetime(2025, 1, 1, 12, 0),
        datetime(2025, 1, 1, 12, 10),
        datetime(2025, 1, 1, 12, 20)
    ]
    timestamps = [
        datetime(2025, 1, 1, 12, 5),
        datetime(2025, 1, 1, 12, 15),
    ]
    arr = ActivityPageHelpers.activity_presence_array(intervals, timestamps)
    assert arr == [1, 1]


def test_plot_player_activity_calls_render(helpers_and_db, mocker, activity_data):
    helpers, db = helpers_and_db
    helpers.start_date = datetime(2023, 1, 1, 12, 0, 0)
    helpers.end_date = helpers.start_date + timedelta(hours=1)
    intervals = [helpers.start_date + timedelta(minutes=i) for i in range(0, 61, 20)]
    mocker.patch.object(helpers, "generate_intervals", return_value=intervals)
    mocker.patch.object(helpers, "activity_presence_array", return_value=[1, 0, 1])
    mock_render = mocker.patch.object(helpers, "render_bar_chart")
    helpers.plot_player_activity([dt for _, _, dt in activity_data])
    mock_render.assert_called_once()


def test_gui_plot_player_activity_calls_render_to_bytesio(helpers_and_db, mocker, activity_data):
    helpers, db = helpers_and_db
    helpers.start_date = datetime(2023, 1, 1, 12, 0, 0)
    helpers.end_date = helpers.start_date + timedelta(hours=1)
    intervals = [helpers.start_date + timedelta(minutes=i) for i in range(0, 61, 20)]
    mocker.patch.object(helpers, "generate_intervals", return_value=intervals)
    mocker.patch.object(helpers, "activity_presence_array", return_value=[0, 1, 1])
    mock_render = mocker.patch.object(helpers, "render_bar_chart_to_bytesio", return_value="png_img_obj")
    ret = helpers.gui_plot_player_activity([dt for _, _, dt in activity_data])
    mock_render.assert_called_once()
    assert ret == "png_img_obj"


def test_calculate_end_date():
    start = datetime(2023, 1, 1, 9, 0, 0)
    e = ActivityPageHelpers.calculate_end_date(start)
    assert e == start + timedelta(hours=1)


def test_render_bar_chart_executes(helpers_and_db, mocker):
    helpers, db = helpers_and_db
    helpers.start_date = datetime(2025, 1, 1, 11, 0)
    helpers.end_date = datetime(2025, 1, 1, 12, 0)
    mocker.patch("matplotlib.pyplot.show")
    helpers.render_bar_chart(["12:00", "12:10"], [1, 0])


def test_render_bar_chart_to_bytesio_returns_bytesio(helpers_and_db):
    helpers, db = helpers_and_db
    helpers.start_date = datetime(2025, 1, 1, 12, 0)
    helpers.end_date = datetime(2025, 1, 1, 13, 0)
    img = helpers.render_bar_chart_to_bytesio(["12:00", "12:10"], [1, 0])
    assert isinstance(img, io.BytesIO)
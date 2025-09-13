import pytest
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO

from backend.db_operations import DbOperations
from frontend.data_collectors import DataCollectors

DB_NAME_TEST = "mgspy_test_front"


@pytest.fixture(scope="module")
def db():
    db_ops = DbOperations(db_name=DB_NAME_TEST)
    conn = db_ops.connect_to_db()
    yield db_ops, conn
    conn.close()


@pytest.fixture(scope="module")
def dc():
    start_dt = datetime(2025, 6, 28, 11, 0, 0)
    end_dt = datetime(2025, 6, 28, 12, 0, 0)
    dc = DataCollectors(start_dt=start_dt, end_dt=end_dt)
    dc.db_name = "mgspy_test_front"
    return dc


@pytest.fixture
def collector():
    start = datetime(2025, 1, 1, 12, 0, 0)
    end = datetime(2025, 1, 1, 12, 5, 0)
    dc = DataCollectors(start, end)
    return dc


def test_get_player_activity(dc):
    timestamps = dc.get_player_activity("Cycu Dzik")
    assert isinstance(timestamps, list)
    assert isinstance(timestamps[0], datetime)


def test_plot_player_activity(dc, mocker):
    show_mock = mocker.patch("matplotlib.pyplot.show")
    timestamps = dc.get_player_activity("Cycu Dzik")
    dc.plot_player_activity(timestamps)
    show_mock.assert_called_once()


def test_gui_plot_player_activity_png_bytesio(dc):
    timestamps = dc.get_player_activity("Cycu Dzik")
    img_bytes = dc.gui_plot_player_activity(timestamps)
    assert hasattr(img_bytes, "read")
    img_bytes.seek(0)
    png_sig = img_bytes.read(8)
    assert png_sig == b"\x89PNG\r\n\x1a\n"


def test_generate_intervals(collector):
    intervals = collector.generate_intervals()
    expected = [
        datetime(2025, 1, 1, 12, 0, 0),
        datetime(2025, 1, 1, 12, 1, 0),
        datetime(2025, 1, 1, 12, 2, 0),
        datetime(2025, 1, 1, 12, 3, 0),
        datetime(2025, 1, 1, 12, 4, 0),
        datetime(2025, 1, 1, 12, 5, 0),
    ]
    assert intervals == expected


def test_activity_presence_array_full(collector):
    intervals = collector.generate_intervals()
    timestamps = [
        datetime(2025, 1, 1, 12, 0, 0),
        datetime(2025, 1, 1, 12, 1, 0),
        datetime(2025, 1, 1, 12, 2, 0),
        datetime(2025, 1, 1, 12, 3, 0),
        datetime(2025, 1, 1, 12, 4, 0),
    ]
    presence = DataCollectors.activity_presence_array(intervals, timestamps)
    assert presence == [1, 1, 1, 1, 1]


def test_activity_presence_array_none(collector):
    intervals = collector.generate_intervals()
    timestamps = []
    presence = DataCollectors.activity_presence_array(intervals, timestamps)
    assert presence == [0, 0, 0, 0, 0]


def test_activity_presence_array_sparse(collector):
    intervals = collector.generate_intervals()
    timestamps = [
        datetime(2025, 1, 1, 12, 0, 0),
        datetime(2025, 1, 1, 12, 3, 0),
    ]
    presence = DataCollectors.activity_presence_array(intervals, timestamps)
    assert presence == [1, 0, 0, 1, 0]


def test_render_bar_chart_shows(monkeypatch, collector):
    monkeypatch.setattr(plt, "show", lambda: None)
    interval_labels = ['12:00', '12:01', '12:02', '12:03', '12:04']
    presence = [1, 0, 1, 0, 1]
    collector.render_bar_chart(interval_labels, presence)


def test_render_bar_chart_to_bytesio_type(collector):
    interval_labels = ['12:00', '12:01', '12:02', '12:03', '12:04']
    presence = [1, 1, 0, 1, 0]
    img = collector.render_bar_chart_to_bytesio(interval_labels, presence)
    assert isinstance(img, BytesIO)
    # Not empty
    assert img.getbuffer().nbytes > 0

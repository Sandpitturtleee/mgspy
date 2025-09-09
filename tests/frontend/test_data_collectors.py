import pytest
from datetime import datetime, timedelta

from backend.db_operations import DbOperations
from frontend.data_collectors import DataCollectors  # <-- Adjust import if needed

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


def test_get_player_activity(dc):
    timestamps = dc.get_player_activity("Cycu Dzik")
    assert isinstance(timestamps, list)
    assert isinstance(timestamps[0], datetime)


def test_plot_player_activity(dc, mocker):
    # Patch plt.show to avoid actually rendering
    show_mock = mocker.patch("matplotlib.pyplot.show")

    timestamps = dc.get_player_activity("Cycu Dzik")

    # Act - should not error
    dc.plot_player_activity(timestamps)

    # Assert - show was called once
    show_mock.assert_called_once()


def test_gui_plot_player_activity_png_bytesio(dc):
    timestamps = dc.get_player_activity("Cycu Dzik")

    # Act
    img_bytes = dc.gui_plot_player_activity(timestamps)

    # Assert: returns BytesIO with PNG magic bytes
    assert hasattr(img_bytes, "read")
    img_bytes.seek(0)
    png_sig = img_bytes.read(8)
    assert png_sig == b"\x89PNG\r\n\x1a\n"  # PNG file signature

    # Optionally, verify there's some more data (actual image content ≫ header)
    img_bytes.seek(0, 2)  # Seek to end of file
    assert img_bytes.tell() > 100  # At least some content

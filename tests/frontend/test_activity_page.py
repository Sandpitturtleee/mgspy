import pytest
from datetime import datetime
from frontend.activity_page import ActivityPage


@pytest.fixture
def page(mocker):
    mock_helpers = mocker.patch("frontend.activity_page_helpers.ActivityPageHelpers", autospec=True)
    instance = ActivityPage()
    instance.helpers = mock_helpers.return_value
    instance.input_nick = mocker.MagicMock()
    instance.start_date = mocker.MagicMock()
    instance.start_time = mocker.MagicMock()
    instance.plot_area = mocker.MagicMock()
    instance.input_nick.value = ""
    instance.start_date.value = "2025-06-28"
    instance.start_time.value = "11:00"
    return instance


def test_convert_datetime_valid(page):
    page.start_date.value = '2025-06-28'
    page.start_time.value = '11:00'
    dt = page.convert_datetime()
    assert dt == datetime(2025, 6, 28, 11, 0)


def test_convert_datetime_invalid_date(page):
    page.start_date.value = 'bad-date'
    page.start_time.value = '11:00'
    with pytest.raises(ValueError):
        page.convert_datetime()


def test_make_plot_nick_required(page, mocker):
    notify_mock = mocker.patch("frontend.activity_page.ui.notify")
    page.input_nick.value = ''
    page.make_plot()
    notify_mock.assert_called_once()
    assert "please" in notify_mock.call_args[0][0].lower()


def test_make_plot_no_activity(page, mocker):
    page.input_nick.value = "TEST"
    page.start_date.value = '2025-06-28'
    page.start_time.value = '11:00'
    page.helpers.get_player_activity.return_value = None
    notify_mock = mocker.patch("frontend.activity_page.ui.notify")
    page.make_plot()
    notify_mock.assert_called_once()
    assert "no activity" in notify_mock.call_args[0][0].lower()


def test_make_plot_success(page, mocker):
    page.input_nick.value = "Sold"
    page.helpers.get_player_activity.return_value = [datetime(2025, 6, 28, 11, 5)]
    fake_img_bytes = b"PNG bytes"
    mock_img = mocker.MagicMock()
    mock_img.read.return_value = fake_img_bytes
    page.helpers.gui_plot_player_activity.return_value = mock_img
    mocker.patch("frontend.activity_page.ui.notify")
    page.make_plot()
    assert page.plot_area.source.startswith("data:image/png;base64,")

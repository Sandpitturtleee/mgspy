import pytest
from frontend.gui import Gui


def test_navbar_links(mocker):
    # Create a mock for ui.row that acts as a context manager
    row_context = mocker.MagicMock()
    row_context.__enter__.return_value = row_context
    row_context.__exit__.return_value = False
    ui_mock = mocker.patch("frontend.gui.ui")
    ui_mock.row.return_value = row_context

    Gui.navbar()

    ui_mock.row.assert_called_once()
    assert ui_mock.link.call_count == 2
    ui_mock.link.assert_any_call("Data", "/")
    ui_mock.link.assert_any_call("Activity", "/activity")

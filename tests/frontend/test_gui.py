import pytest

from frontend.gui import Gui


@pytest.fixture
def gui(mocker):
    gui = Gui()
    # Patch base64 to always return a known string for the dummy image
    mocker.patch('base64.b64encode', return_value=b'ZmFrZV9wbG90')  # fake_plot

    # Patch ui.image().style() to be a dummy object with a .source attribute
    # and ui.input().style()
    dummy_image = type('DummyImage', (), {'source': None})()
    mocker.patch('nicegui.ui.image', return_value=dummy_image)
    dummy_input = type('DummyInput', (), {'value': ""})()
    mocker.patch('nicegui.ui.input', return_value=dummy_input)

    return gui


def test_make_plot_nick_empty(gui, mocker):
    gui.input_nick.value = ""  # empty
    ui_notify = mocker.patch('nicegui.ui.notify')
    gui.make_plot()
    assert gui.plot_area.source is None
    ui_notify.assert_called_once_with("Please enter a nick!", color="red")


def test_make_plot_no_activity(gui, mocker):
    gui.input_nick.value = "Test"
    # Patch get_player_activity to return None/empty
    mocker.patch.object(gui.collector, "get_player_activity", return_value=None)
    ui_notify = mocker.patch('nicegui.ui.notify')
    gui.make_plot()
    assert gui.plot_area.source is None
    ui_notify.assert_called_once_with("No activity found for nick Test", color="red")


def test_make_plot_with_activity(gui, mocker, img):
    gui.input_nick.value = "Test"
    mocker.patch.object(
        gui.collector, "get_player_activity", return_value=[1, 2, 3]
    )
    mocker.patch.object(
        gui.collector, "gui_plot_player_activity", return_value=img
    )
    # Patch again for the notification (should not be called if plot works)
    ui_notify = mocker.patch('nicegui.ui.notify')
    gui.make_plot()
    assert gui.plot_area.source.startswith("data:image/png;base64,")
    ui_notify.assert_not_called()

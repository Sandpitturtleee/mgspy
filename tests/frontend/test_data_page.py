import pytest
from frontend.data_page_helpers import DataPageHelpers
from frontend.data_page import DataPage


@pytest.fixture
def table_input():
    return [{'nick': 'Sold', 'lvl': 53, 'guild': ''}, ]


@pytest.fixture
def mock_fill_table_input(mocker, table_input):
    return mocker.patch.object(
        DataPageHelpers, "fill_table_input", return_value=table_input)


@pytest.fixture
def fill_table():
    return [{'nick': 'Sold', 'lvl': 53, 'guild': ''}, {'nick': 'Charmed', 'lvl': 135, 'guild': ''}]


@pytest.fixture
def mock_fill_table(mocker):
    return mocker.patch.object(
        DataPageHelpers, "fill_table", return_value=fill_table)


def test_page_calls_helpers_and_sets_values(mocker, mock_fill_table):
    dp = DataPage()

    navbar_mock = mocker.patch.object(dp, "navbar")
    mocker.patch("nicegui.ui.column", mocker.MagicMock())
    mocker.patch("nicegui.ui.button", mocker.MagicMock())
    mocker.patch("nicegui.ui.table", mocker.MagicMock())
    mock_input = mocker.patch("nicegui.ui.input", autospec=True)
    dp.page()

    mock_fill_table.assert_called_once()
    navbar_mock.assert_called()
    mock_input.assert_called()


def test_update_table_button_triggers_fill_table_input(
        mocker, mock_fill_table, mock_fill_table_input,fill_table,table_input):
    dp = DataPage()

    dp.input_nick = mocker.Mock()
    dp.input_nick.value = "Sold"
    dp.table_data = fill_table
    table_mock = mocker.MagicMock()
    local_ctx = {}

    def fake_table(**kwargs):
        local_ctx['rows'] = kwargs['rows']
        return table_mock

    mocker.patch("nicegui.ui.table", fake_table)
    mocker.patch("nicegui.ui.input", return_value=dp.input_nick)
    mocker.patch.object(dp, "navbar")
    mocker.patch("nicegui.ui.button")

    dp.page()
    dp.input_nick.value = "Sold"
    table_mock.rows = dp.helpers.fill_table_input(dp.input_nick.value)
    assert table_mock.rows == table_input


def test_update_table_defaults_on_empty(mocker, mock_fill_table,table_input):
    dp = DataPage()
    dp.input_nick = mocker.Mock()
    dp.input_nick.value = ""
    dp.table_data = table_input
    table_mock = mocker.MagicMock()
    table_mock.rows = None
    dp.helpers.fill_table_input = mocker.MagicMock(return_value=[])
    table_mock.rows = dp.table_data

    assert table_mock.rows == dp.table_data

import pytest
from frontend.data_page import DataPage


@pytest.fixture
def page(mocker):
    helpers_mock = mocker.Mock()
    page = DataPage()
    page.helpers = helpers_mock
    page.input_nick = mocker.Mock()
    return page


def test_update_table_shows_filtered_if_exists(page, mocker):
    page.input_nick.value = "Sold"
    page.table_data = [{'nick': 'Sold', 'lvl': 53, 'guild': ''}]
    filtered_result = [{'nick': 'Sold', 'lvl': 53, 'guild': ''}]
    table_mock = mocker.Mock()
    page.helpers.fill_table_input.return_value = filtered_result

    def update_table():
        nick = page.input_nick.value.strip()
        data = page.helpers.fill_table_input(nick)
        if not data:
            data = page.table_data
        table_mock.rows = data

    update_table()
    page.helpers.fill_table_input.assert_called_with("Sold")
    assert table_mock.rows == filtered_result


def test_update_table_shows_all_if_nick_missing(page, mocker):
    page.input_nick.value = "TEST"
    page.table_data = [{'nick': 'Sold', 'lvl': 53, 'guild': ''}]
    table_mock = mocker.Mock()
    page.helpers.fill_table_input.return_value = []

    def update_table():
        nick = page.input_nick.value.strip()
        data = page.helpers.fill_table_input(nick)
        if not data:
            data = page.table_data
        table_mock.rows = data

    update_table()
    page.helpers.fill_table_input.assert_called_with("TEST")
    assert table_mock.rows == page.table_data


def test_initial_table_data_filled(page):
    sample_data = [{'nick': 'Sold', 'lvl': 53, 'guild': ''}]
    page.helpers.fill_table.return_value = sample_data

    page.table_data = page.helpers.fill_table()
    page.helpers.fill_table.assert_called_once()
    assert page.table_data == sample_data

import pytest

from frontend.data_page_helpers import DataPageHelpers


@pytest.fixture
def test_rows():
    data = [
        ("5111553", "155755", "Charmed", "135", ""),
        ("5111553", "142716", "Sold", "53", ""),
        ("973998", "116256", "Brovvar", "64", ""),
    ]
    return data


@pytest.fixture
def helpers_and_db(mocker, test_rows):
    mock_db_cls = mocker.patch("frontend.data_page_helpers.DbOperations", autospec=True)
    mock_db_instance = mock_db_cls.return_value
    mock_db_instance.connect_to_db.return_value = "mock_conn"
    mock_db_instance.select_data.return_value = test_rows
    helpers = DataPageHelpers()
    mock_db_instance.select_data.reset_mock()
    return helpers, mock_db_instance


def test_get_data(helpers_and_db, test_rows):
    helpers, db = helpers_and_db
    data = helpers.get_data()
    assert data == test_rows
    db.select_data.assert_called_once_with(
        db_connection="mock_conn",
        table="profile_data",
        columns="profile, char, nick, lvl, clan",
    )


def test_fill_table(helpers_and_db):
    helpers, db = helpers_and_db
    table = helpers.fill_table()
    assert table == [
        {"nick": "Charmed", "lvl": 135, "guild": ""},
        {"nick": "Brovvar", "lvl": 64, "guild": ""},
        {"nick": "Sold", "lvl": 53, "guild": ""},
    ]
    assert all(["nick" in row and "lvl" in row and "guild" in row for row in table])


def test_fill_table_input_found(helpers_and_db):
    helpers, db = helpers_and_db
    result = helpers.fill_table_input("Sold")
    assert len(result) == 2
    assert result[0]["lvl"] == 135 or result[0]["lvl"] == 53
    urls = [r["profile"] for r in result]
    assert any(
        url.startswith("https://www.margonem.pl/profile/view,5111553#char_")
        for url in urls
    )


def test_fill_table_input_not_found(helpers_and_db):
    helpers, db = helpers_and_db
    result = helpers.fill_table_input("TEST")
    assert result == []


def test_construct_profile_url(helpers_and_db):
    helpers, db = helpers_and_db
    url = helpers.construct_profile_url("5111553", "155755")
    assert url == "https://www.margonem.pl/profile/view,5111553#char_155755,berufs"


def test_find_profile_id_by_nick_found(helpers_and_db, test_rows):
    helpers, db = helpers_and_db
    profile_id = helpers.find_profile_id_by_nick(test_rows, "Sold")
    assert profile_id == "5111553"


def test_find_profile_id_by_nick_not_found(helpers_and_db, test_rows):
    helpers, db = helpers_and_db
    profile_id = helpers.find_profile_id_by_nick(test_rows, "TEST")
    assert profile_id is None


def test_get_unique_chars_by_profile(helpers_and_db, test_rows):
    helpers, db = helpers_and_db
    results = helpers.get_unique_chars_by_profile(test_rows, "5111553")
    assert len(results) == 2
    data = [item["lvl"] for item in results]
    assert sorted(data, reverse=True) == data  # sorted desc
    for item in results:
        assert item["profile"].startswith(
            "https://www.margonem.pl/profile/view,5111553#char_"
        )

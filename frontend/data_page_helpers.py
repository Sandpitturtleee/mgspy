from typing import Any, List, Dict, Optional
from backend.db_operations import DbOperations


class DataPageHelpers:
    """
    Helper class for handling player profile data from the database and constructing profile URLs.

    Attributes
    ----------
    profile_url : str
        Base URL for player profiles.
    db_name : str
        Name of the database.
    db : DbOperations
        Instance for database operations.
    connection : Any
        Active database connection.
    data : list
        Cached player data from the database.

    Methods
    -------
    get_data() -> list
        Fetch all profile data from the database.
    fill_table() -> List[Dict[str, str | Any]]
        Returns sorted character data for table display.
    fill_table_input(nick: str) -> List[Dict[str, str | Any]]
        Returns all unique characters for a given nick.
    construct_profile_url(profile: str, char: str) -> str
        Constructs a profile URL for a specific profile and character.
    find_profile_id_by_nick(rows: list, nick: str) -> Optional[str]
        Finds the profile ID for a given nickname.
    get_unique_chars_by_profile(rows: list, profile_id: str) -> List[Dict[str, str | Any]]
        Returns all unique characters for a given profile with corresponding URLs.
    """

    def __init__(self):
        self.profile_url: str = "https://www.margonem.pl/profile/view"
        self.db_name: str = "mgspy"
        self.db: DbOperations = DbOperations(db_name=self.db_name)
        self.connection: Any = self.db.connect_to_db()
        self.data: list = self.get_data()

    def get_data(self) -> list:
        """
        Fetch all rows from the database.

        Returns
        -------
        list
            List of tuples for player profile data.
        """
        return self.db.select_data(
            db_connection=self.connection,
            table="profile_data",
            columns="profile, char, nick, lvl, clan"
        )

    def fill_table(self) -> List[Dict[str, str | Any]]:
        """
        Construct a sorted list of players for table display.

        Returns
        -------
        List[Dict[str, str | Any]]
            List of players with 'nick', 'lvl', and 'guild', sorted by level in descending order.
        """
        data: List[Dict[str, str | Any]] = []
        for profile, char, nick, lvl, clan in self.data:
            lvl = int(lvl)
            data.append({
                'nick': nick,
                'lvl': lvl,
                'guild': clan,
            })
        return sorted(data, key=lambda x: x['lvl'], reverse=True)

    def fill_table_input(self, nick: str) -> List[Dict[str, str | Any]]:
        """
        Given a nickname, return a list of unique characters for that profile.

        Parameters
        ----------
        nick : str
            Player nickname to search for.

        Returns
        -------
        List[Dict[str, str | Any]]
            List of unique characters for the player's profile, including the constructed profile URL.
        """
        profile_id = self.find_profile_id_by_nick(self.data, nick)
        if profile_id is None:
            return []
        return self.get_unique_chars_by_profile(self.data, profile_id)

    def construct_profile_url(self, profile: str, char: str) -> str:
        """
        Construct a URL for a specific profile and character.

        Parameters
        ----------
        profile : str
            Profile ID for the player.
        char : str
            Character ID for the player.

        Returns
        -------
        str
            Constructed profile URL for the character.
        """
        return f"{self.profile_url},{profile}#char_{char},berufs"

    @staticmethod
    def find_profile_id_by_nick(rows: list, nick: str) -> Optional[str]:
        """
        Find the profile ID for a given nickname.

        Parameters
        ----------
        rows : list
            List of rows from the database (tuples with profile/char/nick/lvl/clan).
        nick : str
            Nickname to search for.

        Returns
        -------
        Optional[str]
            Profile ID if found, otherwise None.
        """
        for profile, char, nick_db, lvl, clan in rows:
            if nick_db.lower() == nick.lower():
                return profile
        return None

    def get_unique_chars_by_profile(self, rows: list, profile_id: str) -> List[Dict[str, str | Any]]:
        """
        Return all unique characters for a given profile with corresponding profile URLs.

        Parameters
        ----------
        rows : list
            List of rows from the database (tuples with profile/char/nick/lvl/clan).
        profile_id : str
            Profile ID to filter by.

        Returns
        -------
        List[Dict[str, str | Any]]
            List of dictionaries each containing 'nick', 'lvl', 'guild', and 'profile' URL, sorted by level descending.
        """
        seen_chars = set()
        result: List[Dict[str, str | Any]] = []
        for profile, char, nick_db, lvl, clan in rows:
            if profile == profile_id and char not in seen_chars:
                seen_chars.add(char)
                url = self.construct_profile_url(profile, char)
                result.append({
                    'nick': nick_db,
                    'lvl': int(lvl),
                    'guild': clan,
                    'profile': url
                })
        result.sort(key=lambda x: x['lvl'], reverse=True)
        return result

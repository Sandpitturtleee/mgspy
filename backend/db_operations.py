import psycopg2
from psycopg2.extensions import connection
import getpass

class DbOperations:
    """
    Handles basic PostgreSQL operations using psycopg2.

    Methods
    -------
    connect_to_db()
        Connects to the specified PostgreSQL database.

    insert_activity_data(db_connection, player_activity)
        Inserts a list of activity dictionaries into the activity_data table.

    insert_profile_data(db_connection, player_data)
        Inserts a list of profile dictionaries into the profile_data table.

    select_data(db_connection, table, columns='*', where_clause=None, params=None)
        Selects data from the specified table and columns, with an optional WHERE clause.

    delete_data(db_connection, table, where_clause=None, params=None)
        Deletes data from the specified table using an optional WHERE clause.
    """

    def __init__(self, db_name):
        self.db_name = db_name
        self.user = getpass.getuser()

    def connect_to_db(self) -> connection:
        """
        Establish a connection to the PostgreSQL database.

        Returns
        -------
        connection : psycopg2 connection object
        """
        try:
            # Establish a connection to the database
            connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=None,
                host="localhost"
            )

        except Exception as e:
            print(f"An error occurred: {e}")

        return connection

    def insert_activity_data(self, db_connection, player_activity: list[dict]):
        """
        Insert activity data into the activity_data table.

        Parameters
        ----------
        db_connection : psycopg2 connection object
        player_activity : list of dict
            Each dict should have keys 'profile', 'char', 'datetime'
        """
        insert_query = """
        INSERT INTO activity_data (profile, char, datetime)
        VALUES (%s, %s, %s);
        """
        with db_connection.cursor() as cursor:
            for data in player_activity:
                values = (
                    int(data['profile']),
                    int(data['char']),
                    data['datetime']
                )
                cursor.execute(insert_query, values)

            db_connection.commit()
            print("Activity data inserted successfully.")

    def insert_profile_data(self, db_connection, profile_data: list[dict]):
        """
        Insert player profile data into profile_data table.

        Parameters
        ----------
        db_connection : psycopg2 connection object
        player_data : list of dict
            Each dict should have keys: 'profile', 'char', 'nick', 'lvl', 'clan', 'world'
        """
        insert_query = """
        INSERT INTO profile_data (profile, char, nick, lvl, clan, world)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        with db_connection.cursor() as cursor:
            for data in profile_data:
                values = (
                    int(data['profile']),
                    int(data['char']),
                    data.get('nick'),
                    int(data['lvl']) if data.get('lvl') is not None else None,
                    data.get('clan'),
                    data.get('world')
                )
                cursor.execute(insert_query, values)

            db_connection.commit()
            print("Profile data inserted successfully.")

    def select_data(self, db_connection, table: str, columns: str = '*', where_clause: str = None,
                    params: tuple = None):
        """
        Select data from a PostgreSQL table.

        Parameters
        ----------
        db_connection : psycopg2 connection object
        table : str
            Name of the table.
        columns : str, optional
            Columns to select, comma-separated, by default '*' (all).
        where_clause : str, optional
            WHERE clause, e.g., "profile = %s", by default None.
        params : tuple or list, optional
            Parameters to use in the WHERE clause, by default None.

        Returns
        -------
        list of tuple
        """
        select_query = f"SELECT {columns} FROM {table}"
        if where_clause:
            select_query += f" WHERE {where_clause}"

        with db_connection.cursor() as cursor:
            cursor.execute(select_query, params)
            results = cursor.fetchall()
            print(f"{len(results)} rows selected from '{table}'.")
            return results

    def delete_data(self, db_connection, table: str, where_clause: str = None, params: tuple = None):
        """
        Delete data from a PostgreSQL table.

        Parameters
        ----------
        db_connection : psycopg2 connection object
        table : str
            Name of the table.
        where_clause : str, optional
            WHERE clause, e.g., "profile = %s", by default None.
        params : tuple or list, optional
            Parameters for WHERE clause, by default None.
        """
        delete_query = f"DELETE FROM {table}"
        if where_clause:
            delete_query += f" WHERE {where_clause}"

        with db_connection.cursor() as cursor:
            cursor.execute(delete_query, params)
            db_connection.commit()
            print(f"Deleted {cursor.rowcount} rows from {table}.")

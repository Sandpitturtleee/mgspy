import os
import time

import psycopg2
from psycopg2.extensions import connection


class DbOperations:
    """
    Handles basic PostgreSQL operations using psycopg2.

    This class provides methods for connecting to a PostgreSQL database, inserting activity and profile data,
    retrieving and deleting records from tables, with connection parameters controlled via environment variables.

    Attributes
    ----------
    db_name : str
        Name of the PostgreSQL database.
    user : str
        Database username.
    password : str
        Database user's password.
    host : str
        Database host address.
    port : int
        Port on which the database server is running.

    Methods
    -------
    connect_to_db(max_retries=10, delay=2) -> connection
        Connects to the PostgreSQL database with retries.
    insert_activity_data(db_connection, player_activity)
        Inserts a list of activity dictionaries into the activity_data table.
    insert_profile_data(db_connection, player_data)
        Inserts a list of profile dictionaries into the profile_data table.
    select_data(db_connection, table, columns='*', where_clause=None, params=None)
        Selects data from a table.
    delete_data(db_connection, table, where_clause=None, params=None)
        Deletes data from a table.
    """

    def __init__(self, db_name=None):
        """
        Create a database operations instance with connection parameters
        set via environment variables or defaults.

        Parameters
        ----------
        db_name : str, optional
            Database name (default: taken from environment variable DB_NAME or set to 'mgspy').
        """
        self.db_name = db_name or os.environ.get("DB_NAME", "mgspy")
        self.user = os.environ.get("DB_USER", "sold")
        self.password = os.environ.get("DB_PASS", "mgspypass")
        self.host = os.environ.get("DB_HOST", "localhost")
        self.port = int(os.environ.get("DB_PORT", 5432))

    def connect_to_db(self, max_retries=10, delay=2) -> connection:
        """
        Establish a connection to the PostgreSQL database, retrying if the operation fails.

        Connection parameters can be set with the following environment variables:
        - DB_HOST (default: 'localhost')
        - DB_NAME (default: 'mgspy')
        - DB_USER (default: 'sold')
        - DB_PASS (default: 'mgspypass')
        - DB_PORT (default: 5432)

        Parameters
        ----------
        max_retries : int, optional
            Number of retry attempts before failing (default: 10).
        delay : int or float, optional
            Number of seconds to wait between retries (default: 2).

        Returns
        -------
        connection : psycopg2.extensions.connection
            A connection object to the PostgreSQL database.

        Raises
        ------
        Exception
            If the connection cannot be established after the given retries.
        """
        for i in range(max_retries):
            try:
                conn = psycopg2.connect(
                    dbname=self.db_name,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                )
                return conn
            except psycopg2.OperationalError as e:
                print(f"DB not ready (attempt {i + 1}/{max_retries}): {e}")
                time.sleep(delay)
        raise Exception("Database not available after retries!")

    @staticmethod
    def insert_activity_data(db_connection, player_activity: list[dict]):
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
                values = (int(data["profile"]), int(data["char"]), data["datetime"])
                cursor.execute(insert_query, values)

            db_connection.commit()
            print("Activity data inserted successfully.")

    @staticmethod
    def insert_profile_data(db_connection, profile_data: list[dict]):
        """
        Insert player profile data into profile_data table.

        Parameters
        ----------
        db_connection : psycopg2 connection object
        profile_data : list of dict
            Each dict should have keys: 'profile', 'char', 'nick', 'lvl', 'clan', 'world'
        """
        insert_query = """
        INSERT INTO profile_data (profile, char, nick, lvl, clan, world)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        with db_connection.cursor() as cursor:
            for data in profile_data:
                values = (
                    int(data["profile"]),
                    int(data["char"]),
                    data.get("nick"),
                    int(data["lvl"]) if data.get("lvl") is not None else None,
                    data.get("clan"),
                    data.get("world"),
                )
                cursor.execute(insert_query, values)

            db_connection.commit()
            print("Profile data inserted successfully.")

    @staticmethod
    def select_data(
            db_connection,
            table: str,
            columns: str = "*",
            where_clause: str = None,
            params: tuple = None,
    ):
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

    @staticmethod
    def delete_data(
            db_connection, table: str, where_clause: str = None, params: tuple = None
    ):
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

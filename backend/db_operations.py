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
                    params: str = None):
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

    def delete_data(self, db_connection, table: str, where_clause: str = None, params: str = None):
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


if __name__ == "__main__":
    db = DbOperations(db_name="mgspy")
    c = db.connect_to_db()
    try:

        # Sample data
        # data = [{'profile': '7023427', 'char': '101958', 'datetime': '2025-06-15 18:00:09'}, {'profile': '6480295', 'char': '89736', 'datetime': '2025-06-15 18:00:09'}, {'profile': '5250610', 'char': '229627', 'datetime': '2025-06-15 18:00:09'}, {'profile': '8050973', 'char': '135309', 'datetime': '2025-06-15 18:00:09'}, {'profile': '7023427', 'char': '131960', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9439752', 'char': '216620', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9306051', 'char': '224354', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9626924', 'char': '245493', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9894024', 'char': '238720', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9624521', 'char': '240855', 'datetime': '2025-06-15 18:00:09'}, {'profile': '5836957', 'char': '166837', 'datetime': '2025-06-15 18:00:09'}, {'profile': '5250610', 'char': '228312', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9819932', 'char': '243253', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9819932', 'char': '244949', 'datetime': '2025-06-15 18:00:09'}, {'profile': '10038738', 'char': '246010', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9041310', 'char': '246262', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9555962', 'char': '245933', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9288365', 'char': '222380', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9621373', 'char': '225125', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9041310', 'char': '188416', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9513484', 'char': '242925', 'datetime': '2025-06-15 18:00:09'}, {'profile': '10039941', 'char': '246157', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9878842', 'char': '238038', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9340238', 'char': '236600', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9056099', 'char': '186992', 'datetime': '2025-06-15 18:00:09'}, {'profile': '4682173', 'char': '195892', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9041310', 'char': '186881', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9998267', 'char': '243663', 'datetime': '2025-06-15 18:00:09'}, {'profile': '5912389', 'char': '245916', 'datetime': '2025-06-15 18:00:09'}, {'profile': '6591871', 'char': '246076', 'datetime': '2025-06-15 18:00:09'}, {'profile': '10040580', 'char': '246350', 'datetime': '2025-06-15 18:00:09'}, {'profile': '6922769', 'char': '153825', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9507928', 'char': '246274', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9927753', 'char': '246332', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9510820', 'char': '245925', 'datetime': '2025-06-15 18:00:09'}, {'profile': '10044102', 'char': '246337', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9049879', 'char': '234219', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9826639', 'char': '246359', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9442678', 'char': '246372', 'datetime': '2025-06-15 18:00:09'}, {'profile': '6188608', 'char': '246120', 'datetime': '2025-06-15 18:00:09'}, {'profile': '10009609', 'char': '244404', 'datetime': '2025-06-15 18:00:09'}, {'profile': '10038764', 'char': '246013', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9927467', 'char': '246375', 'datetime': '2025-06-15 18:00:09'}, {'profile': '10001328', 'char': '245138', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9826639', 'char': '246371', 'datetime': '2025-06-15 18:00:09'}]

        # Call the function with the connection and data
        # db.insert_data(connection, data)

        # Select all rows:
        # all_rows = db.select_data(connection,table='activity_data')
        all_rows = db.select_data(db_connection=c, table='profile_data')
        print(all_rows)

        # Select with filter:
        # filtered_rows = select_data(connection, "profile = %s", (123,))

        # Delete all rows!
        # db.delete_data(connection,table='profile_data')

        # Delete with filter:
        # delete_data(connection, "profile = %s AND char = %s", (123, 456))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        if c:
            c.close()

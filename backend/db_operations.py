import psycopg2
class DbOperations:
    def __init__(self, db_name):
        self.db_name = db_name

    def connect_to_db(self):
        try:
            # Establish a connection to the database
            connection = psycopg2.connect(
                dbname=self.db_name,
                user="sold",
                password=None,
                host="localhost"
            )

        except Exception as e:
            print(f"An error occurred: {e}")

        # finally:
        #     # Close the connection
        #     if connection:
        #         connection.close()
        return connection

    def insert_data(self,connection, data_list):
        """
        Inserts a list of dictionaries into a PostgreSQL table.

        Parameters:
        - connection: A psycopg2 database connection object.
        - data_list: A list of dictionaries containing the data to be inserted.
        """

        # Assuming the table is named 'example_table' and
        # has columns corresponding to the keys in the dictionaries
        insert_query = """
        INSERT INTO activity_data (profile, char, datetime)
        VALUES (%s, %s, %s);
        """

        with connection.cursor() as cursor:
            for data in data_list:
                # Prepare the data for insertion
                values = (
                    int(data['profile']),
                    int(data['char']),
                    data['datetime']
                )
                # Execute the insert query with data
                cursor.execute(insert_query, values)

            # Commit the transaction
            connection.commit()
            print("Data inserted successfully.")

    def select_data(self,connection, where_clause=None, params=None):
        """
        Selects data from the 'activity_data' table.

        Parameters:
        - connection: A psycopg2 database connection object.
        - where_clause: A string containing an optional WHERE clause (e.g., "profile = %s").
        - params: A tuple or list of parameters to be used with the WHERE clause.

        Returns:
        - A list of tuples for each row fetched.
        """

        # Base SELECT query
        select_query = "SELECT profile, char, datetime FROM activity_data"
        if where_clause:
            select_query += f" WHERE {where_clause}"

        with connection.cursor() as cursor:
            cursor.execute(select_query, params)
            results = cursor.fetchall()
            print(f"{len(results)} rows selected.")
            return results

    def delete_data(self,connection, where_clause=None, params=None):
        """
        Deletes data from the 'activity_data' table.

        Parameters:
        - connection: A psycopg2 database connection object.
        - where_clause: A string containing an optional WHERE clause (e.g., "profile = %s").
        - params: A tuple or list of parameters to be used with the WHERE clause.

        Deletes rows matching the filter. If no filter is provided, deletes all rows!
        """

        # Base DELETE query
        delete_query = "DELETE FROM activity_data"
        if where_clause:
            delete_query += f" WHERE {where_clause}"

        with connection.cursor() as cursor:
            cursor.execute(delete_query, params)
            connection.commit()
            print(f"Deleted {cursor.rowcount} rows from activity_data.")


if __name__ == "__main__":
    db = DbOperations(db_name="mgspy")
    connection = db.connect_to_db()
    try:

        # Sample data
        #data = [{'profile': '7023427', 'char': '101958', 'datetime': '2025-06-15 18:00:09'}, {'profile': '6480295', 'char': '89736', 'datetime': '2025-06-15 18:00:09'}, {'profile': '5250610', 'char': '229627', 'datetime': '2025-06-15 18:00:09'}, {'profile': '8050973', 'char': '135309', 'datetime': '2025-06-15 18:00:09'}, {'profile': '7023427', 'char': '131960', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9439752', 'char': '216620', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9306051', 'char': '224354', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9626924', 'char': '245493', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9894024', 'char': '238720', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9624521', 'char': '240855', 'datetime': '2025-06-15 18:00:09'}, {'profile': '5836957', 'char': '166837', 'datetime': '2025-06-15 18:00:09'}, {'profile': '5250610', 'char': '228312', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9819932', 'char': '243253', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9819932', 'char': '244949', 'datetime': '2025-06-15 18:00:09'}, {'profile': '10038738', 'char': '246010', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9041310', 'char': '246262', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9555962', 'char': '245933', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9288365', 'char': '222380', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9621373', 'char': '225125', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9041310', 'char': '188416', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9513484', 'char': '242925', 'datetime': '2025-06-15 18:00:09'}, {'profile': '10039941', 'char': '246157', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9878842', 'char': '238038', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9340238', 'char': '236600', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9056099', 'char': '186992', 'datetime': '2025-06-15 18:00:09'}, {'profile': '4682173', 'char': '195892', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9041310', 'char': '186881', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9998267', 'char': '243663', 'datetime': '2025-06-15 18:00:09'}, {'profile': '5912389', 'char': '245916', 'datetime': '2025-06-15 18:00:09'}, {'profile': '6591871', 'char': '246076', 'datetime': '2025-06-15 18:00:09'}, {'profile': '10040580', 'char': '246350', 'datetime': '2025-06-15 18:00:09'}, {'profile': '6922769', 'char': '153825', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9507928', 'char': '246274', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9927753', 'char': '246332', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9510820', 'char': '245925', 'datetime': '2025-06-15 18:00:09'}, {'profile': '10044102', 'char': '246337', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9049879', 'char': '234219', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9826639', 'char': '246359', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9442678', 'char': '246372', 'datetime': '2025-06-15 18:00:09'}, {'profile': '6188608', 'char': '246120', 'datetime': '2025-06-15 18:00:09'}, {'profile': '10009609', 'char': '244404', 'datetime': '2025-06-15 18:00:09'}, {'profile': '10038764', 'char': '246013', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9927467', 'char': '246375', 'datetime': '2025-06-15 18:00:09'}, {'profile': '10001328', 'char': '245138', 'datetime': '2025-06-15 18:00:09'}, {'profile': '9826639', 'char': '246371', 'datetime': '2025-06-15 18:00:09'}]

        # Call the function with the connection and data
        #db.insert_data(connection, data)

        # Select all rows:
        all_rows = db.select_data(connection)
        print(all_rows)

        # Select with filter:
        #filtered_rows = select_data(connection, "profile = %s", (123,))

        # Delete all rows!
        #db.delete_data(connection)

        # Delete with filter:
        #delete_data(connection, "profile = %s AND char = %s", (123, 456))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        if connection:
            connection.close()


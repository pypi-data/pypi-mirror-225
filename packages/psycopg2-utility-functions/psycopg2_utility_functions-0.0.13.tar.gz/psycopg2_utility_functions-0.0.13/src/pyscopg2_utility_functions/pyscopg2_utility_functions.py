import psycopg2


def connect_to_database(database, user, password, host, port):
    """
    Establishes a connection to a PostgreSQL database.

    Args:
        database (str): The name of the database.
        user (str): The username for the database connection.
        password (str): The password for the database connection.
        host (str): The host address of the database server.
        port (str): The port number to connect to.

    Returns:
        connection: The connection object for the established database connection.

    Raises:
        psycopg2.Error: If an error occurs while connecting to the database.
    """
    try:
        connection = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        return connection
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        raise e


def execute_query(connection, query):
    """
    Executes a SQL query on the connected database.

    Args:
        connection: The connection object for the database connection.
        query (str): The SQL query to execute.

    Raises:
        psycopg2.Error: If an error occurs while executing the query.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        cursor.close()
    except psycopg2.Error as e:
        print("Error executing query:", e)
        cursor.close()
        raise e


def fetch_data(connection, query, cls=None):
    """
    Retrieves data from the database based on the SQL query and instantiates objects of the specified class.

    Args:
        connection: The connection object for the database connection.
        query (str): The SQL query to fetch data from the database.
        cls (class) - optional: The class to be instantiated for each fetched item.

    Returns:
        list: A list of objects instantiated from the specified class.

    Raises:
        psycopg2.Error: If an error occurs while fetching data.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        if cls is None:
            return result
        else:
            objects = []
            for row in result:
                obj = cls(*row)
                objects.append(obj)

        return objects
    except psycopg2.Error as e:
        print("Error fetching data:", e)
        cursor.close()
        raise e


def insert_data(connection, table, data):
    """
    Inserts a single row of data into a table in the database.

    Args:
        connection: The connection object for the database connection.
        table (str): The name of the table to insert data into.
        data (dict): A dictionary containing the column names and values for the row to be inserted.

    Raises:
        psycopg2.Error: If an error occurs while inserting data.
    """
    cursor = connection.cursor()
    try:
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        values = tuple(data.values())
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
    except psycopg2.Error as e:
        print("Error inserting data:", e)
        cursor.close()
        raise e


def update_data(connection, table, condition, data):
    """
    Updates a row in a table based on a condition.

    Args:
        connection: The connection object for the database connection.
        table (str): The name of the table to update.
        condition (str): The condition for selecting the rows to be updated.
        data (dict): A dictionary containing the column names and new values to update.

    Raises:
        psycopg2.Error: If an error occurs while updating data.
    """
    cursor = connection.cursor()
    try:
        set_values = ', '.join([f"{column} = %s" for column in data.keys()])
        values = tuple(data.values())
        query = f"UPDATE {table} SET {set_values} WHERE {condition}"
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
    except psycopg2.Error as e:
        print("Error updating data:", e)
        cursor.close()
        raise e


def delete_data(connection, table, condition):
    """
    Deletes rows from a table based on a condition.

    Args:
        connection: The connection object for the database connection.
        table (str): The name of the table to delete rows from.
        condition (str): The condition for selecting the rows to be deleted.

    Raises:
        psycopg2.Error: If an error occurs while deleting data.
    """
    cursor = connection.cursor()
    try:
        query = f"DELETE FROM {table} WHERE {condition}"
        cursor.execute(query)
        connection.commit()
        cursor.close()
    except psycopg2.Error as e:
        print("Error deleting data:", e)
        cursor.close()
        raise e

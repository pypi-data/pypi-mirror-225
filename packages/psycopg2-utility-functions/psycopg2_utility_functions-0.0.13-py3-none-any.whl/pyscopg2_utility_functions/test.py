import unittest
from unittest.mock import MagicMock, patch
import psycopg2
from pyscopg2_utility_functions import \
    fetch_data, \
    connect_to_database, \
    delete_data, \
    update_data, \
    insert_data, \
    execute_query


class ExampleClass:
    def __init__(self, _id, name, email):
        self._id = _id
        self.name = name
        self.email = email


class Psycopg2UtilityFunctionsTests(unittest.TestCase):
    # execute_query
    def test_execute_query_success(self):
        # Mock connection and cursor
        connection = MagicMock()
        cursor = connection.cursor.return_value

        # Define a sample query
        query = "SELECT * FROM test_table"

        # Call the execute_query function
        execute_query(connection, query)

        # Verify that cursor.execute was called with the correct query
        cursor.execute.assert_called_once_with(query)

        # Verify that connection.commit and cursor.close were called
        connection.commit.assert_called_once()
        cursor.close.assert_called_once()

    def test_execute_query_error(self):
        # Mock connection and cursor
        connection = MagicMock()
        cursor = connection.cursor.return_value
        cursor.execute.side_effect = psycopg2.Error("Query error")

        # Define a sample query
        query = "SELECT * FROM test_table"

        # Expect a psycopg2.Error exception to be raised
        with self.assertRaises(psycopg2.Error):
            execute_query(connection, query)

        # Verify that cursor.execute was called with the correct query
        cursor.execute.assert_called_once_with(query)

        # Verify that cursor.close was called
        cursor.close.assert_called_once()

    # insert_data
    def test_insert_data_success(self):
        # Mock connection and cursor
        connection = MagicMock()
        cursor = connection.cursor.return_value

        # Call the insert_data function
        data = {"name": "John", "age": 25}
        insert_data(connection, "test_table", data)

        # Verify that cursor.execute was called with the correct query and values
        cursor.execute.assert_called_once_with("INSERT INTO test_table (name, age) VALUES (%s, %s)", ("John", 25))

        # Verify that connection.commit and cursor.close were called
        connection.commit.assert_called_once()
        cursor.close.assert_called_once()

    def test_insert_data_error(self):
        # Mock connection and cursor
        connection = MagicMock()
        cursor = connection.cursor.return_value
        cursor.execute.side_effect = psycopg2.Error("Insert error")

        # Call the insert_data function with data that will trigger an error
        data = {"name": "John", "age": 25}

        # Expect a psycopg2.Error exception to be raised
        with self.assertRaises(psycopg2.Error):
            insert_data(connection, "test_table", data)

        # Verify that cursor.execute was called with the correct query
        cursor.execute.assert_called_once_with("INSERT INTO test_table (name, age) VALUES (%s, %s)", ("John", 25))

        # Verify that cursor.close was called
        cursor.close.assert_called_once()

    # update_data
    def test_update_data_success(self):
        # Mock connection and cursor
        connection = MagicMock()
        cursor = connection.cursor.return_value

        # Call the update_data function
        data = {"name": "John", "age": 25}
        update_data(connection, "test_table", "id = 1", data)

        # Verify that cursor.execute was called with the correct query and values
        cursor.execute.assert_called_once_with("UPDATE test_table SET name = %s, age = %s WHERE id = 1", ("John", 25))

        # Verify that connection.commit and cursor.close were called
        connection.commit.assert_called_once()
        cursor.close.assert_called_once()

    def test_update_data_error(self):
        # Mock connection and cursor
        connection = MagicMock()
        cursor = connection.cursor.return_value
        cursor.execute.side_effect = psycopg2.Error("Update error")

        # Call the update_data function with data that will trigger an error
        data = {"name": "John", "age": 25}

        # Expect a psycopg2.Error exception to be raised
        with self.assertRaises(psycopg2.Error):
            update_data(connection, "test_table", "id = 1", data)

        # Verify that cursor.execute was called with the correct query
        cursor.execute.assert_called_once_with("UPDATE test_table SET name = %s, age = %s WHERE id = 1", ("John", 25))

        # Verify that cursor.close was called
        cursor.close.assert_called_once()

    # delete_data
    def test_delete_data_success(self):
        # Mock connection and cursor
        connection = MagicMock()
        cursor = connection.cursor.return_value

        # Call the delete_data function
        delete_data(connection, "test_table", "id = 1")

        # Verify that cursor.execute was called with the correct query
        cursor.execute.assert_called_once_with("DELETE FROM test_table WHERE id = 1")

        # Verify that connection.commit and cursor.close were called
        connection.commit.assert_called_once()
        cursor.close.assert_called_once()

    def test_delete_data_error(self):
        # Mock connection and cursor
        connection = MagicMock()
        cursor = connection.cursor.return_value
        cursor.execute.side_effect = psycopg2.Error("Delete error")

        # Expect a psycopg2.Error exception to be raised
        with self.assertRaises(psycopg2.Error):
            delete_data(connection, "test_table", "id = 1")

        # Verify that cursor.execute was called with the correct query
        cursor.execute.assert_called_once_with("DELETE FROM test_table WHERE id = 1")

        # Verify that cursor.close was called
        cursor.close.assert_called_once()

    # connect_to_database
    def test_connect_to_database_success(self):
        # Mock psycopg2.connect to return a MagicMock connection object
        with patch('psycopg2.connect', return_value=MagicMock()) as mock_connect:
            connection = connect_to_database("test_db", "user", "password", "localhost", "5432")

            # Verify that psycopg2.connect was called with the correct parameters
            mock_connect.assert_called_once_with(
                database="test_db",
                user="user",
                password="password",
                host="localhost",
                port="5432"
            )

            # Verify that the returned connection object is a MagicMock (i.e., the mock worked)
            self.assertIsInstance(connection, MagicMock)

    def test_connect_to_database_error(self):
        # Mock psycopg2.connect to raise a psycopg2.Error exception
        with patch('psycopg2.connect', side_effect=psycopg2.Error("Connection error")) as mock_connect:
            # Expect a psycopg2.Error exception to be raised
            with self.assertRaises(psycopg2.Error):
                connect_to_database("test_db", "user", "password", "localhost", "5432")

            # Verify that psycopg2.connect was called with the correct parameters
            mock_connect.assert_called_once_with(
                database="test_db",
                user="user",
                password="password",
                host="localhost",
                port="5432"
            )

    # fetch_data
    def test_fetch_data_success(self):
        # Define the example query
        query = "SELECT * FROM test_table;"

        # Define the mock result from the query
        result = [
            (1, 'John Doe', 'john.doe@example.com'),
            (2, 'Jane Smith', 'jane.smith@example.com'),
        ]

        # Define the expected objects
        expected_objects = [
            ExampleClass(*row) for row in result
        ]

        # Mock connection and cursor
        connection = MagicMock()
        cursor = connection.cursor.return_value
        cursor.fetchall.return_value = result

        # Call the fetch_data function
        objects = fetch_data(connection, query, ExampleClass)

        # Assert that the correct objects were returned
        for obj, expected_row in zip(objects, result):
            self.assertEqual(obj._id, expected_row[0])
            self.assertEqual(obj.name, expected_row[1])
            self.assertEqual(obj.email, expected_row[2])

    @patch('psycopg2.connect')
    def test_fetch_data_without_cls(self, mock_connect):
        # Create a MagicMock for the cursor and response
        mock_cursor = MagicMock()
        mock_response = [('Alice', 30), ('Bob', 25)]
        mock_cursor.fetchall.return_value = mock_response

        # Attach the cursor to the mock connection
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        # Set up the mock connect to return the mock connection
        mock_connect.return_value = mock_connection

        # Fetch data without cls parameter
        query = "SELECT name, age FROM test_table WHERE age > 25;"
        fetched_data = fetch_data(mock_connection, query)

        # Check if fetched_data is a list of tuples
        self.assertIsInstance(fetched_data, list)
        self.assertTrue(all(isinstance(data, tuple) for data in fetched_data))

    def test_fetch_data_error(self):
        # Define the example query
        query = "SELECT * FROM non_existent_table;"

        # Mock connection and cursor
        connection = MagicMock()
        cursor = connection.cursor.return_value
        cursor.execute.side_effect = psycopg2.Error("Table not found")

        # Mock the psycopg2.Error for the cursor's execute method
        # Attempt to call the fetch_data function, expecting a psycopg2.Error exception
        with self.assertRaises(psycopg2.Error):
            fetch_data(connection, query, ExampleClass)

        # Assert that cursor.close() was called
        cursor.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()

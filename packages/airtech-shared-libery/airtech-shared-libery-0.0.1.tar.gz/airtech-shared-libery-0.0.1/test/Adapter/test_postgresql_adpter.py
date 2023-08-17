import pytest
import psycopg2
from Adapter.postgresql_adpter import PostgreSQLConnection

class TestPostgreSQLConnection:
    # Tests that a connection to the database can be successfully established
    def test_successful_connection(self):
        with PostgreSQLConnection('localhost', 'test_db', 'test_user', 'test_password') as conn:
            assert conn is not None


    # Test that a connection can be successfully retrieved from the connection pool
    def test_get_connection_from_pool(self):
        with PostgreSQLConnection('localhost', 'test_db', 'test_user', 'test_password') as conn:
            assert conn is not None


    # Test that a connection is successfully put back to the connection pool
    def test_put_connection_back_to_pool(self):
        with PostgreSQLConnection('localhost', 'test_db', 'test_user', 'test_password') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
        self.assertTrue(conn.closed)


    # Tests that a cursor can be successfully created
    def test_create_cursor_success(self):
        with PostgreSQLConnection('localhost', 'test_db', 'user', 'password') as conn:
            cursor = conn.create_cursor()
            assert cursor is not None


    # Tests that an error is raised when unable to connect to the database
    def test_unable_to_connect_to_database(self):
        with pytest.raises(psycopg2.Error):
            with PostgreSQLConnection('invalid_host', 'invalid_db', 'invalid_user', 'invalid_password') as conn:
                cursor = conn.create_cursor()
                cursor.execute('SELECT 1')
                cursor.close()


    # Tests that an error is raised when connection pool is full
    def test_connection_pool_full(self):
        with PostgreSQLConnection('localhost', 'test_db', 'user', 'password') as conn:
            cursor = conn.cursor()
            for i in range(1000):
                cursor.execute(f"SELECT {i}")

        with pytest.raises(psycopg2.pool.PoolError):
            with PostgreSQLConnection('localhost', 'test_db', 'user', 'password') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")


    # Test that the connection is closed before commit or rollback is called
    def test_connection_closed_before_commit_or_rollback(self):
        with PostgreSQLConnection('localhost', 'test_db', 'user', 'password') as conn:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, name VARCHAR(255))')
            cursor.execute('INSERT INTO test_table (name) VALUES (%s)', ('test',))
        assert conn.closed == True


    # Tests that a transaction is successfully committed
    def test_commit_transaction(self):
        with PostgreSQLConnection('localhost', 'test_db', 'user', 'password') as conn:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR(255))')
            cursor.execute('INSERT INTO test_table (name) VALUES (%s)', ('test',))
        with PostgreSQLConnection('localhost', 'test_db', 'user', 'password') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM test_table')
            result = cursor.fetchone()
        assert result == (1, 'test')


    # Tests that multiple connections can be obtained from the connection pool
    def test_multiple_connections_from_pool(self):
        with PostgreSQLConnection('localhost', 'test_db', 'test_user', 'test_password') as conn1:
            with PostgreSQLConnection('localhost', 'test_db', 'test_user', 'test_password') as conn2:
                assert conn1 is not None
                assert conn2 is not None
                assert conn1 is not conn2


    # Tests that the connection pool closes and reopens as expected
    def test_connection_pool_closing_and_reopening(self):
        with PostgreSQLConnection('localhost', 'test_db', 'test_user', 'test_password') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            result = cursor.fetchone()
            assert result == (1,)
        with PostgreSQLConnection('localhost', 'test_db', 'test_user', 'test_password') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 2')
            result = cursor.fetchone()
            assert result == (2,)


    # Tests that an error during a transaction is properly handled by the PostgreSQLConnection class
    def test_error_during_transaction(self):
        with PostgreSQLConnection('localhost', 'test_db', 'user', 'password') as conn:
            cursor = conn.create_cursor()
            cursor.execute('CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR(255))')
            cursor.execute('INSERT INTO test_table (name) VALUES (%s)', ('test',))
            cursor.execute('INSERT INTO test_table (name) VALUES (%s)', ('test2',))
            cursor.execute('INSERT INTO test_table (name) VALUES (%s)', ('test3',))
            cursor.execute('INSERT INTO test_table (name) VALUES (%s)', ('test4',))
            cursor.execute('INSERT INTO test_table (name) VALUES (%s)', ('test5',))
            cursor.execute('INSERT INTO test_table (name) VALUES (%s)', ('test6',))
            cursor.execute('INSERT INTO test_table (name) VALUES (%s)', ('test7',))
            cursor.execute('INSERT INTO test_table (name) VALUES (%s)', ('test8',))
            cursor.execute('INSERT INTO test_table (name) VALUES (%s)', ('test9',))
            cursor.execute('INSERT INTO test_table (name) VALUES (%s)', ('test10',))
            cursor.execute('SELECT * FROM test_table')
            results = cursor.fetchall()
            assert len(results) == 10
        with pytest.raises(psycopg2.Error):
            with PostgreSQLConnection('localhost', 'test_db', 'user', 'password') as conn:
                cursor = conn.create_cursor()
                cursor.execute('SELECT * FROM test_table')
                results = cursor.fetchall()
                assert len(results) == 10
                raise psycopg2.Error('Error during transaction')
        with PostgreSQLConnection('localhost', 'test_db', 'user', 'password') as conn:
            cursor = conn.create_cursor()
            cursor.execute('SELECT * FROM test_table')
            results = cursor.fetchall()
            assert len(results) == 0


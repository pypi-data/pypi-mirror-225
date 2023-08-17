import psycopg2
from psycopg2 import pool
import logging

class postgresql_adpter:
    """
    A class for establishing and managing connections to a PostgreSQL database.

    Args:
        host (str): The hostname or IP address of the database server.
        database (str): The name of the database to connect to.
        user (str): The username for authentication.
        password (str): The password for authentication.

    Attributes:
        host (str): The hostname or IP address of the database server.
        database (str): The name of the database to connect to.
        user (str): The username for authentication.
        password (str): The password for authentication.
        connection_pool (psycopg2.pool.SimpleConnectionPool): The connection pool object.
        logger (logging.Logger): The logger object for logging errors.

    """

    def __init__(self, host, database, user, password):
        """
        Initializes a PostgreSQLConnection object.

        Args:
            host (str): The hostname or IP address of the database server.
            database (str): The name of the database to connect to.
            user (str): The username for authentication.
            password (str): The password for authentication.

        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password

        self.connection_pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=1000,
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        """
        Enters a context manager and gets a connection from the connection pool.

        Returns:
            psycopg2.extensions.connection: The database connection object.

        Raises:
            psycopg2.Error: If an error occurs while connecting to the database.

        """
        try:
            self.connection = self.connection_pool.getconn()
            return self.connection
        except psycopg2.Error as e:
            self.logger.error(f"Error connecting to database: {e}")
            raise e

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exits the context manager and handles transaction management.

        Args:
            exc_type (type): The type of the exception that occurred, if any.
            exc_value (Exception): The exception object that was raised, if any.
            traceback (traceback): The traceback object for the exception, if any.

        """
        if self.connection and not self.connection.closed:
            try:
                if exc_type is not None:
                    self.connection.rollback()
                else:
                    self.connection.commit()
            except psycopg2.Error as e:
                self.logger.error(f"Error during transaction: {e}")
            finally:
                self.connection_pool.putconn(self.connection)

    def create_cursor(self):
        """
        Creates a cursor object for executing SQL queries on the database.

        Returns:
            psycopg2.extensions.cursor: The database cursor object.

        """
        return self.connection.cursor()

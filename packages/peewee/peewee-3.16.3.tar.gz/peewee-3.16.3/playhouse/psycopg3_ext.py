from peewee import *

try:
    import psycopg
    #from psycopg.types.json import Jsonb
except ImportError:
    psycopg = None


class Psycopg3Database(PostgresqlDatabase):
    def _connect(self):
        if psycopg is None:
            raise ImproperlyConfigured('psycopg3 is not installed!')
        conn = psycopg.connect(dbname=self.database, **self.connect_params)
        if self._isolation_level is not None:
            conn.isolation_level = self._isolation_level
        conn.autocommit = True
        return conn

    def get_binary_type(self):
        return psycopg.Binary

    def _set_server_version(self, conn):
        self.server_version = conn.pgconn.server_version
        if self.server_version >= 90600:
            self.safe_create_index = True

    def is_connection_usable(self):
        if self._state.closed:
            return False

        # Returns True if we are idle, running a command, or in an active
        # connection. If the connection is in an error state or the connection
        # is otherwise unusable, return False.
        conn = self._state.conn
        return conn.pgconn.transaction_status < conn.TransactionStatus.INERROR

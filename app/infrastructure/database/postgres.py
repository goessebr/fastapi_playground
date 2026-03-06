import contextlib
import psycopg2
from typing import Optional


class PostgresClient:
    """
    Lightweight admin client for infra tasks (health checks, simple queries).
    Keeps dependency on runtime app code out of infra.
    """

    def __init__(self, dsn: str):
        self._dsn = dsn
        self._conn: Optional[psycopg2.extensions.connection] = None

    def connect(self):
        if self._conn is None or self._conn.closed:
            self._conn = psycopg2.connect(self._dsn)
        return self._conn

    @contextlib.contextmanager
    def cursor(self):
        conn = self.connect()
        cur = conn.cursor()
        try:
            yield cur
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    def health_check(self) -> bool:
        try:
            with self.cursor() as cur:
                cur.execute("SELECT 1")
                return cur.fetchone() == (1,)
        except Exception:
            return False

    def execute(self, sql: str, params: Optional[tuple] = None):
        with self.cursor() as cur:
            cur.execute(sql, params)


# usage example (infra script, not imported by app runtime):
# from app.infrastructure.database.client import PostgresClient
# client = PostgresClient(dsn="postgresql://user:pass@host:5432/dbname")
# ok = client.health_check()

import sqlite3
import logging

logger = logging.getLogger(__file__)

class Repo:
    def __init__(self, connection: sqlite3.Connection):
        self._connection = connection

    def file_is_registered(self, hash_digest: str) -> bool:
        cursor = self._connection.cursor()
        cursor.execute("SELECT true FROM files WHERE sha_256 = ?", (hash_digest,))
        return len(cursor.fetchall()) == 1
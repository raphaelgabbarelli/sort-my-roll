import sqlite3
import logging

logger = logging.getLogger(__file__)

class Repo:
    def __init__(self, connection: sqlite3.Connection):
        self._connection = connection

    def file_is_registered(self, file_name: str, hash_digest: str) -> bool:
        pass
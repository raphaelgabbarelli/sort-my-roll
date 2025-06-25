import sqlite3
import logging

logger = logging.getLogger(__file__)


create_table_files = """
CREATE TABLE IF NOT EXISTS files(
file_id TEXT PRIMARY KEY,
file_name TEXT,
sha_256 BLOB,
date_taken INTEGER
);
"""

def initialize_database():
    logger.info("initializing database")
    try:
        with sqlite3.connect('sortmyroll.db') as conn:
            print('connected to db')
            cursor = conn.cursor()

            cursor.execute(create_table_files)

    except sqlite3.OperationalError as e:
        logger.exception("Error while initializing database", stack_info=True)
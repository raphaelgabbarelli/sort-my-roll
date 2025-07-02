from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent) + '/src')

import pytest
from unittest.mock import Mock
import sqlite3
from sort_my_roll.db.repo import Repo

def test_file_is_registered(mocker):
    connection = Mock(spec=sqlite3.Connection)
    cursor = Mock(spec=sqlite3.Cursor)
    connection.cursor.return_value = cursor
    cursor.fetchone.return_value = (True,)
    
    repo = Repo(connection)

    assert repo.file_is_registered("picture_1.heic", '0f315377c91455bbcb85cfd2cdeb0757cd31892f3c6ce520f42f40ff47ef7b3b') == True

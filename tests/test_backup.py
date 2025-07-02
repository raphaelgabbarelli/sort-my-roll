from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent) + '/src')

import pytest
from unittest.mock import Mock
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Queue
from typing import Any
from collections import namedtuple
from sort_my_roll import backup
from sort_my_roll.db.repo import Repo

class MockPath(Path):
    def read_bytes(self):
        super().read_bytes()

    def iterdir(self):
        super().iterdir()

File = namedtuple('File', ['path', 'digest'])


@pytest.fixture
def fake_pictures_files(mocker) -> list[File]:
     
        mocker.patch.object(file_one := MockPath('/fake/path/to/source/picture_1.heic'), 'read_bytes', lambda: b'Pieces of what we could have been')
        mocker.patch.object(file_two := MockPath('/fake/path/to/source/picture_2.gif'), 'read_bytes', lambda: b'Pieces of a shattered dream')
        mocker.patch.object(file_three := MockPath('/fake/path/to/source/picture_3.jpeg'), 'read_bytes', lambda: b'Child, take your dark memories')
        mocker.patch.object(file_four := MockPath('/fake/path/to/source/picture_4.png'), 'read_bytes', lambda: b'Like seeds and plant them far from here')

        # (Path, sha256_hexdigest_of_read_bytes)
        return [File(file_one, '0f315377c91455bbcb85cfd2cdeb0757cd31892f3c6ce520f42f40ff47ef7b3b'), 
            File(file_two, 'c0f01089f22b8b1a98d1364e8a28a0654b34522197111ac873c5cb83f2d7105d'), 
            File(file_three, '6dea79ffb79cacb091f6741908fb376a19f34f6ca285621bcdd32591e178fafe'), 
            File(file_four, 'bf322d35ede41cdd9bbc8039f66209169638b63962bb7cf6788e6ae2eb3fae3d')]

def test_perform_backup(mocker, fake_pictures_files):
    
    mocker.patch.object(source := MockPath('/fake/path/to/source'), 'iterdir', lambda: iter(p.path for p in fake_pictures_files))
    executor_spy = mocker.spy(ProcessPoolExecutor, 'submit')
    
    queue = Queue()
    backup.perform_backup(absolute_path=source, queue=queue)
    
    assert executor_spy.call_count == len(fake_pictures_files)
    

def test_hash_file(mocker, fake_pictures_files):
    
    backup.global_queue = Queue()
    queue_spy_put = mocker.spy(backup.global_queue, 'put')

    repo = Mock(spec=Repo)

    # simulates picture_1.heic being already registered
    def conditional_return(digest):
        return digest == '0f315377c91455bbcb85cfd2cdeb0757cd31892f3c6ce520f42f40ff47ef7b3b'

    repo.file_is_registered.side_effect = conditional_return
    
    for file in fake_pictures_files:
        backup.hash_file(file.path, repo)

    assert queue_spy_put.call_count == len(fake_pictures_files) - 1
    digests = [file.digest for file in fake_pictures_files]
    while backup.global_queue.qsize() > 0:
        message = backup.global_queue.get()
        message.digest in digests
        
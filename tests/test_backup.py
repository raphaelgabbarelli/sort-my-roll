from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent) + '/src')

import pytest
from concurrent.futures import ProcessPoolExecutor
from typing import Any
from sort_my_roll.backup import perform_backup

class MockPath(Path):
    def read_bytes(self):
        super().read_bytes()

    def iterdir(self):
        super().iterdir()


@pytest.fixture
def fake_paths_to_pictures(mocker) -> list[Path]:
     
        mocker.patch.object(file_one := MockPath('/fake/path/to/source/picture_1.heic'), 'read_bytes', lambda: b'Pieces of what we could have been')
        mocker.patch.object(file_two := MockPath('/fake/path/to/source/picture_2.gif'), 'read_bytes', lambda: b'Pieces of a shattered dream')
        mocker.patch.object(file_three := MockPath('/fake/path/to/source/picture_3.jpeg'), 'read_bytes', lambda: b'Child, take your dark memories')
        mocker.patch.object(file_four := MockPath('/fake/path/to/source/picture_4.png'), 'read_bytes', lambda: b'Like seeds and plant them far from here')
        return [file_one, file_two, file_three, file_four]

def test_traverse_source(mocker, fake_paths_to_pictures):
    
    mocker.patch.object(source := MockPath('/fake/path/to/source'), 'iterdir', lambda: iter(fake_paths_to_pictures))
    executor_spy = mocker.spy(ProcessPoolExecutor, 'submit')
    
    perform_backup(absolute_path=source)
    
    assert executor_spy.call_count == len(fake_paths_to_pictures)
    

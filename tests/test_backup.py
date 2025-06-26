from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent) + '/src')

import pytest
from concurrent.futures import ProcessPoolExecutor
from typing import Any
from sort_my_roll.backup import traverse_source


def test_traverse_source(mocker):
    
    pictures = [
        Path('/fake/path/to/source/picture_1.heic'),
        Path('/fake/path/to/source/picture_2.gif'),
        Path('/fake/path/to/source/picture_3.jpeg'),
        Path('/fake/path/to/source/picture_4.png')
    ]

    mock_path = mocker.patch.object(Path, 'iterdir', return_value=iter(pictures))
    executor_mock = mocker.patch.object(ProcessPoolExecutor, 'map', return_value=iter([]))
    
    executor = ProcessPoolExecutor()
    executor_spy = mocker.spy(executor, 'submit')
    traverse_source(source := Path('/fake/path/to/source'), executor)
    
    assert executor_spy.call_count == len(pictures)
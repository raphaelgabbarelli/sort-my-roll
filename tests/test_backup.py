from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent) + '/src')

import pytest
from sort_my_roll.backup import traverse_source


def test_traverse_source():
    pass
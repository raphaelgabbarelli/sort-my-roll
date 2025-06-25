from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent) + '/src')

import pytest
from sort_my_roll.cli import entry
from click.testing import CliRunner


@pytest.mark.parametrize('command,expected', [
    ('init', 'initializing database'),
    ('backup --source /fakepath', 'performing backup from'),
    ('integrity-check', 'performing integrity check')])
def test_cli(command, expected):
    runner = CliRunner()
    result = runner.invoke(entry, command)
    assert result.exit_code == 0
    assert expected in result.output
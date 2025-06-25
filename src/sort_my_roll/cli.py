import click
from pathlib import Path
import logging
from sort_my_roll.db.init import initialize_database
from sort_my_roll.backup import traverse_source

logger = logging.getLogger(__file__)

@click.group()
def entry():
    pass


@click.command('init', help='initializes the current directory as a backup point')
def init():
    click.echo('initializing database')
    initialize_database()


@click.command('backup', help='perform a backup from source to destination')
@click.option('--source', help='source directory or mountpoint')
def backup(source):
    click.echo(f'performing backup from {source} to local directory')
    
    try:
        source_path = Path(source)
        click.echo(f'checking {source_path}')
        if not source_path.is_dir():
            logger.warning("source option [%s] is not a directory", source)
            click.echo("The --source parameter is not a directory")
        elif not source_path.exists():
            logger.warning("source directory [%s] does not exist", source)
            click.echo("The --source directory does not exist")
    except Exception as e:
        logger.exception("Invalid source")

    traverse_source(source_path)
    
        

@click.command('integrity-check', help='performs an integrity check on the current backup point')
def integrity_check():
    click.echo('performing integrity check')


entry.add_command(init)
entry.add_command(backup)
entry.add_command(integrity_check)
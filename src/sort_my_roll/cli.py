import click
from sort_my_roll.db.init import initialize_database

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


@click.command('integrity-check', help='performs an integrity check on the current backup point')
def integrity_check():
    click.echo('performing integrity check')


entry.add_command(init)
entry.add_command(backup)
entry.add_command(integrity_check)
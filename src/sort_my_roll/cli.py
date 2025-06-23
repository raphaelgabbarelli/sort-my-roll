import click


@click.group()
def entry():
    pass


@click.command('init', help='initializes the current directory as a backup point')
def init():
    print('initializing database')


@click.command('backup', help='perform a backup from source to destination')
@click.option('--source', help='source directory or mountpoint')
@click.option('--destination', default='.', help='destination directory. if left empy, the current directory is assumed to be the destination')
def backup(source, destination):
    print(f'performing backup from {source} to {destination}')


@click.command('integrity-check', help='performs an integrity check on the current backup point')
def integrity_check():
    pass


entry.add_command(init)
entry.add_command(backup)
entry.add_command(integrity_check)
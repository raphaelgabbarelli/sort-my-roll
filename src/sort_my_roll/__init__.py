import sys
import logging
from sort_my_roll.cli import entry

def __setup_logger():
    log_format = '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s'
    handlers = [logging.FileHandler('logs.dat')]
    logging.basicConfig(format=log_format, handlers=handlers)
    

def main():
    __setup_logger()
    sys.exit(entry())


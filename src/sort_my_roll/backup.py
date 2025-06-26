import logging
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Queue
from pathlib import Path

logger = logging.getLogger(__file__)


def hash(file_path: Path):
    print(f'hashing {file_path}')

def pool_initializer(q):
    global queue
    queue = q

def traverse_source(absolute_path: Path, process_pool_executor: ProcessPoolExecutor):
    
    for p in absolute_path.iterdir():
        if p.is_dir():
            traverse_source(p, process_pool_executor)
        else:
            process_pool_executor.submit(hash, p)

def perform_backup(absolute_path: Path):
    queue = Queue()
    with ProcessPoolExecutor(initializer=pool_initializer, initargs=(q,)) as executor:
        traverse_source(absolute_path, executor)
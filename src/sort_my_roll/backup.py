import logging
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Queue
from pathlib import Path

logger = logging.getLogger(__file__)

global_queue = None

def hash(file_path: Path):
    global_queue.put(f'requests for {file_path}')

def pool_initializer(q):
    global global_queue
    global_queue = q

def traverse_source(absolute_path: Path, process_pool_executor: ProcessPoolExecutor):
    
    for p in absolute_path.iterdir():
        if p.is_dir():
            traverse_source(p, process_pool_executor)
        else:
            process_pool_executor.submit(hash, p)

def perform_backup(absolute_path: Path, queue: Queue):
    with ProcessPoolExecutor(initializer=pool_initializer, initargs=(queue,)) as executor:
        traverse_source(absolute_path, executor)
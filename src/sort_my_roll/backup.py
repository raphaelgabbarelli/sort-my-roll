import logging
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Queue
from queue import Full
from pathlib import Path
from hashlib import sha256

from sort_my_roll.db.repo import Repo

logger = logging.getLogger(__file__)
global_queue = None

class WriteCommand:
    def __init__(self, file_name:str, digest: str):
        self.file_name = file_name
        self.digest = digest

def hash_file(file_path: Path, repo: Repo):

    if not repo:
        raise ValueError("Repo cannot be None")

    try:
        digest = sha256(file_path.read_bytes()).hexdigest()
    except TypeError:
        logger.exception("invalid type of content to be hashed")
        # TODO - add to a dead letter queue
        return
    except ValueError:
        logger.exception("invalid content to be hashed")
        # TODO - add to a dead letter queue
        return
        
    if not repo.file_is_registered(digest):
        command = WriteCommand(file_name=file_path.name, digest=digest)
        try:
            global_queue.put(command)
        except ValueError:
            logger.exception("Cannot put command to closed queue")
        except Full:
            logger.exception("Cannot put command to full queue")

def pool_initializer(q):
    global global_queue
    global_queue = q

def traverse_source(absolute_path: Path, process_pool_executor: ProcessPoolExecutor):
    
    for p in absolute_path.iterdir():
        if p.is_dir():
            traverse_source(p, process_pool_executor)
        else:
            process_pool_executor.submit(hash_file, p)

def perform_backup(absolute_path: Path, queue: Queue):
    with ProcessPoolExecutor(initializer=pool_initializer, initargs=(queue,)) as executor:
        traverse_source(absolute_path, executor)
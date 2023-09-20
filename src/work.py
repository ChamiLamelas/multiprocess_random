from multiprocessing import Pool
from pathlib import Path
import numpy as np
import time
import os
import shutil

DATA = os.path.join('..', 'data')
SEQUENTIAL = 'sequential'
PARALLEL = 'parallel'
PARALLEL_SEEDED = 'parallel_seeded'


def clear_dirs(*dirs):
    for dir in dirs:
        if os.path.isdir(dir):
            shutil.rmtree(dir)
        Path(dir).mkdir(parents=True)


def work(run, start_time, save_folder):
    n = np.random.normal(loc=0, scale=1, size=1)[0]
    t = time.time() - start_time
    Path(os.path.join(DATA, save_folder, f"{run}.txt")).write_text(
        f"{t}\n{n}\n")
    time.sleep(5)


def seeded_work(run, start_time, save_folder):
    np.random.seed(os.getpid())
    work(run, start_time, save_folder)


def main():
    clear_dirs(DATA, os.path.join(DATA, SEQUENTIAL), os.path.join(
        DATA, PARALLEL), os.path.join(DATA, PARALLEL_SEEDED))
    
    start_time = time.time()
    pool = Pool(processes=10)
    for run in range(30):
        pool.apply_async(func=work, args=(run, start_time, PARALLEL))
    pool.close()
    pool.join()

    start_time = time.time()
    for run in range(30):
        work(run, start_time, SEQUENTIAL)

    start_time = time.time()
    pool = Pool(processes=10)
    for run in range(30):
        pool.apply_async(func=seeded_work, args=(
            run, start_time, PARALLEL_SEEDED))
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()

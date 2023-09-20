from multiprocessing import Pool
from pathlib import Path
import numpy as np
import time
import os
import shutil
import pickle
from datetime import timedelta
from math import ceil

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
    Path(os.path.join(DATA, save_folder, f"{run}_data.txt")).write_text(
        f"{t}\n{n}\n")
    with open(os.path.join(DATA, save_folder, f"{run}_state.pkl"), 'wb+') as f:
        pickle.dump(np.random.get_state(), f)
    time.sleep(5)


def seeded_work(run, start_time, save_folder):
    seed = int(time.time() * os.getpid()) % (2 ** 32)
    np.random.seed(seed)
    Path(os.path.join(DATA, save_folder,
         f"{run}_seed.txt")).write_text(str(seed) + "\n")
    work(run, start_time, save_folder)


def main():
    script_start_time = time.time()

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
    

    print("Runtime (hh:mm:ss): ", str(
        timedelta(seconds=ceil(time.time() - script_start_time))))


if __name__ == '__main__':
    main()

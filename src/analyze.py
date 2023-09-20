import matplotlib.pyplot as plt
from pathlib import Path
from work import DATA, SEQUENTIAL, PARALLEL, PARALLEL_SEEDED
import os 
import numpy as np
import platform

PLOT = os.path.join("..", "plots")

def plot(folder):
    times = list()
    datas = list()
    for path in os.scandir(os.path.join(DATA, folder)):
        lines = Path(path).read_text().splitlines()
        time = float(lines[0].strip())
        data = float(lines[1].strip())
        times.append(time)
        datas.append(data)
    plt.figure()
    plt.scatter(times, datas)
    plt.title(np.var(datas))
    plt.savefig(os.path.join(PLOT, f"{folder}_dist_{platform.system()}.png"), bbox_inches='tight')

def main():
    Path(PLOT).mkdir(parents=True, exist_ok=True)
    plot(SEQUENTIAL)
    plot(PARALLEL)
    plot(PARALLEL_SEEDED)


if __name__ == '__main__':
    main()
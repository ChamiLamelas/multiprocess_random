import matplotlib.pyplot as plt
from pathlib import Path
from work import DATA, SEQUENTIAL, PARALLEL, PARALLEL_SEEDED
import os
import numpy as np
import platform
import pickle
from collections import Counter

PLOT = os.path.join("..", "plots")


def check_state_equality(state1, state2):
    """checks if 2 numpy random states are equal"""

    return all([(e1 == e2).all() if isinstance(e1, np.ndarray) else e1 == e2 for e1, e2 in zip(state1, state2)])


def tabulate_unhashable(states):
    """
    numpy random states are np.ndarrays so they can't be put into a Counter( )
    to tabulate.

    Thus, to tabulate, we have to tabulate for each state how many other states
    its equal to.

    Example: 

        Let states be represented by letters

        states = [A, B, A, C]
        output = tabulate_unhashable(states)

        output would be [2, 1, 1] because states 1 and 3 were equal and states
        2 and 4 were unique.
    """

    # track which states have already been tabulated
    tabulated = [False] * len(states)

    # equals[i] is all the states discovered to be equal to state i
    # note, if state j equals state i but it was discovered to be equal to i
    # first, equals[j] will be empty
    equals = list()
    for _ in range(len(states)):
        equals.append(list())

    for i, s in enumerate(states):
        # if state was already discovered equal to some earlier state, skip it
        if tabulated[i]:
            continue

        # iterate over other states that haven't been tabulated, if equal to this
        # state, tabulate
        for j, t in enumerate(states):
            if tabulated[j]:
                continue
            if check_state_equality(s, t) or i == j:
                equals[i].append(j)
                tabulated[j] = True

    # output nonzero tabulated counts
    return [len(e) for e in equals if len(e) > 0]


def plot(folder):
    times = list()
    datas = list()
    states = list()
    for entry in os.scandir(os.path.join(DATA, folder)):
        if entry.path.endswith("data.txt"):
            lines = Path(entry.path).read_text().splitlines()
            time = float(lines[0].strip())
            data = float(lines[1].strip())
            times.append(time)
            datas.append(data)
        elif entry.path.endswith(".pkl"):
            with open(entry.path, 'rb') as f:
                states.append(pickle.load(f))
    tabulation = tabulate_unhashable(states)
    plt.figure()
    plt.scatter(times, datas)
    plt.title(f"{folder} Distribution by Time {platform.system()}")
    plt.savefig(os.path.join(
        PLOT, f"{folder}_dist_{platform.system().lower()}.png"), bbox_inches='tight')
    Path(os.path.join(PLOT, f"{folder}_states_{platform.system().lower()}.txt")).write_text(
        ", ".join(str(e) for e in tabulation) + "\n")
    Path(os.path.join(PLOT, f"{folder}_variance_{platform.system().lower()}.txt")).write_text(
        ", ".join(str(e) for e in Counter(datas).values()) + "\n")


def main():
    Path(PLOT).mkdir(parents=True, exist_ok=True)
    plot(SEQUENTIAL)
    plot(PARALLEL)
    plot(PARALLEL_SEEDED)


if __name__ == '__main__':
    main()

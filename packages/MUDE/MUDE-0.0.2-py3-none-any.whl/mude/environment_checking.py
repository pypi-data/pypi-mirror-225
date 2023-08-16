import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy as sp

from pathlib import Path


def check_environment():
    """
    Prints the Conda prefix (full path to Conda installation) of the Conda environment that is
    currently in use. Additionally, prints a list of the versions of a hard-coded set of packages
    that we use within MUDE.
    """
    print("Conda prefix: {}".format(os.environ["CONDA_PREFIX"]))
    print("Numpy version: {}".format(np.__version__))
    print("Matplotlib version: {}".format(mpl.__version__))
    print("Scipy version: {}".format(sp.__version__))


def _print_directory_tree(path):
    """
    Internal helper function that prints out a tree view of a given directory and all subdirectories.
    """
    for root, _, files in os.walk(path):
        indentation = root.replace(path, "").count(os.sep)
        folder_indentation = "    " * indentation
        folder_string = os.path.basename(root)
        print("{}{}/".format(folder_indentation, folder_string))
        file_indentation = "    " * (indentation + 1)
        for file in files:
            print("{}{}".format(file_indentation, file))


def check_directory(level=0):
    """
    Prints a tree view of the currently-active directory, plus the indicated amount of levels upwards.
    """
    current_directory = Path(os.getcwd())
    if level == 0:
        _print_directory_tree(str(current_directory))
    elif level < 0:
        print(
            "Error: cannot print directory to a level {}, which is below 0. Printing level 0 only.".format(
                level
            )
        )
        _print_directory_tree(str(current_directory))
    elif level > len(current_directory.parents):
        print(
            "Error: trying to print out to a level ({}) above the number of parent directories ({}). Printing level 0 only.".format(
                level, len(current_directory.parents)
            )
        )
        _print_directory_tree(str(current_directory))
    else:
        _print_directory_tree(str(current_directory.parents[level - 1]))


def example_plot():
    """
    Creates an example plot of a sine and cosine, primarily as tool to verify that all necessary
    packages and functionality are present to do so.
    """
    fig, ax = plt.subplots(figsize=(6, 3))
    x = np.arange(0, 2 * np.pi, step=0.01)
    sine = np.sin(x)
    cosine = np.cos(x)
    ax.plot(x, sine, label="Sine", color="#00A6D6", linewidth=2)
    ax.plot(x, cosine, label="Cosine", color="#000000", linestyle="--", linewidth=2)
    ax.set_xlabel("Argument [-]")
    ax.set_ylabel("Function value [-]")
    fig.suptitle("Example plot")
    ax.legend()
    plt.show()

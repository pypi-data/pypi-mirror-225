import pandas as pd
from matplotlib import pyplot as plt
import seaborn
from pathlib import Path

from nlpia2.init import DATA_DIR, IMAGES_DIR


FILENAME_ROOT = Path(__file__).with_suffix('').name
CH_STR = 'ch07'
SHOW = False


def render(
        filename_root=FILENAME_ROOT, show=SHOW):
    seaborn.set_theme('notebook')
    seaborn.set_style('whitegrid')

    df = pd.read_csv(DATA_DIR / filename_root, index_col=0)
    figsize = (10, 6)
    fig = plt.figure(figsize=figsize)
    df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
    df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
    df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
    plt.grid('on')
    plt.xlabel('Time (sec)')
    plt.ylabel('Signal amplitude (-1 to +1)')
    plt.legend()
    fig.savefig(IMAGES_DIR / CH_STR / filename_root + '.png')
    if show:
        plt.show(block=False)
    return fig


if __name

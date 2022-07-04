from IPython.display import clear_output
import dataclasses
from typing import List, Union, Tuple

import matplotlib.figure
from matplotlib import pyplot as plt
import numpy as np


@dataclasses.dataclass(init=True)
class LivePlotter:
    x: List
    y: List
    xlim: Union[int, float]
    xlabel: str = "x label"
    ylabel: str = "y label"
    ylim: int = 100
    figsize: Tuple[float] = (10, 10)
    grid: bool = True
    title: str = ""
    fig: matplotlib.figure.Figure = None
    ax: matplotlib.figure.Axes = None
    line_of_best_fit: bool = False

    def new(self):
        fig, ax = plt.plot(self.figsize)
        self.fig = fig
        self.ax = ax

        ax.xlim(0, self.xlim)
        ax.ylim(0, self.ylim)
        ax.title(self.title)

        plt.grid(self.grid)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.show()

    def _add_value(self, val, attr):
        vals = getattr(self, attr)

        if isinstance(val, (int, float)):
            vals.append(float(val))

        if isinstance(val, list):
            vals.append([float(v) for v in val])

        setattr(self, attr, vals)

    def add_values(
        self,
        x: Union[int, float, List[int, float]] = None,
        y: Union[int, float, List[int, float]] = None,
    ):
        self._add_value(x, "x")
        self._add_value(y, "y")

    def live_plot(self):
        clear_output(wait=True)
        self.ax.set_xdata(self.x)
        self.ax.set_ydata(self.x)

        if len(self.x) > 1 and self.line_of_best_fit:
            m, b = list(np.polyfit(x=self.x, y=self.y, deg=1))
            plt.plot(self.x, [x * m for x in self.x] + b)

        self.fig.canvas.draw()

#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /d8analysis/visual/seaborn/grid.py                                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday August 15th 2023 04:04:08 pm                                                #
# Modified   : Tuesday August 15th 2023 04:18:32 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import math

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
from dependency_injector.wiring import inject, Provide

from d8analysis.visual.seaborn.base import SeabornVisual
from d8analysis.visual.seaborn.config import SeabornCanvas
from d8analysis.container import D8AnalysisContainer


# ------------------------------------------------------------------------------------------------ #
class GridPlot:
    """Encapsulates a single or multi-plot visualization

    Args:
        canvas (SeabornCanvas): A dataclass containing the configuration of the canvas
            for the visualization. Optional.

    """

    @inject
    def __init__(
        self,
        title: str = None,
        canvas: type[SeabornCanvas] = Provide[D8AnalysisContainer.canvas.seaborn],
    ) -> None:
        self._title = title
        self._canvas = canvas or SeabornCanvas()
        self._plots = []

    def add_plot(self, plot: SeabornVisual) -> None:
        """Adds a plot object to the visualization

        Args:
            plot (Plot): A Plot object
        """
        self._plots.append(plot)

    def plot(self) -> None:
        sns.set_style(self._canvas.style)
        sns.set_palette(self._canvas.palette)

        self._set_axes()
        for plot in self._plots:
            plot.plot()

    def _set_axes(self) -> None:
        """Sets the axis object on each designated plot."""
        nplots = len(self._plots)
        nrows = math.ceil(nplots / self._canvas.maxcols)
        ncols = min(self._canvas.maxcols, nplots)

        fig = plt.figure(
            layout="constrained", figsize=(self._canvas.width, self._canvas.height * nrows)
        )

        if self._title is not None:
            fig.suptitle(self._title)

        gs = GridSpec(nrows=nrows, ncols=ncols, figure=fig)

        for idx, plot in enumerate(self._plots):
            row = int(idx / ncols)
            col = idx % ncols

            # If last plot, take all remaining columns.
            if idx < nplots - 1:
                ax = fig.add_subplot(gs[row, col])
            else:
                ax = fig.add_subplot(gs[row, col:])

            plot.ax = ax

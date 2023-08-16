#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /d8analysis/visual/seaborn/association.py                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday August 13th 2023 11:25:29 pm                                                 #
# Modified   : Monday August 14th 2023 12:23:02 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Plotizations that Reveal Associations between Variables."""
from typing import Union

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from dependency_injector.wiring import inject, Provide

from d8analysis.container import D8AnalysisContainer
from d8analysis.visual.seaborn.base import SeabornVisual
from d8analysis.visual.seaborn.plot import SeabornVisualizer


# ------------------------------------------------------------------------------------------------ #
class PairPlot(SeabornVisual):  # pragma: no cover
    """Wrapper for the lineplot method in SeabornVisualizer."""

    @inject
    def __init__(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        vars: list = None,
        hue: str = None,
        title: str = None,
        visualizer: SeabornVisualizer = Provide[D8AnalysisContainer.visualizer.seaborn],
        *args,
        **kwargs,
    ) -> None:  # pragma: no cover
        self._visualizer = visualizer
        self._data = data
        self._vars = vars
        self._hue = hue
        self._title = title
        self._args = args
        self._kwargs = kwargs

    def plot(self) -> None:
        """Renders the plot"""
        self._visualizer.pairplot(
            data=self._data,
            vars=self._vars,
            hue=self._hue,
            title=self._title,
            *self._args,
            **self._kwargs,
        )


# ------------------------------------------------------------------------------------------------ #
class ScatterPlot(SeabornVisual):
    """Wrapper for the lineplot method in SeabornVisualizer."""

    @inject
    def __init__(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        ax: plt.Axes = None,
        visualizer: SeabornVisualizer = Provide[D8AnalysisContainer.visualizer.seaborn],
        *args,
        **kwargs,
    ) -> None:  # pragma: no cover
        self._visualizer = visualizer
        self._data = data
        self._x = x
        self._y = y
        self._hue = hue
        self._title = title
        self._ax = ax
        self._args = args
        self._kwargs = kwargs

    def plot(self) -> None:
        """Renders the plot"""
        self._visualizer.scatterplot(
            data=self._data,
            x=self._x,
            y=self._y,
            hue=self._hue,
            title=self._title,
            ax=self._ax,
            *self._args,
            **self._kwargs,
        )


# ------------------------------------------------------------------------------------------------ #
class JointPlot(SeabornVisual):  # pragma: no cover
    """Wrapper for the lineplot method in SeabornVisualizer."""

    @inject
    def __init__(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        visualizer: SeabornVisualizer = Provide[D8AnalysisContainer.visualizer.seaborn],
        *args,
        **kwargs,
    ) -> None:  # pragma: no cover
        self._visualizer = visualizer
        self._data = data
        self._x = x
        self._y = y
        self._hue = hue
        self._title = title
        self._args = args
        self._kwargs = kwargs

    def plot(self) -> None:
        """Renders the plot"""
        self._visualizer.jointplot(
            data=self._data,
            x=self._x,
            y=self._y,
            hue=self._hue,
            title=self._title,
            *self._args,
            **self._kwargs,
        )


# ------------------------------------------------------------------------------------------------ #
class LinePlot(SeabornVisual):
    """Wrapper for the lineplot method in SeabornVisualizer."""

    @inject
    def __init__(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        ax: plt.Axes = None,
        visualizer: SeabornVisualizer = Provide[D8AnalysisContainer.visualizer.seaborn],
        *args,
        **kwargs,
    ) -> None:  # pragma: no cover
        self._visualizer = visualizer
        self._data = data
        self._x = x
        self._y = y
        self._hue = hue
        self._title = title
        self._ax = ax
        self._args = args
        self._kwargs = kwargs

    def plot(self) -> None:
        """Renders the plot"""
        self._visualizer.lineplot(
            data=self._data,
            x=self._x,
            y=self._y,
            hue=self._hue,
            title=self._title,
            ax=self._ax,
            *self._args,
            **self._kwargs,
        )

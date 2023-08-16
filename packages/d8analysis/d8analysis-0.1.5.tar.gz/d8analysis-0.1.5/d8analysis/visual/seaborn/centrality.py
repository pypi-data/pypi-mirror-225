#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /d8analysis/visual/seaborn/centrality.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday August 13th 2023 11:33:13 pm                                                 #
# Modified   : Monday August 14th 2023 12:16:30 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Plotizations that Reveal Centrality for numeric variables."""
from typing import Union

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from dependency_injector.wiring import inject, Provide

from d8analysis.container import D8AnalysisContainer
from d8analysis.visual.seaborn.base import SeabornVisual
from d8analysis.visual.seaborn.plot import SeabornVisualizer


# ------------------------------------------------------------------------------------------------ #
class Barplot(SeabornVisual):  # pragma: no cover
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
        self._visualizer.barplot(
            data=self._data,
            x=self._x,
            y=self._y,
            hue=self._hue,
            title=self._title,
            ax=self._ax,
            *self._args,
            **self._kwargs,
        )

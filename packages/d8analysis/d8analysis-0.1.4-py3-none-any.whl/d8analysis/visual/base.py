#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.10                                                                             #
# Filename   : /d8analysis/visual/base.py                                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday May 28th 2023 06:23:03 pm                                                    #
# Modified   : Sunday August 13th 2023 10:36:00 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass
from abc import ABC, abstractmethod

from d8analysis import DataClass


# ------------------------------------------------------------------------------------------------ #
#                                           COLORS                                                 #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class Colors(DataClass):
    cool_black: str = "#002B5B"
    police_blue: str = "#2B4865"
    teal_blue: str = "#256D85"
    pale_robin_egg_blue: str = "#8FE3CF"
    russian_violet: str = "#231955"
    dark_cornflower_blue: str = "#1F4690"
    meat_brown: str = "#E8AA42"
    peach: str = "#FFE5B4"
    dark_blue: str = "#002B5B"
    blue: str = "#1F4690"
    orange: str = "#E8AA42"
    crimson: str = "#BA0020"

    def __post_init__(self) -> None:
        return


# ------------------------------------------------------------------------------------------------ #
#                                           CANVAS                                                 #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class Canvas(DataClass):
    """Namespace for Canvas subclasses"""


# ------------------------------------------------------------------------------------------------ #
#                                       VISUALIZER                                                 #
# ------------------------------------------------------------------------------------------------ #
class Visualizer(ABC):  # pragma: no cover
    """Wrapper for Seaborn visualizations.


    Args:
        canvas (Canvas): A dataclass containing the configuration of the canvas
            for the visualization.
    """

    @abstractmethod
    def __init__(self, canvas: Canvas, *args, **kwargs) -> None:  # pragma: no cover
        """Defines the construction requirement for Visualizers"""

    @abstractmethod
    def lineplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def boxplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def kdeplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def ecdfplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def histogram(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def scatterplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def barplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""


# ------------------------------------------------------------------------------------------------ #
#                                          Visual                                                  #
# ------------------------------------------------------------------------------------------------ #
class Visual(ABC):
    """Wrapper classes for Visualizer methods."""

    def plot(self) -> None:
        """Renders the visualization."""

#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /d8analysis/visual/seaborn/config.py                                                #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 24th 2023 04:11:27 pm                                                 #
# Modified   : Tuesday August 15th 2023 05:16:08 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
import math
from dataclasses import dataclass, field

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

from d8analysis import DataClass
from d8analysis.visual.base import Canvas
from d8analysis.visual.config import Colors

# ------------------------------------------------------------------------------------------------ #
plt.rcParams["font.size"] = "10"

# ------------------------------------------------------------------------------------------------ #
#                                            PALETTES                                              #
# ------------------------------------------------------------------------------------------------ #
SEABORN_PALETTES = {
    "darkblue": sns.dark_palette("#69d", reverse=False, as_cmap=False),
    "darkblue_r": sns.dark_palette("#69d", reverse=True, as_cmap=False),
    "winter_blue": sns.color_palette(
        [Colors.cool_black, Colors.police_blue, Colors.teal_blue, Colors.pale_robin_egg_blue],
        as_cmap=True,
    ),
    "blue_orange": sns.color_palette(
        [Colors.russian_violet, Colors.dark_cornflower_blue, Colors.meat_brown, Colors.peach],
        as_cmap=True,
    ),
}


@dataclass
class Palettes(DataClass):
    blues: str = "Blues"
    blues_r: str = "Blues_r"
    mako: str = "mako"
    bluegreen: str = "crest"
    paired: str = "Paired"
    dark: str = "dark"
    colorblind: str = "colorblind"
    seaborn_palettes: dict = field(default_factory=dict)


# ------------------------------------------------------------------------------------------------ #
#                                            LEGEND                                                #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class LegendConfig(DataClass):
    loc: str = "best"
    ncols: int = 1
    fontsize: int = 8
    labels: list[str] = field(default_factory=list)
    markerfirst: bool = True
    reverse: bool = False
    frameon: bool = False
    fancybox: bool = True
    framealpha: float = 0.3
    mode: str = None
    title: str = None
    title_fontsize: int = 8
    alignment: str = "left"


# ------------------------------------------------------------------------------------------------ #
#                                       HISTPLOT CONFIG                                            #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class HistDataClass(DataClass):
    stat: str = "count"  # Most used values are ['count', 'probability', 'percent', 'density']
    discrete: bool = False
    cumulative: bool = False
    multiple: str = "layer"  # Valid values ['layer','dodge','stack','fill']
    element: str = "bars"  # Also use 'step'
    fill: bool = False
    kde: bool = True
    legend: bool = True


# ------------------------------------------------------------------------------------------------ #
#                                       HISTPLOT CONFIG                                            #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class KdeDataClass(DataClass):
    cumulative: bool = False
    multiple: str = "layer"  # Valid values ['layer','dodge','stack','fill']
    fill: bool = None
    legend: bool = True


# ------------------------------------------------------------------------------------------------ #
#                                        BARPLOT CONFIG                                            #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class BarDataClass(DataClass):
    estimator: str = "sum"  # ['mean','sum']
    saturation: float = 0.7
    dodge: bool = False


# ------------------------------------------------------------------------------------------------ #
#                                      COUNTPLOT CONFIG                                            #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class CountDataClass(DataClass):
    saturation: float = 0.7
    dodge: bool = False


# ------------------------------------------------------------------------------------------------ #
#                                      POINTPLOT CONFIG                                            #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class PointDataClass(DataClass):
    estimator: str = "mean"
    dodge: bool = False
    linestyles: str = "-"
    join: bool = True

    def __post_init__(self) -> None:
        return


# ------------------------------------------------------------------------------------------------ #
#                                       BOXPLOT CONFIG                                             #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class BoxDataClass(DataClass):
    saturation: float = 0.7
    dodge: bool = True


# ------------------------------------------------------------------------------------------------ #
#                                      SCATTERPLOT CONFIG                                          #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class ScatterDataClass(DataClass):
    size: str = None
    style: str = None
    markers: bool = True
    legend: str = "auto"  # Valid values: ['auto','brief','full',False]
    dodge: bool = True


# ------------------------------------------------------------------------------------------------ #
#                                      LINEPLOT CONFIG                                             #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class LineDataClass(DataClass):
    size: str = None
    style: str = None
    dashes: bool = True
    estimator: str = "mean"
    markers: bool = None
    sort: bool = True
    legend: str = "auto"  # Valid values: ['auto','brief','full',False]
    dodge: bool = True


# ------------------------------------------------------------------------------------------------ #
#                                      HEATMAP CONFIG                                              #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class HeatmapConfig(DataClass):
    vmin: float = None
    vmax: float = None
    cmap: str = str
    center: float = None
    annot: bool = True
    fmt: str = None
    linewidths: float = 0
    linecolor: str = "white"
    cbar: bool = True
    cbar_kws: dict = None
    square: bool = False
    xticklabels: str = "auto"
    yticklabels: str = "auto"


# ------------------------------------------------------------------------------------------------ #
#                                            CANVAS                                                #
# ------------------------------------------------------------------------------------------------ #


@dataclass
class SeabornCanvas(Canvas):
    """SeabornCanvas class encapsulating figure level configuration."""

    width: int = 12  # The maximum width of the canvas
    height: int = 4  # The height of a single row.
    maxcols: int = 2  # The maximum number of columns in a multi-plot visualization.
    palette: str = "Blues_r"  # Seaborn palette or matplotlib colormap
    style: str = "whitegrid"  # A Seaborn aesthetic
    saturation: float = 0.5
    fontsize: int = 10
    fontsize_title: int = 12
    colors: Colors = Colors()
    palettes: Palettes = Palettes()
    legend_config: LegendConfig = LegendConfig()
    histplot_config: HistDataClass = HistDataClass()
    kdeplot_config: KdeDataClass = KdeDataClass()
    heatmap_config: HeatmapConfig = HeatmapConfig()
    lineplot_config: LineDataClass = LineDataClass()
    scatterplot_config: ScatterDataClass = ScatterDataClass()
    boxplot_config: BoxDataClass = BoxDataClass()
    pointplot_config: PointDataClass = PointDataClass()
    countplot_config: CountDataClass = CountDataClass()
    barplot_config: BarDataClass = BarDataClass()

    def get_figaxes(self, nplots: int = 1, figsize: tuple = None) -> SeabornCanvas:
        """Configures the figure and axes objects.

        Args:
            nplots (int): The number of plots to be rendered on the canvas.
            figsize (tuple[int,int]): Plot width and row height.
        """
        figsize = figsize or (self.width, self.height)

        if nplots == 1:
            fig, axes = plt.subplots(figsize=figsize)
        else:
            nrows = math.ceil(nplots / self.maxcols)
            ncols = min(self.maxcols, nplots)

            fig = plt.figure(layout="constrained", figsize=figsize)
            gs = GridSpec(nrows=nrows, ncols=ncols, figure=fig)

            axes = []
            for idx in range(nplots):
                row = int(idx / ncols)
                col = idx % ncols

                if idx < nplots - 1:
                    ax = fig.add_subplot(gs[row, col])
                else:
                    ax = fig.add_subplot(gs[row, col:])
                axes.append(ax)

        return fig, axes

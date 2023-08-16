#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /d8analysis/visual/seaborn/plot.py                                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday August 13th 2023 08:23:33 am                                                 #
# Modified   : Tuesday August 15th 2023 03:37:06 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Wrapper for several Seaborn plotting functions."""
from typing import List, Union

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from d8analysis.visual.base import Visualizer
from d8analysis.visual.seaborn.config import SeabornCanvas


# ------------------------------------------------------------------------------------------------ #
class SeabornVisualizer(Visualizer):  # pragma: no cover
    """Wrapper for Seaborn plotiziations."""

    def __init__(self, canvas: SeabornCanvas):
        super().__init__(canvas)
        self._canvas = canvas
        sns.set_style(style=self._canvas.style)
        sns.set_palette(palette=self._canvas.palette)

    def lineplot(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        ax: plt.Axes = None,
        *args,
        **kwargs,
    ) -> None:
        """Draw a line plot with possibility of several semantic groupings.

        The relationship between x and y can be shown for different subsets of the data using the
        hue, size, and style parameters. These parameters control what visual semantics are used to
        identify the different subsets. It is possible to show up to three dimensions independently
        by using all three semantic types, but this style of plot can be hard to interpret and is
        often ineffective. Using redundant semantics (i.e. both hue and style for the same variable)
        can be helpful for making graphics more accessible.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.


        """
        if ax is None:
            fig, ax = self._canvas.get_figaxes()

        sns.lineplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            ax=ax,
            palette=self._canvas.palette,
            *args,
            **kwargs,
        )
        if title is not None:
            ax.set_title(title)

    def scatterplot(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        ax: plt.Axes = None,
        *args,
        **kwargs,
    ) -> None:
        """Draw a scatter plot with possibility of several semantic groupings.

        The relationship between x and y can be shown for different subsets of the data using the
        hue, size, and style parameters. These parameters control what visual semantics are used to
        identify the different subsets. It is possible to show up to three dimensions independently
        by using all three semantic types, but this style of plot can be hard to interpret and is
        often ineffective. Using redundant semantics (i.e. both hue and style for the same variable)
        can be helpful for making graphics more accessible.

        Args: Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.


        """
        if ax is None:
            fig, ax = self._canvas.get_figaxes()

        sns.scatterplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            ax=ax,
            palette=self._canvas.palette,
            *args,
            **kwargs,
        )
        if title is not None:
            ax.set_title(title)

    def histogram(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        x: str = None,
        y: str = None,
        hue: str = None,
        stat: str = "density",
        element: str = "bars",
        fill: bool = True,
        title: str = None,
        ax: plt.Axes = None,
        *args,
        **kwargs,
    ) -> None:
        """Draw a scatter plot with possibility of several semantic groupings.

        The relationship between x and y can be shown for different subsets of the data using the
        hue, size, and style parameters. These parameters control what visual semantics are used to
        identify the different subsets. It is possible to show up to three dimensions independently
        by using all three semantic types, but this style of plot can be hard to interpret and is
        often ineffective. Using redundant semantics (i.e. both hue and style for the same variable)
        can be helpful for making graphics more accessible.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            stat (str): Aggregate statistics for each bin. Optional. Default is 'density'.
                See https://seaborn.pydata.org/generated/seaborn.histplot.html for valid values.
            element (str): Visual representation of the histogram statistic. Only relevant with univariate data. Optional. Default is 'bars'. fill (bool): If True, fill in the space under the histogram. Only relevant with univariate data.
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.


        """
        if ax is None:
            fig, ax = self._canvas.get_figaxes()

        sns.histplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            stat=stat,
            element=element,
            fill=fill,
            ax=ax,
            palette=self._canvas.palette,
            *args,
            **kwargs,
        )
        if title is not None:
            ax.set_title(title)

    def boxplot(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        ax: plt.Axes = None,
        *args,
        **kwargs,
    ) -> None:
        """Draw a box plot to show distributions with respect to categories.

        A box plot (or box-and-whisker plot) shows the distribution of quantitative data in a way
        that facilitates comparisons between variables or across levels of a categorical variable.
        The box shows the quartiles of the dataset while the whiskers extend to show the rest of the
        distribution, except for points that are determined to be “outliers” using a method that is
        a function of the inter-quartile range.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.


        """
        if ax is None:
            fig, ax = self._canvas.get_figaxes()

        sns.boxplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            ax=ax,
            palette=self._canvas.palette,
            *args,
            **kwargs,
        )
        if title is not None:
            ax.set_title(title)

    def kdeplot(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        ax: plt.Axes = None,
        *args,
        **kwargs,
    ) -> None:
        """Plot univariate or bivariate distributions using kernel density estimation.

        A kernel density estimate (KDE) plot is a method for visualizing the distribution of
        observations in a dataset, analogous to a histogram. KDE represents the data using a
        continuous probability density curve in one or more dimensions.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.


        """
        if ax is None:
            fig, ax = self._canvas.get_figaxes()

        sns.kdeplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            ax=ax,
            palette=self._canvas.palette,
            *args,
            **kwargs,
        )
        if title is not None:
            ax.set_title(title)

    def ecdfplot(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        ax: plt.Axes = None,
        *args,
        **kwargs,
    ) -> None:
        """Plot empirical cumulative distribution functions.

        An ECDF represents the proportion or count of observations falling below each unique value
        in a dataset. Compared to a histogram or density plot, it has the advantage that each
        observation is visualized directly, meaning that there are no binning or smoothing
        parameters that need to be adjusted. It also aids direct comparisons between multiple
        distributions. A downside is that the relationship between the appearance of the plot and
        the basic properties of the distribution (such as its central tendency, variance, and the
        presence of any bimodality) may not be as intuitive.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.

        """
        if ax is None:
            fig, ax = self._canvas.get_figaxes()

        sns.ecdfplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            ax=ax,
            palette=self._canvas.palette,
            *args,
            **kwargs,
        )
        if title is not None:
            ax.set_title(title)

    def barplot(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        ax: plt.Axes = None,
        *args,
        **kwargs,
    ) -> None:
        """Show point estimates and errors as rectangular bars.

        A bar plot represents an estimate of central tendency for a numeric variable with the height of each
        rectangle and provides some indication of the uncertainty around that estimate using error bars. Bar
        plots include 0 in the quantitative axis range, and they are a good choice when 0 is a meaningful
        value for the quantitative variable, and you want to make comparisons against it.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.

        """
        if ax is None:
            fig, ax = self._canvas.get_figaxes()

        sns.barplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            ax=ax,
            palette=self._canvas.palette,
            *args,
            **kwargs,
        )
        if title is not None:
            ax.set_title(title)

        if hue is not None:
            plt.legend(loc="upper right")

    def violinplot(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        ax: plt.Axes = None,
        *args,
        **kwargs,
    ) -> None:
        """Draw a combination of boxplot and kernel density estimate.

        A violin plot plays a similar role as a box and whisker plot. It shows the distribution of
        quantitative data across several levels of one (or more) categorical variables such that those
        distributions can be compared. Unlike a box plot, in which all of the plot components correspond to
        actual datapoints, the violin plot features a kernel density estimation of the underlying
        distribution.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.


        """
        if ax is None:
            fig, ax = self._canvas.get_figaxes()

        sns.violinplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            ax=ax,
            palette=self._canvas.palette,
            *args,
            **kwargs,
        )
        if title is not None:
            ax.set_title(title)

    def histpdfplot(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        x: str = None,
        y: str = None,
        title: str = None,
        ax: plt.Axes = None,
        *args,
        **kwargs,
    ) -> None:
        """Draw a combination of a histogram and the theoretical probability density function.

        This 'goodness of fit' visualization reveals the contrast between an empirical distribution
        and a theoretical probability distribution, estimated using the parameters from the data.
        The histogram renders counts from the data value. The values for the theoretical probability
        density function, x_pdf, and y_pdf is rendered on a shared x-axis.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x_pdf, y_pdf (np.ndarray): Array containing x and y value of the probability density function.
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.


        """
        if ax is None:
            fig, ax = self._canvas.get_figaxes()

        ax = sns.histplot(
            data=data,
            x=x,
            y=y,
            stat="density",
            element="bars",
            fill=True,
            kde=True,
            color=self._canvas.colors.dark_blue,
            ax=ax,
            label="Empirical Distribution",
            legend=True,
        )
        if title is not None:
            ax.set_title(title)

    def pdfcdfplot(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        x: str = None,
        y: str = None,
        title: str = None,
        ax: plt.Axes = None,
        *args,
        **kwargs,
    ) -> None:
        """Renders a combination of the probabiity density and cumulative distribution functions.

        This visualization provides the probability density function and cumulative distribution
        function in a single plot with shared x-axis.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.



        """
        if ax is None:
            fig, ax1 = self._canvas.get_figaxes()

        ax1 = sns.kdeplot(
            data=data,
            x=x,
            y=y,
            color=self._canvas.colors.dark_blue,
            ax=ax1,
            label="Probability Density Function",
            legend=True,
        )
        ax2 = ax1.twinx()
        ax2 = sns.kdeplot(
            data=data,
            x=x,
            y=y,
            cumulative=True,
            ax=ax2,
            color=self._canvas.colors.orange,
            label="Cumulative Distribution Function",
            legend=True,
        )
        title = "Probability Density Function and Cumulative Distribution Function"

        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()

        ax1.legend(handles=h1 + h2, labels=l1 + l2, loc="upper left")
        fig.suptitle(title, fontsize=self._canvas.fontsize_title)
        fig.tight_layout()

    def pairplot(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        vars: list = None,
        hue: str = None,
        title: str = None,
        *args,
        **kwargs,
    ) -> None:
        """Plot pairwise relationships in a dataset.

        By default, this function will create a grid of Axes such that each numeric variable in data
        will by shared across the y-axes across a single row and the x-axes across a single column.
        The diagonal plots are treated differently: a univariate distribution plot is drawn to show
        the marginal distribution of the data in each column.

        It is also possible to show a subset of variables or plot different variables on the rows
        and columns.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure.
                Either a long-form collection of vectors that can be assigned to named variables or
                a wide-form dataset that will be internally reshaped
            vars (list): Variables within data to use, otherwise use every column with a numeric datatype. Optional, if not provided all numeric columns will be included.
            hue (str): Grouping variable that will produce lines with different colors. Can be
            either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional


        """

        g = sns.pairplot(
            data=data,
            vars=vars,
            hue=hue,
            palette=self._canvas.palette,
            *args,
            **kwargs,
        )
        if title is not None:
            g.fig.suptitle(title)
        g.tight_layout()

    def jointplot(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        *args,
        **kwargs,
    ) -> None:
        """Draw a plot of two variables with bivariate and univariate graphs.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional


        """

        g = sns.jointplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            palette=self._canvas.palette,
            *args,
            **kwargs,
        )
        if title is not None:
            g.fig.suptitle(title)
        g.fig.tight_layout()

    def _wrap_ticklabels(
        self, axis: str, axes: List[plt.Axes], fontsize: int = 8
    ) -> List[plt.Axes]:
        """Wraps long tick labels"""
        if axis.lower() == "x":
            for i, ax in enumerate(axes):
                xlabels = [label.get_text() for label in ax.get_xticklabels()]
                xlabels = [label.replace(" ", "\n") for label in xlabels]
                ax.set_xticklabels(xlabels, fontdict={"fontsize": fontsize})
                ax.tick_params(axis="x", labelsize=fontsize)

        if axis.lower() == "y":
            for i, ax in enumerate(axes):
                ylabels = [label.get_text() for label in ax.get_yticklabels()]
                ylabels = [label.replace(" ", "\n") for label in ylabels]
                ax.set_yticklabels(ylabels, fontdict={"fontsize": fontsize})
                ax.tick_params(axis="y", labelsize=fontsize)

        return axes

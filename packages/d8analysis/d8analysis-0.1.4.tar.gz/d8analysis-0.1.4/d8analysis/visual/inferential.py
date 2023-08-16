#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /d8analysis/visual/inferential.py                                                   #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday August 11th 2023 06:37:59 pm                                                 #
# Modified   : Monday August 14th 2023 04:30:39 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Continuous Random Variable Probability Distributions"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

from dependency_injector.wiring import inject, Provide

from d8analysis.container import D8AnalysisContainer
from d8analysis.visual.base import Plot
from d8analysis.visual.seaborn.config import SeabornCanvas
from d8analysis.quantitative.inferential.centrality.ttest import TTestResult
from d8analysis.quantitative.inferential.chisquare import ChiSquareResult
from d8analysis.quantitative.inferential.distribution.kstest import KSOneTestResult
from d8analysis.data.generation import RVSDistribution


# ------------------------------------------------------------------------------------------------ #
#                            STUDENT'S T HYPOTHESIS TEST                                           #
# ------------------------------------------------------------------------------------------------ #
class TTestPlot(Plot):  # pragma: no cover
    """Plots a Student's t probability density function (PDF) for a student's t-test.

    Parameterized by the t-statistic, degrees of freedom and the signficance level, this
    object plots the PDF and the hypothesis test reject region.

    Args:
        result (TTestResult): A Student's t-test result object.
        ax (plt.Axes): A matplotlib Axes object. Optional. If  If not none, the ax parameter
            overrides the default set in the base class.
        title (str): The visualization title. Optional
        canvas (SeabornCanvas): A dataclass containing the configuration of the canvas
            for the visualization. Optional.
        args and kwargs passed to the underlying seaborn histplot method.
            See https://seaborn.pydata.org/generated/seaborn.histplot.html for a
            complete list of parameters.
    """

    @inject
    def __init__(
        self,
        result: TTestResult,
        title: str = None,
        canvas: type[SeabornCanvas] = Provide[D8AnalysisContainer.canvas],
        *args,
        **kwargs,
    ) -> None:
        super().__init__(canvas=canvas)
        self._result = result
        self._canvas = canvas
        self._title = title
        self._args = args
        self._kwargs = kwargs

        self._axes = None
        self._fig = None
        sns.set_style(self._canvas.style)

    def plot(self) -> None:
        self._axes = self._axes or self._canvas.config().axes

        # Render the probability distribution
        x = np.linspace(
            stats.t.ppf(0.001, self._result.dof), stats.t.ppf(0.999, self._result.dof), 500
        )
        y = stats.t.pdf(x, self._result.dof)
        self._ax = sns.lineplot(x=x, y=y, markers=False, dashes=False, sort=True, ax=self._ax)

        # Compute reject region
        lower = x[0]
        upper = x[-1]
        lower_alpha = self._result.alpha / 2
        upper_alpha = 1 - (self._result.alpha / 2)
        lower_critical = stats.t.ppf(lower_alpha, self._result.dof)
        upper_critical = stats.t.ppf(upper_alpha, self._result.dof)

        self._fill_reject_region(
            lower=lower, upper=upper, lower_critical=lower_critical, upper_critical=upper_critical
        )

        self._ax.set_title(
            f"{self._result.result}",
            fontsize=self._canvas.fontsize_title,
        )

        # ax.set_xlabel(r"$X^2$")
        self._ax.set_ylabel("Probability Density")
        plt.tight_layout()

        if self._legend_config is not None:
            self.config_legend()

    def _fill_reject_region(
        self,
        lower: float,
        upper: float,
        lower_critical: float,
        upper_critical: float,
    ) -> None:
        """Fills the area under the curve at the value of the hypothesis test statistic."""

        # Fill lower tail
        xlower = np.arange(lower, lower_critical, 0.001)
        self._ax.fill_between(
            x=xlower,
            y1=0,
            y2=stats.t.pdf(xlower, self._result.dof),
            color=self._canvas.colors.orange,
        )

        # Fill Upper Tail
        xupper = np.arange(upper_critical, upper, 0.001)
        self._ax.fill_between(
            x=xupper,
            y1=0,
            y2=stats.t.pdf(xupper, self._result.dof),
            color=self._canvas.colors.orange,
        )

        # Plot the statistic
        line = self._ax.lines[0]
        xdata = line.get_xydata()[:, 0]
        ydata = line.get_xydata()[:, 1]
        statistic = round(self._result.value, 4)
        try:
            idx = np.where(xdata > self._result.value)[0][0]
            x = xdata[idx]
            y = ydata[idx]
            _ = sns.regplot(
                x=np.array([x]),
                y=np.array([y]),
                scatter=True,
                fit_reg=False,
                marker="o",
                scatter_kws={"s": 100},
                ax=self._ax,
                color=self._canvas.colors.dark_blue,
            )
            self._ax.annotate(
                f"t = {str(statistic)}",
                (x, y),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
            )

            self._ax.annotate(
                "Critical Value",
                (lower_critical, 0),
                textcoords="offset points",
                xytext=(20, 15),
                ha="left",
                arrowprops={"width": 2, "shrink": 0.05},
            )

            self._ax.annotate(
                "Critical Value",
                (upper_critical, 0),
                xycoords="data",
                textcoords="offset points",
                xytext=(-20, 15),
                ha="right",
                arrowprops={"width": 2, "shrink": 0.05},
            )
        except IndexError:
            pass


# ------------------------------------------------------------------------------------------------ #
#                                 CHI SQUARE TEST                                                  #
# ------------------------------------------------------------------------------------------------ #
class X2TestPlot(Plot):  # pragma: no cover
    """Plots results of a Chi-Square Goodness of Fit Test

    Args:
        result (ChiSquareResult): A Student's t-test result object.
        ax (plt.Axes): A matplotlib Axes object. Optional. If  If not none, the ax parameter
            overrides the default set in the base class.
        title (str): The visualization title. Optional
        canvas (SeabornCanvas): A dataclass containing the configuration of the canvas
            for the visualization. Optional.
        args and kwargs passed to the underlying seaborn histplot method.
            See https://seaborn.pydata.org/generated/seaborn.histplot.html for a
            complete list of parameters.
    """

    @inject
    def __init__(
        self,
        result: ChiSquareResult,
        title: str = None,
        canvas: type[SeabornCanvas] = Provide[D8AnalysisContainer.canvas],
        *args,
        **kwargs,
    ) -> None:
        super().__init__(canvas=canvas)
        self._result = result
        self._canvas = canvas
        self._title = title
        self._args = args
        self._kwargs = kwargs

        self._axes = None
        self._fig = None
        sns.set_style(self._canvas.style)

    def plot(self) -> None:
        self._axes = self._axes or self._canvas.config().axes

        # Render the probability distribution
        x = np.linspace(
            stats.chi2.ppf(0.01, self._result.dof), stats.chi2.ppf(0.99, self._result.dof), 100
        )
        y = stats.chi2.pdf(x, self._result.dof)
        self._ax = sns.lineplot(x=x, y=y, markers=False, dashes=False, sort=True, ax=self._ax)

        # Compute reject region
        upper = x[-1]
        upper_alpha = 1 - self._result.alpha
        critical = stats.chi2.ppf(upper_alpha, self._result.dof)
        self._fill_curve(critical=critical, upper=upper)

        self._axes.set_title(
            f"X\u00b2Test Result\n{self._result.result}",
            fontsize=self._canvas.fontsize_title,
        )

        self._ax.set_xlabel(r"$X^2$")
        self._ax.set_ylabel("Probability Density")

    def _fill_curve(self, critical: float, upper: float) -> None:
        """Fills the area under the curve at the value of the hypothesis test statistic."""

        # Fill Upper Tail
        x = np.arange(critical, upper, 0.001)
        self._ax.fill_between(
            x=x,
            y1=0,
            y2=stats.chi2.pdf(x, self._result.dof),
            color=self._canvas.colors.orange,
        )

        # Plot the statistic
        line = self._ax.lines[0]
        xdata = line.get_xydata()[:, 0]
        ydata = line.get_xydata()[:, 1]
        statistic = round(self._result.value, 4)
        try:
            idx = np.where(xdata > self._result.value)[0][0]
            x = xdata[idx]
            y = ydata[idx]
            _ = sns.regplot(
                x=np.array([x]),
                y=np.array([y]),
                scatter=True,
                fit_reg=False,
                marker="o",
                scatter_kws={"s": 100},
                ax=self._ax,
                color=self._canvas.colors.dark_blue,
            )
            self._ax.annotate(
                rf"$X^2$ = {str(statistic)}",
                (x, y),
                textcoords="offset points",
                xytext=(0, 20),
                ha="center",
            )

            self._ax.annotate(
                "Critical Value",
                (critical, 0),
                xycoords="data",
                textcoords="offset points",
                xytext=(-20, 15),
                ha="right",
                arrowprops={"width": 2, "shrink": 0.05},
            )

        except IndexError:
            pass


# ------------------------------------------------------------------------------------------------ #
#                           KOLMOGOROV-SMIRNOV GOF TEST PLOT                                       #
# ------------------------------------------------------------------------------------------------ #
class KSOneTestPlot(Plot):

    """Plots results of a one-sample Kolmogorov-Smirnov test for goodness of fit.

    This test compares the underlying distribution F(x) of a sample against a given continuous
    distribution G(x).

    Args:
        result (KSOneTestResult): A Student's t-test result object.
        ax (plt.Axes): A matplotlib Axes object. Optional. If  If not none, the ax parameter
            overrides the default set in the base class.
        title (str): The visualization title. Optional
        canvas (SeabornCanvas): A dataclass containing the configuration of the canvas
            for the visualization. Optional.
        args and kwargs passed to the underlying seaborn histplot method.
            See https://seaborn.pydata.org/generated/seaborn.histplot.html for a
            complete list of parameters.
    """

    @inject
    def __init__(
        self,
        result: KSOneTestResult,
        title: str = None,
        canvas: type[SeabornCanvas] = Provide[D8AnalysisContainer.canvas],
        *args,
        **kwargs,
    ) -> None:
        super().__init__(canvas=canvas)
        self._result = result
        self._canvas = canvas
        self._title = title
        self._args = args
        self._kwargs = kwargs

        self._axes = None
        self._fig = None
        sns.set_style(self._canvas.style)

    def plot(self) -> None:
        # Two axes, one for pdf, the other for cdf
        fig, (ax1, ax2) = self._canvas.get_figaxes(2)

        # Obtain a distribution object which returns a pdf, and cdf for the reference distribution
        dist = RVSDistribution()
        _, pdf, cdf = dist(data=self._result.data, distribution=self._result.reference_distribution)

        # Plot empirical and theoretical pdfs
        p1 = sns.kdeplot(
            data=self._results.data, color=self._canvas.colors.dark_blue, legend=False, ax=ax1
        )
        p2 = sns.lineplot(x=pdf.x, y=pdf.y, legend=False, ax=ax1)

        # Plot empirical and theoretical cdfs
        p3 = sns.kdeplot(
            data=self._results.data,
            color=self._canvas.colors.dark_blue,
            legend=False,
            ax=ax2,
            cumulative=True,
        )
        p4 = sns.lineplot(x=cdf.x, y=cdf.y, legend=False, ax=ax2)

        # Configure the legends.
        ax1.legend(
            (p1, p2),
            ("Empirical Probability Density Function", "Theoretical Probability Density Function"),
            loc="upper right",
        )
        ax2.legend(
            (p3, p4),
            (
                "Empirical Cumulative Distribution Function",
                "Theoretical Cumulative Distribution Function",
            ),
            loc="upper left",
        )
        fig.suptitle(
            f"Kolmogorov-Smirnov Goodness of Fit\n{self.reference_distribution.capitalize()} Distribution\n{self.result}",
            fontsize=self._canvas.fontsize_title,
        )
        plt.tight_layout()
        plt.show()

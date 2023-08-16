#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.10                                                                             #
# Filename   : /d8analysis/quantitative/inferential/relational/spearman.py                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday June 7th 2023 08:15:08 pm                                                 #
# Modified   : Monday August 14th 2023 08:38:37 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass
import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from dependency_injector.wiring import inject, Provide

from d8analysis.visual.base import Canvas
from d8analysis.container import D8AnalysisContainer
from d8analysis.quantitative.inferential.base import StatTestProfileTwo
from d8analysis.quantitative.inferential.base import (
    StatTestResult,
    StatisticalTest,
    StatTestProfile,
)


# ------------------------------------------------------------------------------------------------ #
#                                     TEST RESULT                                                  #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class SpearmanCorrelationResult(StatTestResult):
    data: pd.DataFrame = None
    a: str = None
    b: str = None
    dof: float = None

    @inject
    def __post_init__(self, canvas: Canvas = Provide[D8AnalysisContainer.canvas.seaborn]) -> None:
        super().__post_init__(canvas=canvas)
        self._ax1 = None
        self._ax2 = None

    def plot(self) -> None:
        """Renders three plots: Test Statistic, Cumulative Distribution and Probability Density Functions."""
        # self.plot_statistic()
        self.plot_data()

    def plot_statistic(self, ax: plt.Axes = None) -> None:
        """Plots the test statistic and reject region

        Args:
            ax (plt.Axes): Matplotlib axes object. Optional. If provided, this will override the current
                value of the axes designated for this plot, if any. Otherwise, if the axes is
                None, one is provided by the canvas object.
        """
        if ax is not None:
            self._ax1 = ax
        elif self._ax1 is None:
            _, self._ax1 = self._canvas.get_figaxes()

        # Render probability density
        self._logger.debug("Rendering probability density")
        dist = stats.t(df=self.dof)
        x = np.linspace(dist.ppf(0.001), dist.ppf(0.999), 500)
        y = dist.pdf(x)
        self._ax1 = sns.lineplot(x=x, y=y, markers=False, dashes=False, sort=True, ax=self._ax1)
        self._logger.debug(f"Len x: {len(x)}")
        self._logger.debug(f"Min x: {min(x)}")
        self._logger.debug(f"Max x: {max(x)}")

        self._logger.debug(f"Len y: {len(y)}")
        self._logger.debug(f"Min y: {min(y)}")
        self._logger.debug(f"Max y: {max(y)}")

        # Transform the r statistic and pvalue as per https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html#scipy.stats.spearmanr
        critical_value = np.abs(
            self.value * np.sqrt(self.dof / ((self.value + 1.0) * (1.0 - self.value)))
        )
        self._logger.debug(f"Computing critical value: {critical_value}")
        pvalue = dist.cdf(-critical_value) + dist.sf(critical_value)
        self._logger.debug(f"Computing p value: {pvalue}")

        # Compute reject region.
        upper = x >= critical_value
        lower = x <= -critical_value
        self._logger.debug(f"Num values greater than critical values {sum(upper)}")
        self._logger.debug(f"Num values less than critical values {sum(lower)}")

        # Plot statistic
        self._logger.debug("Plotting statistic")
        # Plot the statistic
        line = self._ax1.lines[0]
        xdata = line.get_xydata()[:, 0]
        ydata = line.get_xydata()[:, 1]
        statistic = round(self.value, 4)

        idx = np.where(xdata > self.value)[0][0]
        self._logger.debug(f"Statistic index: {idx}")
        a = xdata[idx]
        b = ydata[idx]
        self._logger.debug(f"a: {a}")
        self._logger.debug(f"b: {b}")
        _ = sns.regplot(
            x=[a],
            y=[b],
            scatter=True,
            fit_reg=False,
            marker="o",
            scatter_kws={"s": 100},
            ax=self._ax1,
            color=self._canvas.colors.dark_blue,
        )
        self._logger.debug("Creating Annotation 1.")
        self._ax1.annotate(
            f"r({self.dof})={statistic}, p={round(pvalue,4)}",
            (a, b),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
        )

        self._logger.debug("Filling Lower Tail.")
        # Fill Lower Tail
        self._ax1.fill_between(
            x[lower],
            y1=0,
            y2=y[lower],
            color=self._canvas.colors.orange,
        )

        self._logger.debug("Filling Upper Tail.")
        # Fill Upper Tail
        self._ax1.fill_between(
            x[upper],
            y1=0,
            y2=y[upper],
            color=self._canvas.colors.orange,
        )

        self._logger.debug("Annotating Lower Critical Value.")
        # Create annotations
        self._ax1.annotate(
            "Critical Value",
            (-critical_value, 0),
            textcoords="offset points",
            xytext=(20, 20),
            ha="left",
            arrowprops={"width": 2, "shrink": 0.05, "headwidth": 4},
        )

        self._logger.debug("Annotating Upper Critical Value.")
        self._ax1.annotate(
            "Critical Value",
            (critical_value, 0),
            textcoords="offset points",
            xytext=(-20, 20),
            ha="right",
            arrowprops={"width": 2, "shrink": 0.05, "headwidth": 4},
        )
        plt.show()

        plt.tight_layout()

        self._logger.debug("Plot Statistic Complete.")

    def plot_data(self, ax: plt.Axes = None) -> None:
        """Plots the data.

        Args:
            ax (plt.Axes): Matplotlib axes object. Optional. If provided, this will override the current
                value of the axes designated for this plot, if any. Otherwise, if the axes is
                None, one is provided by the canvas object.
        """

        if ax is not None:
            self._ax2 = ax
        elif self._ax2 is None:
            _, self._ax2 = self._canvas.get_figaxes()

        self._ax2 = sns.regplot(
            data=self.data,
            x=self.a,
            y=self.b,
            ax=self._ax2,
            fit_reg=True,
        )

        self._ax2.set_title(
            f"{self.result}",
            fontsize=self._canvas.fontsize_title,
        )

        # plt.tight_layout()


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class SpearmanCorrelationTest(StatisticalTest):
    __id = "spearman"

    def __init__(self, data: pd.DataFrame, a=str, b=str, alpha: float = 0.05) -> None:
        super().__init__()
        self._data = data
        self._a = a
        self._b = b
        self._alpha = alpha
        self._profile = StatTestProfileTwo.create(self.__id)
        self._result = None

    @property
    def profile(self) -> StatTestProfile:
        """Returns the statistical test profile."""
        return self._profile

    @property
    def result(self) -> StatTestResult:
        """Returns a Statistical Test Result object."""
        return self._result

    def run(self) -> None:
        """Performs the statistical test and creates a result object."""

        r, pvalue = stats.spearmanr(
            a=self._data[self._a].values,
            b=self._data[self._b].values,
            alternative="two-sided",
            nan_policy="omit",
        )

        dof = len(self._data) - 2

        result = self._report_results(r=r, pvalue=pvalue, dof=dof)

        if pvalue > self._alpha:  # pragma: no cover
            inference = f"The two variables had {self._interpret_r(r)}, r({dof})={round(r,2)}, {self._report_pvalue(pvalue)}.\nHowever, the pvalue, {round(pvalue,2)} is greater than level of significance {int(self._alpha*100)}% indicating that the correlation coefficient is not statistically significant."
        else:
            inference = f"The two variables had {self._interpret_r(r)}, r({dof})={round(r,2)}, {self._report_pvalue(pvalue)}.\nFurther, the pvalue, {round(pvalue,2)} is lower than level of significance {int(self._alpha*100)}% indicating that the correlation coefficient is statistically significant."

        # Create the result object.
        self._result = SpearmanCorrelationResult(
            test=self._profile.name,
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            value=r,
            pvalue=pvalue,
            dof=dof,
            result=result,
            data=self._data,
            a=self._a,
            b=self._b,
            inference=inference,
            alpha=self._alpha,
        )

    def _report_results(self, r: float, pvalue: float, dof: float) -> str:
        return f"Spearman Correlation Test\nr({dof})={round(r,3)}, {self._report_pvalue(pvalue)}\n{self._interpret_r(r).capitalize()}"

    def _interpret_r(self, r: float) -> str:
        """Interprets the value of the correlation[1]_

        .. [1] Mukaka MM. Statistics corner: A guide to appropriate use of correlation coefficient in medical research. Malawi Med J. 2012 Sep;24(3):69-71. PMID: 23638278; PMCID: PMC3576830.


        """

        if r < 0:
            direction = "negative"
        else:
            direction = "positive"

        r = abs(r)
        if r >= 0.9:
            return f"very high {direction} correlation"
        elif r >= 0.70:
            return f"high {direction} correlation"
        elif r >= 0.5:
            return f"moderate {direction} correlation"
        elif r >= 0.3:
            return f"low {direction} correlation"
        else:
            return "negligible correlation"

#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /d8analysis/quantitative/inferential/relational/chisquare.py                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday May 29th 2023 03:00:39 am                                                    #
# Modified   : Monday August 14th 2023 03:14:00 pm                                                 #
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
class ChiSquareIndependenceResult(StatTestResult):
    dof: int = None
    data: pd.DataFrame = None
    a: str = None
    b: str = None

    @inject
    def __post_init__(self, canvas: Canvas = Provide[D8AnalysisContainer.canvas.seaborn]) -> None:
        super().__post_init__(canvas=canvas)
        self._ax1 = None
        self._ax2 = None

    def plot(self) -> None:
        """Renders three plots: Test Statistic, Cumulative Distribution and Probability Density Functions."""
        self._fig, (self._ax1, self._ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12, 8))
        self.plot_statistic()
        self.plot_contingency()

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

        # Render the probability distribution
        x = np.linspace(stats.chi2.ppf(0.01, self.dof), stats.chi2.ppf(0.99, self.dof), 100)
        y = stats.chi2.pdf(x, self.dof)
        self._ax1 = sns.lineplot(x=x, y=y, markers=False, dashes=False, sort=True, ax=self._ax1)

        # Compute reject region
        upper = x[-1]
        upper_alpha = 1 - self.alpha
        critical = stats.chi2.ppf(upper_alpha, self.dof)
        self._fill_curve(critical=critical, upper=upper)

        self._ax1.set_title(
            f"{self.result}",
            fontsize=self._canvas.fontsize_title,
        )

        self._ax1.set_xlabel(r"$X^2$")
        self._ax1.set_ylabel("Probability Density")
        plt.tight_layout()

    def _fill_curve(self, critical: float, upper: float) -> None:
        """Fills the area under the curve at the value of the hypothesis test statistic."""

        # Fill Upper Tail
        x = np.arange(critical, upper, 0.001)
        self._ax1.fill_between(
            x=x,
            y1=0,
            y2=stats.chi2.pdf(x, self.dof),
            color=self._canvas.colors.orange,
        )

        # Plot the statistic
        line = self._ax1.lines[0]
        xdata = line.get_xydata()[:, 0]
        ydata = line.get_xydata()[:, 1]
        statistic = round(self.value, 4)
        try:
            idx = np.where(xdata > self.value)[0][0]
            x = xdata[idx]
            y = ydata[idx]
            _ = sns.regplot(
                x=np.array([x]),
                y=np.array([y]),
                scatter=True,
                fit_reg=False,
                marker="o",
                scatter_kws={"s": 100},
                ax=self._ax1,
                color=self._canvas.colors.dark_blue,
            )
            self._ax1.annotate(
                rf"$X^2$ = {str(statistic)}",
                (x, y),
                textcoords="offset points",
                xytext=(0, 20),
                ha="center",
            )

            self._ax1.annotate(
                "Critical Value",
                (critical, 0),
                xycoords="data",
                textcoords="offset points",
                xytext=(-20, 15),
                ha="right",
                arrowprops={"width": 2, "headwidth": 4, "shrink": 0.05},
            )

        except IndexError:
            pass

    def plot_contingency(self, ax: plt.Axes = None) -> None:
        """Plots the contingency table.

        Args:
            ax (plt.Axes): Matplotlib axes object. Optional. If provided, this will override the current
                value of the axes designated for this plot, if any. Otherwise, if the axes is
                None, one is provided by the canvas object.
        """

        if ax is not None:
            self._ax2 = ax
        elif self._ax2 is None:
            _, self._ax2 = self._canvas.get_figaxes()

        self._ax2 = sns.countplot(
            data=self.data, x=self.a, hue=self.b, ax=self._ax2, palette=self._canvas.palette
        )

        title = f"Contingency Table\n{self.a.capitalize()} and {self.b.capitalize()}"
        self._ax2.set_title(title)
        plt.tight_layout()


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class ChiSquareIndependenceTest(StatisticalTest):
    """Chi-Square Test of Independence

    The Chi-Square test of independence is used to determine if there is a significant relationship between two nominal (categorical) variables.  The frequency of each category for one nominal variable is compared across the categories of the second nominal variable.
    """

    __id = "x2ind"

    def __init__(
        self, data: pd.DataFrame, a: str = None, b: str = None, alpha: float = 0.05
    ) -> None:
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

        n = len(self._data)

        obs = stats.contingency.crosstab(self._data[self._a], self._data[self._b])

        statistic, pvalue, dof, exp = stats.chi2_contingency(obs[1])

        result = self._report_results(statistic=statistic, pvalue=pvalue, dof=dof, n=n)

        if pvalue > self._alpha:  # pragma: no cover
            inference = f"The pvalue {round(pvalue,2)} is greater than level of significance {int(self._alpha*100)}%; therefore, the null hypothesis is not rejected. The evidence against independence of {self._a} and {self._b} is not significant."
        else:
            inference = f"The pvalue {round(pvalue,2)} is less than level of significance {int(self._alpha*100)}%; therefore, the null hypothesis is rejected. The evidence against independence of {self._a} and {self._b} is significant."

        # Create the result object.
        self._result = ChiSquareIndependenceResult(
            test=self._profile.name,
            H0=self._profile.H0,
            statistic="X\u00b2",
            hypothesis=self._profile.hypothesis,
            dof=dof,
            value=statistic,
            pvalue=pvalue,
            result=result,
            data=self._data,
            a=self._a,
            b=self._b,
            inference=inference,
            alpha=self._alpha,
        )

    def _report_results(self, statistic: float, pvalue: float, dof: float, n: int) -> str:
        return f"X\u00b2 Test of Independence\n{self._a.capitalize()} and {self._b.capitalize()}\nX\u00b2({dof}, N={n})={round(statistic,2)}, {self._report_pvalue(pvalue)}."

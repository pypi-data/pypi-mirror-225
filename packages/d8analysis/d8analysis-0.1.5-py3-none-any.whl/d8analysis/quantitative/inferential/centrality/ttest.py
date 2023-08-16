#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.10                                                                             #
# Filename   : /d8analysis/quantitative/inferential/centrality/ttest.py                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday June 7th 2023 11:41:00 pm                                                 #
# Modified   : Tuesday August 15th 2023 08:00:44 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass

import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from dependency_injector.wiring import inject, Provide

from d8analysis.container import D8AnalysisContainer
from d8analysis.visual.base import Canvas
from d8analysis.quantitative.inferential.base import (
    StatTestProfileTwo,
    StatTestResult,
    StatisticalTest,
    StatTestProfile,
)
from d8analysis.quantitative.descriptive.continuous import DescriptiveStats


# ------------------------------------------------------------------------------------------------ #
#                                     TEST RESULT                                                  #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class TTestResult(StatTestResult):
    dof: int = None
    homoscedastic: bool = None
    a: np.ndarray = None
    b: np.ndarray = None
    a_stats: DescriptiveStats = None
    b_stats: DescriptiveStats = None

    @inject
    def __post_init__(self, canvas: Canvas = Provide[D8AnalysisContainer.canvas.seaborn]) -> None:
        super().__post_init__(canvas=canvas)
        _, self._ax = self._canvas.get_figaxes()

    def plot(self) -> None:
        """Plots the test statistic and reject region"""

        # Render the probability distribution
        x = np.linspace(stats.t.ppf(0.001, self.dof), stats.t.ppf(0.999, self.dof), 500)
        y = stats.t.pdf(x, self.dof)
        self._ax = sns.lineplot(x=x, y=y, markers=False, dashes=False, sort=True, ax=self._ax)

        # Compute reject region
        lower = x[0]
        upper = x[-1]
        lower_alpha = self.alpha / 2
        upper_alpha = 1 - (self.alpha / 2)
        lower_critical = stats.t.ppf(lower_alpha, self.dof)
        upper_critical = stats.t.ppf(upper_alpha, self.dof)

        self._fill_reject_region(
            lower=lower, upper=upper, lower_critical=lower_critical, upper_critical=upper_critical
        )

        self._ax.set_title(
            "Independent Samples T-Test",
            fontsize=self._canvas.fontsize_title,
        )

        # ax.set_xlabel(r"$X^2$")
        self._ax.set_ylabel("Probability Density")
        plt.tight_layout()

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
            y2=stats.t.pdf(xlower, self.dof),
            color=self._canvas.colors.orange,
        )

        # Fill Upper Tail
        xupper = np.arange(upper_critical, upper, 0.001)
        self._ax.fill_between(
            x=xupper,
            y1=0,
            y2=stats.t.pdf(xupper, self.dof),
            color=self._canvas.colors.orange,
        )

        # Plot the statistic
        line = self._ax.lines[0]
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
                arrowprops={"width": 2, "headwidth": 4, "shrink": 0.05},
            )

            self._ax.annotate(
                "Critical Value",
                (upper_critical, 0),
                xycoords="data",
                textcoords="offset points",
                xytext=(-20, 15),
                ha="right",
                arrowprops={"width": 2, "headwidth": 4, "shrink": 0.05},
            )

            self._ax.text(
                0.5,
                0.5,
                self.result,
                horizontalalignment="center",
                verticalalignment="center",
                transform=self._ax.transAxes,
            )
        except IndexError:
            pass


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class TTest(StatisticalTest):
    """Calculate the T-test for the means of two independent samples of scores.

    This is a test for the null hypothesis that 2 independent samples have identical average
    (expected) values. This test assumes that the populations have identical variances by default.

    Args:
        a: (np.ndarray): An array containing the first of two independent samples.
        b: (np.ndarray): An array containing the second of two independent samples.
        alpha (float): The level of statistical significance for inference.
        homoscedastic (bool): If True, perform a standard independent 2 sample test t
            hat assumes equal population variances. If False, perform Welch’s
            t-test, which does not assume equal population variance.

    """

    __id = "t2"

    def __init__(
        self, a: np.ndarray, b: np.ndarray, alpha: float = 0.05, homoscedastic: bool = False
    ) -> None:
        super().__init__()
        self._a = a
        self._b = b
        self._alpha = alpha
        self._homoscedastic = homoscedastic
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
        """Executes the TTest."""

        statistic, pvalue = stats.ttest_ind(a=self._a, b=self._b, equal_var=self._homoscedastic)

        a_stats = DescriptiveStats.describe(self._a)
        b_stats = DescriptiveStats.describe(self._b)

        dof = len(self._a) + len(self._b) - 2

        result = self._report_results(a_stats, b_stats, dof, statistic, pvalue)

        if pvalue > self._alpha:  # pragma: no cover
            inference = f"The pvalue {round(pvalue,2)} is greater than level of significance {int(self._alpha*100)}%; therefore, the null hypothesis is not rejected. The evidence against identical centers for a and b is not significant."
        else:
            inference = f"The pvalue {round(pvalue,2)} is less than level of significance {int(self._alpha*100)}%; therefore, the null hypothesis is rejected. The evidence against identical centers for a and b is significant."

        # Create the result object.
        self._result = TTestResult(
            test=self._profile.name,
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            homoscedastic=self._homoscedastic,
            dof=dof,
            value=np.abs(statistic),
            pvalue=pvalue,
            result=result,
            a=self._a,
            b=self._b,
            a_stats=a_stats,
            b_stats=b_stats,
            inference=inference,
            alpha=self._alpha,
        )

    def _report_results(self, a_stats, b_stats, dof, statistic, pvalue) -> str:
        return f"Independent Samples t Test\na: (N = {a_stats.count}, M = {round(a_stats.mean,2)}, SD = {round(a_stats.std,2)})\nb: (N = {b_stats.count}, M = {round(b_stats.mean,2)}, SD = {round(b_stats.std,2)})\nt({dof}) = {round(statistic,2)}, {self._report_pvalue(pvalue)} {self._report_alpha()}"

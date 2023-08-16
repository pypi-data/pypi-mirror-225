#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.10                                                                             #
# Filename   : /d8analysis/quantitative/inferential/distribution/kstest.py                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday June 6th 2023 01:45:05 am                                                   #
# Modified   : Monday August 14th 2023 02:40:46 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass
from typing import Union

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from dependency_injector.wiring import inject, Provide

from d8analysis.container import D8AnalysisContainer
from d8analysis.visual.base import Canvas
from d8analysis.quantitative.inferential.base import (
    StatTestProfileOne,
    StatTestResult,
    StatisticalTest,
    StatTestProfile,
)
from d8analysis.data.generation import RVSDistribution


# ------------------------------------------------------------------------------------------------ #
#                                     TEST RESULT                                                  #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class KSTestResult(StatTestResult):
    """Encapsulates the hypothesis test results."""

    a: np.ndarray = None
    b: Union[np.ndarray, str] = None
    a_name: str = "Sample 1"  # Name of Sample
    b_name: str = "Sample 2"  # Name of Sample 2 if two sample test

    @inject
    def __post_init__(self, canvas: Canvas = Provide[D8AnalysisContainer.canvas.seaborn]) -> None:
        super().__post_init__(canvas=canvas)
        self._ax1 = None
        self._ax2 = None
        self._ax3 = None

    def plot(self) -> None:
        self._fig, (self._ax1, self._ax2, self._ax3) = plt.subplots(
            nrows=3, ncols=1, figsize=(12, 12)
        )
        self.plot_statistic()
        self.plot_cdf()
        self.plot_pdf()

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

        n = len(self.a)

        # Render the probability distribution
        x = np.linspace(stats.kstwo.ppf(0.001, n), stats.kstwo.ppf(0.999, n), 500)
        y = stats.kstwo.pdf(x, n)
        self._ax1 = sns.lineplot(x=x, y=y, markers=False, dashes=False, sort=True, ax=self._ax1)

        # Compute reject region
        lower = x[0]
        upper = x[-1]
        lower_alpha = self.alpha / 2
        upper_alpha = 1 - (self.alpha / 2)
        lower_critical = stats.kstwo.ppf(lower_alpha, n)
        upper_critical = stats.kstwo.ppf(upper_alpha, n)

        self._fill_reject_region(
            n=n,
            lower=lower,
            upper=upper,
            lower_critical=lower_critical,
            upper_critical=upper_critical,
        )

        self._ax1.set_title(
            f"Kolmogorov-Smirnov Goodness of Fit\n{self.result}",
            fontsize=self._canvas.fontsize_title,
        )

        self._ax1.set_ylabel("Probability Density")
        plt.tight_layout()

    def _fill_reject_region(
        self,
        n: int,
        lower: float,
        upper: float,
        lower_critical: float,
        upper_critical: float,
    ) -> None:
        """Fills the area under the curve at the value of the hypothesis test statistic."""

        # Fill lower tail
        xlower = np.arange(lower, lower_critical, 0.001)
        self._ax1.fill_between(
            x=xlower,
            y1=0,
            y2=stats.kstwo.pdf(xlower, n),
            color=self._canvas.colors.orange,
        )

        # Fill Upper Tail
        xupper = np.arange(upper_critical, upper, 0.001)
        self._ax1.fill_between(
            x=xupper,
            y1=0,
            y2=stats.kstwo.pdf(xupper, n),
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
                f"D = {str(statistic)}",
                (x, y),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
            )

            self._ax1.annotate(
                "Critical Value",
                (lower_critical, 0),
                textcoords="offset points",
                xytext=(20, 15),
                ha="left",
                arrowprops={"width": 2, "headwidth": 4, "shrink": 0.05},
            )

            self._ax1.annotate(
                "Critical Value",
                (upper_critical, 0),
                xycoords="data",
                textcoords="offset points",
                xytext=(-20, 15),
                ha="right",
                arrowprops={"width": 2, "headwidth": 4, "shrink": 0.05},
            )
        except IndexError:
            pass

    def plot_cdf(self, ax: plt.Axes = None) -> None:
        """Plots the cumulative distribution function for two samples or the sample and the theoretical distribution.

        Args:
            ax (plt.Axes): Matplotlib axes object. Optional. If provided, this will override the current
                value of the axes designated for this plot, if any. Otherwise, if the axes is
                None, one is provided by the canvas object.
        """
        if ax is not None:
            self._ax1 = ax
        elif self._ax2 is None:
            _, self._ax2 = self._canvas.get_figaxes()

        x = self.a

        if isinstance(self.b, str):
            title = "Theoretical and Empirical Cumulative Distribution Function"
            self._ax2 = sns.ecdfplot(
                x=x,
                stat="proportion",
                ax=self._ax2,
                label=f"Empirical Cumulative Distribution Function: {self.a_name}",
                legend=True,
            )
            d = RVSDistribution()
            cdf = d(data=x, distribution=self.b).cdf
            self._ax2 = sns.lineplot(
                x=cdf.x,
                y=cdf.y,
                ax=self._ax2,
                color=self._canvas.colors.orange,
                label=f"Cumulative Distribution Function: {cdf.name}",
                legend=True,
            )
        else:
            title = "Two Sample Cumulative Distribution Function"
            x2 = self.b
            self._ax2 = sns.ecdfplot(
                x=x,
                stat="proportion",
                ax=self._ax2,
                label=f"Empirical Cumulative Distribution Function: {self.a_name}",
                legend=True,
            )
            self._ax2 = sns.ecdfplot(
                x=x2,
                stat="proportion",
                ax=self._ax2,
                color=self._canvas.colors.orange,
                label=f"Empirical Cumulative Distribution Function: {self.b_name}",
                legend=True,
            )

            h2, l2 = self._ax2.get_legend_handles_labels()
            self._ax2.legend(handles=h2, labels=l2, loc="upper left")

        self._ax2.set_title(title, fontsize=self._canvas.fontsize_title)
        plt.tight_layout()

    def plot_pdf(self, ax: plt.Axes = None) -> None:
        """Plots the probability density function for the two samples or sample and theoretical distriubtion.

        Args:
            ax (plt.Axes): Matplotlib axes object. Optional. If provided, this will override the current
                value of the axes designated for this plot, if any. Otherwise, if the axes is
                None, one is provided by the canvas object.
        """
        if ax is not None:
            self._ax3 = ax
        elif self._ax3 is None:
            _, self._ax3 = self._canvas.get_figaxes()

        x = self.a

        if isinstance(self.b, str):
            title = "Theoretical and Empirical Probability Density Function"
            self._ax3 = sns.kdeplot(
                x=x,
                ax=self._ax3,
                label=f"Empirical Probability Density Function: {self.a_name}",
                legend=True,
            )
            d = RVSDistribution()
            pdf = d(data=x, distribution=self.b).pdf
            self._ax3 = sns.lineplot(
                x=pdf.x,
                y=pdf.y,
                ax=self._ax3,
                color=self._canvas.colors.orange,
                label=f"Probability Density Function: {pdf.name} ",
                legend=True,
            )
        else:
            title = "Two Sample Probability Density Function"
            x2 = self.b
            self._ax3 = sns.kdeplot(
                x=x,
                ax=self._ax3,
                label=f"Empirical Probability Density Function: {self.a_name}",
                legend=True,
            )
            self._ax3 = sns.kdeplot(
                x=x2,
                ax=self._ax3,
                color=self._canvas.colors.orange,
                label=f"Empirical Probability Density Function: {self.b_name}",
                legend=True,
            )
            h1, l1 = self._ax3.get_legend_handles_labels()
            self._ax3.legend(handles=h1, labels=l1, loc="upper right")

        self._ax3.set_title(title, fontsize=self._canvas.fontsize_title)
        plt.tight_layout()


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class KSTest(StatisticalTest):
    """Performs the statistical test and creates a result object.

    Args:
        a (np.ndarray): 1D Numpy array of data to be tested.
        b (Union[str, np.ndarray]): A 1-D array, or a string containing the name of the
            reference distribution from the scipy list of Continuous Distributions
            at https://docs.scipy.org/doc/scipy/reference/stats.html
        a_name (str): The name of the sample distribution. Optional.
        b_name (str): The name of the sample 2 distribution, if two-sample test. Optional.

    """

    __id = "kstest"

    def __init__(
        self,
        a: np.ndarray,
        b: Union[str, np.ndarray],
        a_name: str = "Sample 1",
        b_name: str = "Sample 2",
        alpha: float = 0.05,
    ) -> None:
        super().__init__()
        self._a = a
        self._b = b
        self._a_name = a_name
        self._b_name = b_name
        self._alpha = alpha
        self._profile = StatTestProfileOne.create(self.__id)
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

        n = len(self._a)

        # Conduct the two-sided ks test
        try:
            result = stats.kstest(rvs=self._a, cdf=self._b, alternative="two-sided")
        except KeyError as e:
            msg = f"Distribution {self._reference_distribution} is not supported.\n{e}"
            self._logger.error(msg)
            raise

        inference = self._infer(pvalue=result.pvalue)

        interpretation = None
        if len(self._a) < 50:
            interpretation = "Note: The Kolmogorov-Smirnov Test requires a sample size N > 50. For smaller sample sizes, the Shapiro-Wilk test should be considered."
        if len(self._a) > 1000:
            interpretation = "Note: The Kolmogorov-Smirnov Test on large sample sizes may lead to rejections of the null hypothesis that are statistically significant, yet practically insignificant."

        # Create the result object.
        self._result = KSTestResult(
            test=self._profile.name,
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            value=result.statistic,
            pvalue=result.pvalue,
            result=self._report_results(n=n, statistic=result.statistic, pvalue=result.pvalue),
            a=self._a,
            b=self._b,
            a_name=self._a_name,
            b_name=self._b_name,
            inference=inference,
            interpretation=interpretation,
            alpha=self._alpha,
        )

    def _infer(self, pvalue: float) -> str:
        """Formats the inference for the hypothesis based upon whether it is one or two sample"""
        if isinstance(self._b, str):
            if pvalue > self._alpha:
                inference = f"The pvalue {round(pvalue,2)} is greater than level of significance {int(self._alpha*100)}%; therefore, the null hypothesis is not rejected. The evidence against the data being drawn from the {self._b} is not significant."
            else:
                inference = f"The pvalue {round(pvalue,2)} is less than level of significance {int(self._alpha*100)}%; therefore, the null hypothesis is rejected. The evidence against the data being drawn from the {self._b} is significant."
        else:
            if pvalue > self._alpha:
                inference = f"The pvalue {round(pvalue,2)} is greater than level of significance {int(self._alpha*100)}%; therefore, the null hypothesis is not rejected. The evidence against the data being drawn from the same distribution is not significant."
            else:
                inference = f"The pvalue {round(pvalue,2)} is less than level of significance {int(self._alpha*100)}%; therefore, the null hypothesis is rejected. The evidence against the data being drawn from the same distribution is significant."
        return inference

    def _report_results(self, n: int, statistic: float, pvalue: float) -> str:
        """Reports the result in APA style."""
        result = f"D({n})={round(statistic,4)}, p={round(pvalue,3)}"
        return result

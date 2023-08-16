#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.10                                                                             #
# Filename   : /d8analysis/quantitative/inferential/base.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday June 5th 2023 12:13:09 am                                                    #
# Modified   : Tuesday August 15th 2023 08:29:03 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from abc import ABC, abstractmethod
import logging
from dataclasses import dataclass, fields
import seaborn as sns

from d8analysis import DataClass
from d8analysis.service.io import IOService
from d8analysis.visual.base import Canvas

# ------------------------------------------------------------------------------------------------ #
ANALYSIS_TYPES = {
    "univariate": "Univariate",
    "bivariate": "Bivariate",
    "multivariate": "Multivariate",
}
STAT_CONFIG = "config/stats.yml"


# ------------------------------------------------------------------------------------------------ #
@dataclass
class StatTestProfile(DataClass):
    """Abstract base class defining the interface for statistical tests.

    Interface inspired by: https://doc.dataiku.com/dss/latest/statistics/tests.html
    """

    id: str
    name: str = None
    description: str = None
    statistic: str = None
    analysis: str = None  # one of ANALYSIS_TYPES
    hypothesis: str = None  # One of HYPOTHESIS_TYPES
    H0: str = None
    parametric: bool = None
    min_sample_size: int = None
    assumptions: str = None
    use_when: str = None

    @classmethod
    def create(cls, id) -> None:
        """Loads the values from the statistical tests file"""
        profiles = IOService.read(STAT_CONFIG)
        profile = profiles[id]
        fieldlist = {f.name for f in fields(cls) if f.init}
        filtered_dict = {k: v for k, v in profile.items() if k in fieldlist}
        filtered_dict["id"] = id
        return cls(**filtered_dict)


# ------------------------------------------------------------------------------------------------ #
@dataclass
class StatTestProfileOne(StatTestProfile):
    X_variable_type: str = None


# ------------------------------------------------------------------------------------------------ #
@dataclass
class StatTestProfileTwo(StatTestProfile):
    X_variable_type: str = None
    Y_variable_type: str = None


# ------------------------------------------------------------------------------------------------ #
@dataclass
class StatTestResult(DataClass):
    test: str = None
    hypothesis: str = None
    H0: str = None
    statistic: str = None
    value: float = 0
    pvalue: float = 0
    inference: str = None
    alpha: float = 0.05
    result: str = None
    interpretation: str = None

    def __post_init__(self, canvas: Canvas) -> None:
        self._canvas = canvas
        sns.set_style(self._canvas.style)
        sns.set_palette(self._canvas.palette)
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @abstractmethod
    def plot(self, *args, **kwargs) -> None:
        """Renders plots of test statistics, pdf, cdf, data, etc..."""


# ------------------------------------------------------------------------------------------------ #
class StatisticalTest(ABC):
    """Base class for Statistical Tests"""

    def __init__(self, io: IOService = IOService, *args, **kwargs) -> None:
        self._io = io
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    @abstractmethod
    def profile(self) -> StatTestProfile:
        """Returns the statistical test profile."""

    @property
    @abstractmethod
    def result(self) -> StatTestResult:
        """Returns a Statistical Test Result object."""

    @abstractmethod
    def run(self) -> None:
        """Performs the statistical test and creates a result object."""

    def _report_pvalue(self, pvalue: float) -> str:
        """Rounds the pvalue in accordance with the APA Style Guide 7th Edition"""
        if pvalue < 0.001:
            return "p<.001"
        else:
            return "p=" + str(round(pvalue, 4))

    def _report_alpha(self) -> str:
        a = int(self._alpha * 100)
        return f"significant at {a}%."

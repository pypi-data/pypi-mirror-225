#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.10                                                                             #
# Filename   : /d8analysis/quantitative/descriptive/continuous.py                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday June 8th 2023 02:56:56 am                                                  #
# Modified   : Tuesday August 15th 2023 08:08:09 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass
from typing import Union

import pandas as pd
import numpy as np
from scipy import stats

from d8analysis.quantitative.descriptive.base import DescriptiveOne


# ------------------------------------------------------------------------------------------------ #
@dataclass
class DescriptiveStats(DescriptiveOne):
    name: str  # Name of the variable
    length: int  # total  length of variable
    count: int  # number of non-null values
    size: int  # total number of bytes
    min: float
    q25: float
    mean: float
    median: float
    q75: float
    max: float
    range: float
    std: float
    var: float
    skew: float
    kurtosis: float

    @classmethod
    def describe(cls, x: Union[pd.Series, np.ndarray], name: str = None) -> None:
        name = name or cls.get_name(x=x)
        return cls(
            name=name,
            length=len(x),
            count=len(list(filter(None, x))),
            size=x.__sizeof__(),
            mean=np.mean(x),
            std=np.std(x),
            var=np.var(x),
            min=np.min(x),
            q25=np.percentile(x, q=25),
            median=np.median(x),
            q75=np.percentile(x, q=75),
            max=np.max(x),
            range=np.max(x) - np.min(x),
            skew=stats.skew(x),
            kurtosis=stats.kurtosis(x, bias=False),
        )

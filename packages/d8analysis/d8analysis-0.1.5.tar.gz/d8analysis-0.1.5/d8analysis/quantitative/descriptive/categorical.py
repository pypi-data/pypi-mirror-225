#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.10                                                                             #
# Filename   : /d8analysis/quantitative/descriptive/categorical.py                                 #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday June 8th 2023 02:56:56 am                                                  #
# Modified   : Tuesday August 15th 2023 08:25:51 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass
import statistics
from typing import Union

import pandas as pd
import numpy as np

from d8analysis.quantitative.descriptive.base import DescriptiveOne


# ------------------------------------------------------------------------------------------------ #
@dataclass
class DescriptiveStats(DescriptiveOne):
    name: str  # Name of variable
    length: int  # total  length of variable
    count: int  # number of non-null values
    size: float  # total number of bytes
    mode: Union[int, str]
    unique: int

    @classmethod
    def describe(cls, x: Union[pd.Series, np.ndarray], name: str = None) -> None:
        name = name or cls.get_name(x=x)
        return cls(
            name=name,
            length=len(x),
            count=len(list(filter(None, x))),
            size=x.__sizeof__(),
            mode=statistics.mode(x),
            unique=len(np.unique(x)),
        )

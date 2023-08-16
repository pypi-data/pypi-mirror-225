#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /d8analysis/quantitative/descriptive/base.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday August 15th 2023 07:41:35 pm                                                #
# Modified   : Tuesday August 15th 2023 07:53:39 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from abc import abstractclassmethod
from dataclasses import dataclass
from typing import Union

import pandas as pd
import numpy as np

from d8analysis import DataClass


# ------------------------------------------------------------------------------------------------ #
@dataclass
class DescriptiveOne(DataClass):
    """Base class for single-variable descriptive statistics subclasses."""

    @abstractclassmethod
    def describe(self, x: Union[pd.Series, np.ndarray], name: str = None) -> DescriptiveOne:
        """Computes the descriptive statistics for"""

    @classmethod
    def get_name(cls, x: Union[pd.Series, np.ndarray]) -> Union[str, None]:
        if isinstance(x, pd.Series):
            return x.name

#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.10                                                                             #
# Filename   : /d8analysis/quantitative/descriptive/statistics.py                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday June 8th 2023 02:56:56 am                                                  #
# Modified   : Sunday August 13th 2023 07:46:52 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC
from datetime import datetime
from dataclasses import dataclass
from typing import Union

import pandas as pd
import numpy as np
from scipy import stats

from d8analysis import IMMUTABLE_TYPES, SEQUENCE_TYPES

# ------------------------------------------------------------------------------------------------ #


@dataclass
class VarStats(ABC):
    length: int  # total length of variable
    count: int  # Non-null count
    size: int  # Size in memory

    @classmethod
    def compute(cls, x: Union[pd.Series, np.ndarray]) -> None:
        return cls(length=len(x), count=len(list(filter(None, x))), size=x.__sizeof__())

    def __repr__(self) -> str:
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(
                "{}={!r}".format(k, v)
                for k, v in self.__dict__.items()
                if type(v) in IMMUTABLE_TYPES
            ),
        )

    def __str__(self) -> str:
        width = 32
        breadth = width * 2
        s = f"\n\n{self.__class__.__name__.center(breadth, ' ')}"
        d = self.as_dict()
        for k, v in d.items():
            if type(v) in IMMUTABLE_TYPES:
                s += f"\n{k.rjust(width,' ')} | {v}"
        s += "\n\n"
        return s

    def as_dict(self) -> dict:
        """Returns a dictionary representation of the the Config object."""
        return {
            k: self._export_config(v) for k, v in self.__dict__.items() if not k.startswith("_")
        }

    @classmethod
    def _export_config(cls, v):  # pragma: no cover
        """Returns v with Configs converted to dicts, recursively."""
        if isinstance(v, IMMUTABLE_TYPES):
            return v
        elif isinstance(v, SEQUENCE_TYPES):
            return type(v)(map(cls._export_config, v))
        elif isinstance(v, datetime):
            return v
        elif isinstance(v, dict):
            return v
        elif hasattr(v, "as_dict"):
            return v.as_dict()
        else:
            """Else nothing. What do you want?"""

    def as_df(self) -> pd.DataFrame:
        """Returns the project in DataFrame format"""
        d = self.as_dict()
        return pd.DataFrame(data=d, index=[0])


# ------------------------------------------------------------------------------------------------ #
@dataclass
class QuantStats(VarStats):
    mean: float
    std: float
    var: float
    min: float
    q25: float
    median: float
    q75: float
    max: float
    range: float
    skew: float
    kurtosis: float

    @classmethod
    def compute(cls, x: Union[pd.Series, np.ndarray]) -> None:
        return cls(
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


# ------------------------------------------------------------------------------------------------ #
@dataclass
class QualStats(VarStats):
    mode: Union[int, str]
    unique: int
    freq: int

    @classmethod
    def compute(cls, x: Union[pd.Series, np.ndarray]) -> None:
        return cls(
            length=len(x),
            count=len(list(filter(None, x))),
            size=x.__sizeof__(),
            mode=stats.mode(x),
            unique=len(np.unique(x)),
            freq=np.bincount(x).argmax(),
        )

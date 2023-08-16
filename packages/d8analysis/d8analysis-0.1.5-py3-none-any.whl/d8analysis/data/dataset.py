#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /d8analysis/data/dataset.py                                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday August 10th 2023 08:52:00 pm                                               #
# Modified   : Tuesday August 15th 2023 06:11:50 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import pandas as pd

from d8analysis.data.base import Dataset


# ------------------------------------------------------------------------------------------------ #
class CreditScoreDataset(Dataset):
    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__(df=df)

    def __getitem__(self, idx: int) -> pd.Series:
        return self._df.iloc[idx]

    @property
    def summary(self) -> pd.DataFrame:
        return (
            self._df[["Gender", "Education", "Marital Status", "Own", "Credit Rating"]]
            .value_counts()
            .reset_index()
        )

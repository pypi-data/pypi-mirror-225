#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /d8analysis/data/base.py                                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday August 10th 2023 08:29:08 pm                                               #
# Modified   : Tuesday August 15th 2023 06:19:35 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
import logging
from typing import Any, Callable, Union

import pandas as pd


# ------------------------------------------------------------------------------------------------ #
#                                            DATASET                                               #
# ------------------------------------------------------------------------------------------------ #
class Dataset(ABC):
    """Encapsulates tabular data in pandas DataFrame format.

    Args:
        df (pd.DataFrame): Pandas DataFrame object.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def __len__(self):
        """Returns the length of the dataset."""
        return len(self._df)

    @abstractmethod
    def __getitem__(self, idx: int) -> Any:
        """Returns an entity at the designated index"""

    @abstractproperty
    def summary(self) -> pd.DataFrame:
        """Returns a summary of the dataset contents in DataFrame format"""

    @property
    def columns(self) -> list:
        """Returns a list containing the names of the columns in the dataset."""
        return self._df.columns

    @property
    def dtypes(self) -> list:
        """Returns the count of data types in the dataset."""
        dtypes = self._df.dtypes.value_counts().reset_index()
        dtypes.columns = ["Data Type", "Count"]
        return dtypes

    @property
    def size(self) -> int:
        """Returns the size of the Dataset in memory in bytes."""
        return self._df.memory_usage(deep=True).sum()

    # ------------------------------------------------------------------------------------------- #
    @property
    def overview(self) -> pd.DataFrame:
        """Returns an overview of the dataset in terms of its shape and size."""

        nvars = self._df.shape[1]
        nrows = self._df.shape[0]
        ncells = nvars * nrows
        size = self._df.memory_usage(deep=True).sum().sum()
        d = {
            "Number of Observations": nrows,
            "Number of Variables": nvars,
            "Number of Cells": ncells,
            "Size (Bytes)": size,
        }
        overview = pd.DataFrame.from_dict(data=d, orient="index").reset_index()
        overview.columns = ["Characteristic", "Total"]
        return overview

    # ------------------------------------------------------------------------------------------- #
    @property
    def info(self) -> pd.DataFrame:
        """Returns a DataFrame with basic dataset quality statistics"""

        info = self._df.dtypes.to_frame().reset_index()
        info.columns = ["Column", "DataType"]
        info["Valid"] = self._df.count().values
        info["Null"] = self._df.isna().sum().values
        info["Validity"] = info["Valid"] / self._df.shape[0]
        info["Cardinality"] = self._df.nunique().values
        info["Percent Unique"] = self._df.nunique().values / self._df.shape[0]
        info["Size"] = self._df.memory_usage(deep=True, index=False).to_frame().reset_index()[0]
        info = round(info, 2)
        return info

    # ------------------------------------------------------------------------------------------- #
    def as_df(self) -> pd.DataFrame:
        """Returns the dataset as a pandas DataFrame"""
        return self._df

    # ------------------------------------------------------------------------------------------- #
    def sample(
        self, n: int = 5, frac: float = None, replace: bool = False, random_state: int = None
    ) -> pd.DataFrame:
        """Returns a sample from the FOG Dataset

        Args:
            n (int): Number of items to return. Defaults to five.
            frac (float): Proportion of items to return
            replace (bool): Whether to sample with replacement
            random_state (int): Pseudo random seed.
        """
        return self._df.sample(n=n, frac=frac, replace=replace, random_state=random_state)

    # ------------------------------------------------------------------------------------------- #
    def select(self, include: list = None, exclude: list = None) -> pd.DataFrame:
        """Selects columns of the data to be included or excluded.

        Args:
            include (list[str]): List of columns to include. Only values in the dataset columns
                are include. Values that do not exist in the dataset are ignored. No KeyError
                exception is raised.
            exclude (list[str]): List of columns to exclude. If non-Null, include parameter
                is ignored, and all columns will be returned except those indicated
                here.
        """
        if exclude is not None:
            cols = [col for col in self._df.columns if col not in exclude]
        elif include is not None:
            cols = [col for col in self._df.columns if col in include]
        else:
            cols = self._df.columns
        return self._df[cols]

    # ------------------------------------------------------------------------------------------- #
    def subset(self, condition: Callable) -> pd.DataFrame:
        """Subsets the data according to the stated condition.

        Args:
            condition (Callable): Lambda function that will be used to
                subset the data as a pandas dataframe.
                Example condition = lambda df: df['age'] > 18
        """
        try:
            return self._df[condition]
        except Exception as e:
            msg = f"Exception of type {type(e)} occurred.\n{e}"
            self._logger.exception(msg)
            raise

    # ------------------------------------------------------------------------------------------- #
    def head(self, n: int = 5) -> pd.DataFrame:
        return self._df.head(n)

    # ------------------------------------------------------------------------------------------- #
    def describe(
        self,
        include: list[str] = None,
        exclude: list[str] = None,
        groupby: Union[str, list[str]] = None,
    ) -> pd.DataFrame:
        """Provides descriptive statistics for the dataset.

        Args:
            include (list[str]): List of data types to include in the analysis.
            exclude (list[str]): List of data types to exclude from the analysis.
            groupby (str): Column used as a factor variable for descriptive statistics.
        """
        if groupby is None:
            return self._df.describe(include=include, exclude=exclude).T
        else:
            return self._df.groupby(by=groupby).describe(include=include, exclude=exclude)

    # ------------------------------------------------------------------------------------------- #
    def unique(self, columns: list = None) -> pd.DataFrame:
        """Returns a DataFrame containing the unique values for all or the designated columns.

        Args:
            columns (list): List of columns for which unique values are to be returned.
        """
        if columns is not None:
            return self._df[columns].drop_duplicates().reset_index(drop=True)
        else:
            return self._df.drop_duplicates().reset_index(drop=True)

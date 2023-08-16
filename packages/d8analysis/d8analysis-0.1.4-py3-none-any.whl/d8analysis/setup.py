#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.0.9                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /d8analysis/setup.py                                                                #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday June 5th 2023 04:58:20 pm                                                    #
# Modified   : Thursday August 10th 2023 10:27:33 pm                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging  # pragma: no cover

import pandas as pd  # pragma: no cover

from d8analysis.service.io import IOService  # pragma: no cover

# ------------------------------------------------------------------------------------------------ #
SOURCE = "notes/Statistical Tests.xlsx"  # pragma: no cover
DEST = "config/stats.yml"  # pragma: no cover
# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)  # pragma: no cover


def get_stat_tests(source: str) -> pd.DataFrame:  # pragma: no cover
    return pd.read_excel(source, sheet_name="stats", index_col="id")


def save_as_yaml(df: pd.DataFrame, destination: str) -> None:  # pragma: no cover
    d = df.to_dict(orient="index")
    IOService.write(filepath=destination, data=d)


def report(df: pd.DataFrame) -> None:  # pragma: no cover
    report = df[["name", "analysis", "hypothesis", "H0"]]
    print(f"Statistical Tests Loaded\n{report}")


def main():  # pragma: no cover
    df = get_stat_tests(source=SOURCE)
    save_as_yaml(df=df, destination=DEST)
    report(df=df)


if __name__ == "__main__":  # pragma: no cover
    main()

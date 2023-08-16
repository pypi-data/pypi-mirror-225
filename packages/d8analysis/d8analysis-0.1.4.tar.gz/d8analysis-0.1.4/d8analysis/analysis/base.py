#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.10                                                                             #
# Filename   : /d8analysis/analysis/base.py                                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday June 5th 2023 12:13:09 am                                                    #
# Modified   : Monday August 14th 2023 07:50:22 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
import logging
from dataclasses import dataclass

from d8analysis import DataClass

logging.getLogger("matplotlib").setLevel(logging.WARNING)
# ------------------------------------------------------------------------------------------------ #


class Analysis(ABC):
    """Defines the interface for analysis classes."""

    def __init__(self, *args, **kwargs) -> None:
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @abstractproperty
    def result(self) -> Result:
        """Returns a Result object for the analysis"""

    @abstractmethod
    def run(self) -> None:
        """Executes the analysis"""


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Result(DataClass):
    """Base class for all results"""

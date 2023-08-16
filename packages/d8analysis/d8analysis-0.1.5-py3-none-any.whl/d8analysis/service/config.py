#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /d8analysis/service/config.py                                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday August 15th 2023 05:36:24 pm                                                #
# Modified   : Tuesday August 15th 2023 05:50:54 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from d8analysis.service.io import IOService


# ------------------------------------------------------------------------------------------------ #
class LoggingConfig:  # pragma: no cover
    """Manages logging configuration"""

    __filepath = "config/logging.yml"

    @classmethod
    def get(cls) -> dict:
        """Returns the configuration"""
        return IOService.read(cls.__filepath)

    @classmethod
    def get_level(cls) -> str:
        """Retursn logging level for the console."""

        config = IOService.read(cls.__filepath)
        return config["logging"]["handlers"]["console"]["level"]

    @classmethod
    def set_level(cls, level: str = "DEBUG") -> None:
        """Sets logging level for the console.

        Args:
            level (str): The logging level in all caps.
        """

        config = IOService.read(cls.__filepath)
        config["logging"]["handlers"]["console"]["level"] = level
        IOService.write(cls.__filepath, data=config)

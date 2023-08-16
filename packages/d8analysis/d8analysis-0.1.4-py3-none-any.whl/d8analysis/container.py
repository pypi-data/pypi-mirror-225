#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.10                                                                             #
# Filename   : /d8analysis/container.py                                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 07:02:56 pm                                                  #
# Modified   : Sunday August 13th 2023 11:41:00 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Framework Dependency Container"""
import logging.config  # pragma: no cover

from dependency_injector import containers, providers

from d8analysis.visual.seaborn.config import SeabornCanvas
from d8analysis.visual.seaborn.plot import SeabornVisualizer


# ------------------------------------------------------------------------------------------------ #
#                                        LOGGING                                                   #
# ------------------------------------------------------------------------------------------------ #
class LoggingContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config,
    )


# ------------------------------------------------------------------------------------------------ #
#                                    VISUALIZER CONTAINER                                          #
# ------------------------------------------------------------------------------------------------ #
class VisualizerContainer(containers.DeclarativeContainer):
    canvas = providers.Dependency()
    seaborn = providers.Factory(SeabornVisualizer, canvas=canvas)


# ------------------------------------------------------------------------------------------------ #
#                                     CANVAS CONTAINER                                             #
# ------------------------------------------------------------------------------------------------ #
class CanvasContainer(containers.DeclarativeContainer):
    seaborn = providers.Factory(SeabornCanvas)


# ------------------------------------------------------------------------------------------------ #
#                                          FRAMEWORK                                               #
# ------------------------------------------------------------------------------------------------ #
class D8AnalysisContainer(containers.DeclarativeContainer):
    log_config = providers.Configuration(yaml_files=["config/logging.yml"])

    logs = providers.Container(LoggingContainer, config=log_config.logging)

    canvas = providers.Container(CanvasContainer)

    visualizer = providers.Container(VisualizerContainer, canvas=canvas.seaborn)

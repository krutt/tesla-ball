#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/tasks/demo.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-06 19:33
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

from logging import getLogger


def task() -> None:
    logger = getLogger(__name__)
    logger.info("This is a sample job")


__all__ = ["task"]

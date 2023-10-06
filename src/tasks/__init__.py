#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/tasks/__init__.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-06 19:33
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Local modules ###
from src.tasks.open_channel import task as open_channel_task
from src.tasks.demo import task as demo_task

__all__ = ["demo_task", "open_channel_task"]

#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/models/order_state.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-11 00:00
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:

# *************************************************************
### Standard packages ###
from enum import Enum


class OrderState(str, Enum):
    """
    Enumeration Class for `state` column
    """

    PENDING: str = "pending"
    COMPLETED: str = "completed"
    REJECTED: str = "rejected"

#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/models/earn_order.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-08 16:53
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module defining `EarnOrder` ORM-model
"""

### Local modules ###
from src.models.order import Order


class EarnOrder(Order):
  """Class mapping Object Relation to table `earn_order`"""

  class Meta:
    table: str = "earn_order"


__all__ = ["EarnOrder"]

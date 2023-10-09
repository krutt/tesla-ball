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

### Third-party packages ###
from tortoise.fields import IntField
from tortoise.models import Model


class EarnOrder(Model):
    """Class mapping Object Relation to table `earn_order`"""

    id: IntField = IntField(pk=True)


__all__ = ["EarnOrder"]

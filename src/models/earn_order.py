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

### Standard packages ###
from datetime import datetime
from uuid import UUID, uuid4 as uuid

### Third-party packages ###
from tortoise.fields import DatetimeField, IntField, UUIDField
from tortoise.models import Model


class EarnOrder(Model):
    """Class mapping Object Relation to table `earn_order`"""

    class Meta:
        table: str = "earn_order"

    ### Identifier fields ###
    id: int = IntField(pk=True)
    order_id: UUID = UUIDField(default=uuid())  # Set once at creation, never changed

    ### Datetime fields ###
    created_at: datetime = DatetimeField(auto_now_add=True)
    updated_at: datetime = DatetimeField(auto_now=True)


__all__ = ["EarnOrder"]

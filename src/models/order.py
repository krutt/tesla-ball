#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/models/order.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-11 00:00
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:

# *************************************************************

### Standard packages ###
from datetime import datetime
from enum import Enum
from typing import List
from uuid import UUID, uuid4 as uuid

### Third-party packages ###
from tortoise.models import Model
from tortoise.fields import CharEnumField, DatetimeField, IntField, UUIDField


class OrderState(str, Enum):
    """Enumeration Class for `state` column"""

    PENDING: str = "pending"
    PAID: str = "paid"
    OPENING: str = "opening"
    COMPLETED: str = "completed"
    REJECTED: str = "rejected"


class Order(Model):
    """Abstract ORM-model to be based upon by subclasses"""

    class Meta:
        abstract: bool = True

    ### Identifier fields ###
    id: int = IntField(pk=True)
    order_id: UUID = UUIDField(default=uuid())  # Set once at creation, never changed

    ### State-machine enumeration field ###
    state: str = CharEnumField(OrderState, default=OrderState.PENDING)

    ### Datetime fields ###
    created_at: datetime = DatetimeField(auto_now_add=True)
    updated_at: datetime = DatetimeField(auto_now=True)

    @classmethod
    async def completed(cls) -> List["Order"]:
        return await cls.filter(state=OrderState.COMPLETED)

    @classmethod
    async def paid(cls) -> List["Order"]:
        return await cls.filter(state=OrderState.PAID)

    @classmethod
    async def opening(cls) -> List["Order"]:
        return await cls.filter(state=OrderState.OPENING)

    @classmethod
    async def pending(cls) -> List["Order"]:
        return await cls.filter(state=OrderState.PENDING)

    @classmethod
    async def rejected(cls) -> List["Order"]:
        return await cls.filter(state=OrderState.REJECTED)


__all__ = ["Order", "OrderState"]

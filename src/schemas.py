#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:    ~~/src/schemas.py
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
from typing_extensions import Self
from uuid import UUID, uuid4 as uuid

### Third-party packages ###
from tortoise.fields import CharEnumField, CharField, DatetimeField, IntField, UUIDField
from tortoise.models import Model


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
  order_id: UUID = UUIDField(default=uuid)  # Set once at creation, never changed

  ### State-machine enumeration field ###
  state: str = CharEnumField(OrderState, default=OrderState.PENDING)

  ### Datetime fields ###
  created_at: datetime = DatetimeField(auto_now_add=True)
  updated_at: datetime = DatetimeField(auto_now=True)

  @classmethod
  async def completed(cls) -> List[Self]:
    return await cls.filter(state=OrderState.COMPLETED)

  @classmethod
  async def paid(cls) -> List[Self]:
    return await cls.filter(state=OrderState.PAID)

  @classmethod
  async def opening(cls) -> List[Self]:
    return await cls.filter(state=OrderState.OPENING)

  @classmethod
  async def pending(cls) -> List[Self]:
    return await cls.filter(state=OrderState.PENDING)

  @classmethod
  async def rejected(cls) -> List[Self]:
    return await cls.filter(state=OrderState.REJECTED)


### Subclasses ###
class EarnOrder(Order):
  """Class mapping Object Relation to table `earn_order`"""

  class Meta:
    table: str = "earn_order"


class InboundOrder(Order):
  """Class mapping Object Relation to table `inbound_order`"""

  class Meta:
    table: str = "inbound_order"

  ### Data fields ###
  bolt11: str = CharField(max_length=379, null=True)  # type: ignore[assignment]
  fee_rate: int = IntField(default=6)
  host: str = CharField(max_length=255)  # type: ignore[assignment]
  port: int = IntField(default=9735)
  pubkey: str = CharField(max_length=66)  # type: ignore[assignment]
  remote_balance: int = IntField(default=20_000)
  txid: str = CharField(max_length=255, null=True)  # type: ignore[assignment]


class SwapType(str, Enum):
  REVERSE: str = "reverse"
  SUBMARINE: str = "submarine"


class SwapOrder(Order):
  """Class mapping Object Relation to table `swap_order`"""

  class Meta:
    table: str = "swap_order"

  ### Data fields ###
  claim_pubkey: str = CharField(max_length=255)  # type: ignore[assignment]
  expected_amount: int = IntField(max=25_000_000, min=50_000)
  lockup: str = CharField(max_length=64)  # type: ignore[assignment]
  pre_image: str = CharField(max_length=255)  # type: ignore[assignment]
  refund_pubkey: str = CharField(max_length=255)  # type: ignore[assignment]
  swap_type: SwapType = CharEnumField(SwapType, default=SwapType.SUBMARINE)
  txid: str = CharField(max_length=255, null=True)  # type: ignore[assignment]


__all__ = ["EarnOrder", "InboundOrder", Self, "OrderState", "SwapOrder", "SwapType"]

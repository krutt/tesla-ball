#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/models/inbound_order.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-08 16:53
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module defining `InboundOrder` ORM-model
"""

### Standard packages ###
from datetime import datetime
from uuid import UUID, uuid4 as uuid

### Third-party packages ###
from tortoise.fields import CharField, CharEnumField, DatetimeField, IntField, UUIDField
from tortoise.models import Model

### Local modules ###
from src.models.order_state import OrderState


class InboundOrder(Model):
    """Class mapping Object Relation to table `inbound_order`"""

    class Meta:
        table: str = "inbound_order"

    ### Identifier fields ###
    id: int = IntField(pk=True)
    order_id: UUID = UUIDField(default=uuid())  # Set once at creation, never changed

    ### Data fields ###
    fee_rate: int = IntField(default=6)  # tentative, economy fee in 2023
    host: str = CharField(max_length=255)
    invoice: str = CharField(max_length=379, null=True)
    port: int = IntField(default=9735)
    pubkey: str = CharField(max_length=66)
    remote_balance: int = IntField(default=20_000)  # defaults to minimum channel open size for LND
    state: str = CharEnumField(OrderState, default=OrderState.PENDING)
    txid: str = CharField(max_length=255, null=True)

    ### Datetime fields ###
    created_at: datetime = DatetimeField(auto_now_add=True)
    updated_at: datetime = DatetimeField(auto_now=True)


__all__ = ["InboundOrder"]

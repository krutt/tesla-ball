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

### Third-party packages ###
from tortoise.fields import CharField, IntField

### Local modules ###
from src.models.order import Order


class InboundOrder(Order):
    """Class mapping Object Relation to table `inbound_order`"""

    class Meta:
        table: str = "inbound_order"

    ### Data fields ###
    fee_rate: int = IntField(default=6)  # tentative, economy fee in 2023
    host: str = CharField(max_length=255)
    invoice: str = CharField(max_length=379, null=True)
    port: int = IntField(default=9735)
    pubkey: str = CharField(max_length=66)
    remote_balance: int = IntField(default=20_000)  # defaults to minimum channel open size for LND
    txid: str = CharField(max_length=255, null=True)


__all__ = ["InboundOrder"]

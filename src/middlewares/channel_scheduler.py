#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/middlewares/channel_scheduler.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-06 19:33
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from binascii import hexlify
from typing import List

### Third-party packages ###
### v3.10.4 API ###
from apscheduler.schedulers.asyncio import AsyncIOScheduler as AsyncScheduler

### TODO: v4.0.0a3 API ###
# from apscheduler import AsyncScheduler
from grpc import RpcError
from starlette.types import ASGIApp

### Local modules ###
from src.middlewares.scheduler import SchedulerMiddleware
from src.models import OrderState, InboundOrder
from src.services.lightning import ChannelPoint, Lightning


async def task() -> None:
    lightning: Lightning = Lightning()
    orders: List[InboundOrder] = await InboundOrder.filter(state=OrderState.PENDING)
    for order in orders:
        try:
            lightning.connect_peer(host=order.host, pubkey=order.pubkey)
        except RpcError as err:
            if "already connected to peer: " not in str(err):
                order.state = OrderState.COMPLETED
                await order.save()
        try:
            channel_point: ChannelPoint = lightning.open_channel(
                amount=order.remote_balance,
                pubkey=order.pubkey,
                sat_per_byte=order.fee_rate,
            )
            order.txid = hexlify(channel_point.funding_txid_bytes).decode()
            await order.save()
        except RpcError as err:
            if "Number of pending channels exceed maximum" in str(err):
                print("[WARN] Cannot open any more channels at current block, try again later.")
                break
            elif "channels cannot be created before the wallet is fully synced" in str(err):
                print("[WARN] LND currently not synchronized and therefore cannot open channel.")
                break
            else:
                order.state = OrderState.REJECTED
                await order.save()


class ChannelSchedulerMiddleware(SchedulerMiddleware):
    def __init__(self, app: ASGIApp, interval: int, scheduler: AsyncScheduler) -> None:
        self.app = app
        self.interval = interval
        self.scheduler = scheduler
        self.task = task


__all__ = ["ChannelSchedulerMiddleware"]

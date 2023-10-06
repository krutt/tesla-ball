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
from uuid import UUID, uuid4 as uuid

### Third-party packages ###
### v3.10.4 API ###
from apscheduler.schedulers.asyncio import AsyncIOScheduler as AsyncScheduler

### TODO: v4.0.0a3 API ###
# from apscheduler import AsyncScheduler
from grpc import RpcError
from pydantic import BaseModel, Field, StrictInt, StrictStr
from starlette.types import ASGIApp

### Local modules ###
from src.middlewares import SchedulerMiddleware
from src.services.lightning import ChannelPoint, Lightning


class InboundTicket(BaseModel):
    bolt11: StrictStr
    fee_rate: StrictInt
    host: StrictStr
    pubkey: StrictStr
    remote_balance: StrictInt
    uuid: UUID = Field(default=uuid(), description="Ticket unique identifier")


def task(inbound_ticket: InboundTicket) -> None:
    lightning: Lightning = Lightning()
    try:
        lightning.connect_peer(host=inbound_ticket.host, pubkey=inbound_ticket.pubkey)
    except RpcError as err:
        if "already connected to peer: " not in str(err):
            # return {"detail": "Failed to connect to peer"}
            pass
    try:
        channel_point: ChannelPoint = lightning.open_channel(
            amount=inbound_ticket.remote_balance,
            pubkey=inbound_ticket.pubkey,
            sat_per_byte=inbound_ticket.fee_rate,
        )
        # return {"txid": hexlify(channel_point.funding_txid_bytes).decode()}
        pass
    except RpcError as err:
        if "Number of pending channels exceed maximum" in str(err):
            # response.status_code = 503
            # return {"detail": "Cannot open any more channels at current block, try again later."}
            pass
        else:
            # response.status_code = 502
            # return {"detail": "Unable to open new channel"}
            pass


class ChannelSchedulerMiddleware(SchedulerMiddleware):
    def __init__(self, app: ASGIApp, scheduler: AsyncScheduler) -> None:
        self.app = app
        self.interval = 300  # 5 minutes
        self.scheduler = scheduler
        self.task = task


__all__ = ["ChannelSchedulerMiddleware"]

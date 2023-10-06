#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/tasks/open_channel.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-06 19:33
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from binascii import hexlify
from uuid import UUID4 as UUID, uuid4 as uuid

### Third-party packages ###
from grpc import RpcError
from pydantic import BaseModel, Field, StrictInt, StrictStr

### Local modules ###
from src.services.lightning import ChannelPoint, Lightning


class InboundTicket(BaseModel):
    bolt11: StrictStr
    fee_rate: StrictStr
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
        return {"txid": hexlify(channel_point.funding_txid_bytes).decode()}
    except RpcError as err:
        if "Number of pending channels exceed maximum" in str(err):
            # response.status_code = 503
            # return {"detail": "Cannot open any more channels at current block, try again later."}
            pass
        else:
            # response.status_code = 502
            # return {"detail": "Unable to open new channel"}
            pass


__all__ = ["task"]

#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/jobs/channel_open.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-14 17:12
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from binascii import hexlify
from typing import List

### Third-party packages ###
from grpc import RpcError

### Local modules ###
from src.models import OrderState, InboundOrder
from src.services.lightning import ChannelPoint, Lightning


async def job() -> None:
    lightning: Lightning = Lightning()
    orders: List[InboundOrder] = await InboundOrder.paid()  # type: ignore[assignment]
    for order in orders:
        try:
            lightning.connect_peer(host=order.host, pubkey=order.pubkey)
        except RpcError as err:
            if "already connected to peer: " not in str(err):
                print("[WARN] Unable to find targeted host or connect to it.")
                continue
        try:
            channel_point: ChannelPoint = lightning.open_channel(
                amount=order.remote_balance,
                pubkey=order.pubkey,
                sat_per_byte=order.fee_rate,
            )
            order.txid = hexlify(channel_point.funding_txid_bytes).decode()
            order.state = OrderState.OPENING
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


__all__ = ["job"]

#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:    ~~/src/jobs/txn_confirm.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-16 11:20
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import List

### Local modules ###
from src.schemas import InboundOrder, OrderState
from src.services.lightning import Lightning, ListChannelsResponse, PendingChannelsResponse


async def job() -> None:
  lightning: Lightning = Lightning()
  orders: List[InboundOrder] = await InboundOrder.opening()  # type: ignore[assignment]
  funding_txids: List[str] = list(map(lambda order: order.txid, orders))
  pending_response: PendingChannelsResponse = lightning.pending_channels()
  for channel in pending_response.pending_open_channels:
    dixt, _ = channel.channel.channel_point.split(":")
    dixt_twos: List[str] = [dixt[i : i + 2] for i in range(0, len(dixt), 2)]
    txid_twos: List[str] = list(reversed(dixt_twos))
    txid: str = "".join(txid_twos)
    if txid in funding_txids:
      funding_txids.remove(txid)
  if len(funding_txids) == 0:
    return
  response: ListChannelsResponse = lightning.list_channels()
  funded_txids: List[str] = []
  for channel in response.channels:
    dixt, _ = channel.channel_point.split(":")  # type: ignore[no-redef]
    dixt_twos: List[str] = [dixt[i : i + 2] for i in range(0, len(dixt), 2)]  # type: ignore[no-redef]
    txid_twos: List[str] = list(reversed(dixt_twos))  # type: ignore[no-redef]
    txid: str = "".join(txid_twos)  # type: ignore[no-redef]
    if txid in funding_txids:
      funded_txids.append(txid)
  for txid in funded_txids:
    order: InboundOrder = await InboundOrder.get(txid=txid)
    order.state = OrderState.COMPLETED
    await order.save()


__all__ = ["job"]

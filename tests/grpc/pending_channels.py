#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/tests/grpc/pending_channels.py
# VERSION: 	   0.1.0
# CREATED: 	   2024-01-16 13:40
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from binascii import hexlify
from typing import List

### Third-party packages ###
from pytest import mark

### Local modules ###
from src.services.lightning import ChannelPoint, Lightning, PendingChannelsResponse
from tests import LND_TARGET_PUBKEY as PUBKEY
from tests.grpc import lightning


def test_01_empty_pending_channels(lightning: Lightning) -> None:
  pending_response: PendingChannelsResponse = lightning.pending_channels()
  assert pending_response is not None
  assert pending_response.pending_open_channels is not None
  assert len(pending_response.pending_open_channels) == 0


@mark.parametrize(
  "remote_balance, pubkey, fee_rate",
  [(120_000, PUBKEY, 3)],
)
def test_02_one_pending_channel(
  fee_rate: int, lightning: Lightning, pubkey: str, remote_balance: int
) -> None:
  channel_point: ChannelPoint = lightning.open_channel(
    amount=remote_balance,
    pubkey=pubkey,
    sat_per_byte=fee_rate,
  )
  assert channel_point is not None
  funding_txid: str = hexlify(channel_point.funding_txid_bytes).decode()
  assert funding_txid is not None
  assert isinstance(funding_txid, str)
  assert len(funding_txid) == 64
  pending_response: PendingChannelsResponse = lightning.pending_channels()
  assert pending_response is not None
  assert pending_response.pending_open_channels is not None
  assert len(pending_response.pending_open_channels) == 1
  channel = pending_response.pending_open_channels[0].channel
  assert channel is not None
  assert isinstance(channel.capacity, int)
  assert channel.capacity == remote_balance
  assert isinstance(channel.channel_point, str)
  dixt, _ = channel.channel_point.split(":")
  dixt_twos: List[str] = [dixt[i : i + 2] for i in range(0, len(dixt), 2)]
  txid_twos: List[str] = list(reversed(dixt_twos))
  txid: str = "".join(txid_twos)
  assert txid == funding_txid

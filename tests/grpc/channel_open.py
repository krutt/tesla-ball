#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/tests/grpc/channel_open.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-28 00:58
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from binascii import hexlify

### Third-party packages ###
from pytest import mark, raises
from grpc import RpcError

### Local modules ###
from src.services.lightning import ChannelPoint, Lightning
from tests import LND_TARGET_PUBKEY as PUBKEY
from tests.grpc import lightning


@mark.parametrize(
  "remote_balance, pubkey, fee_rate",
  [
    (120_000, PUBKEY, 3),
  ],
)
def test_01_open_valid_channel(
  fee_rate: int, lightning: Lightning, pubkey: str, remote_balance: int
) -> None:
  channel_point: ChannelPoint = lightning.open_channel(
    amount=remote_balance,
    pubkey=pubkey,
    sat_per_byte=fee_rate,
  )
  funding_txid: str = hexlify(channel_point.funding_txid_bytes).decode()
  assert funding_txid is not None
  assert isinstance(funding_txid, str)
  assert len(funding_txid) == 64


@mark.parametrize(
  "fee_rate, exc_message, pubkey, remote_balance",
  [
    (100, '"channel is too small, the minimum channel size is: 20000 SAT"', PUBKEY, 19_999),
    (
      100,
      '"funding amount is too large, the max channel size is: 0.16777215 BTC"',
      PUBKEY,
      16_777_216,
    ),
  ],
)
def test_02_attempt_invalid_channel(
  fee_rate: int, exc_message: str, lightning: Lightning, pubkey: str, remote_balance: int
) -> None:
  with raises(RpcError) as exc_info:
    lightning.open_channel(
      amount=remote_balance,
      pubkey=pubkey,
      sat_per_byte=fee_rate,
    )
  assert exc_info.match(exc_message)

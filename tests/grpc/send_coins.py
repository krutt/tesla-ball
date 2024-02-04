#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:  ~~/tests/grpc/send_coins.py
# VERSION: 	 0.1.0
# CREATED: 	 2024-02-04 15:29
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from grpc import RpcError
from pytest import mark, raises


### Local modules ###
from src.services import AddrResponse, Lightning, SendCoinsResponse, WalletKit
from tests.grpc import lightning, wallet_kit


@mark.parametrize("amount", [1_000, 10_000, 100_000])
def test_01_send_coins(amount: int, lightning: Lightning, wallet_kit: WalletKit) -> None:
  addr_response: AddrResponse = wallet_kit.request_address()
  address: str = addr_response.addr
  send_coins_response: SendCoinsResponse = lightning.send_coins(address, amount)
  assert send_coins_response is not None
  assert send_coins_response.txid is not None
  assert isinstance(send_coins_response.txid, str)
  assert len(send_coins_response.txid) == 64


@mark.parametrize("amount", [1, 10, 100])
def test_02_send_dust_failed(amount: int, lightning: Lightning, wallet_kit: WalletKit) -> None:
  addr_response: AddrResponse = wallet_kit.request_address()
  address: str = addr_response.addr
  with raises(RpcError) as exc_info:
    lightning.send_coins(address, amount)
  assert exc_info.match("transaction output is dust")

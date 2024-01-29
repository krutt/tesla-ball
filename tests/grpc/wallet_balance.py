#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:    ~~/tests/grpc/wallet_balance.py
# VERSION: 	   0.1.0
# CREATED: 	   2024-01-16 14:14
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Local modules ###
from src.services.lightning import Lightning, WalletBalanceResponse
from tests.grpc import lightning


def test_wallet_balance(lightning: Lightning) -> None:
  wallet_balance: WalletBalanceResponse = lightning.wallet_balance()
  assert wallet_balance is not None
  assert wallet_balance.total_balance is not None
  assert isinstance(wallet_balance.total_balance, int)
  assert wallet_balance.confirmed_balance is not None
  assert isinstance(wallet_balance.confirmed_balance, int)
  assert wallet_balance.unconfirmed_balance is not None
  assert isinstance(wallet_balance.unconfirmed_balance, int)
  assert wallet_balance.account_balance is not None
  assert wallet_balance.reserved_balance_anchor_chan is not None
  assert isinstance(wallet_balance.reserved_balance_anchor_chan, int)

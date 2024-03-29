#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:    ~~/tests/grpc/estimate_fee.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-11-02 14:45
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Local modules ###
from src.services import EstimateFeeResponse, WalletKit
from tests.grpc import wallet_kit


def test_estimate_fee(wallet_kit: WalletKit) -> None:
  fee_estimate: EstimateFeeResponse = wallet_kit.estimate_fee()
  assert isinstance(fee_estimate, EstimateFeeResponse)
  assert isinstance(fee_estimate.sat_per_kw, int)
  assert fee_estimate.sat_per_kw == 12500  # testnet
  sat_per_vbyte = fee_estimate.sat_per_kw / 4_000
  assert sat_per_vbyte == 3.125

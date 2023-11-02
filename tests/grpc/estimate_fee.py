#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/tests/grpc/estimate_fee.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-11-02 14:45
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Local modules ###
from src.services.walletkit import EstimateFeeResponse, WalletKit


def test_01_estimate_fee() -> None:
    wallet_kit: WalletKit = WalletKit()
    fee_estimate: EstimateFeeResponse = wallet_kit.estimate_fee()
    assert isinstance(fee_estimate, EstimateFeeResponse)
    assert isinstance(fee_estimate.sat_per_kw, int)
    assert fee_estimate.sat_per_kw == 12500  # testnet
    sat_per_vbyte = fee_estimate.sat_per_kw / 4_000
    assert sat_per_vbyte == 3.125

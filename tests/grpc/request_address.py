#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/tests/grpc/request_address.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-11-25 14:37
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Local modules ###
from src.services import AddrResponse, WalletKit
from tests.grpc import wallet_kit


def test_01_request_address(wallet_kit: WalletKit) -> None:
    addr_response: AddrResponse = wallet_kit.request_address()
    assert addr_response.addr is not None
    assert isinstance(addr_response.addr, str)
    assert len(addr_response.addr) == 44

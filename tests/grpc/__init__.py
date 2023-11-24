#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/tests/grpc/__init__.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-28 00:58
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module defining reusable fixtures used for gRPC testing
"""

### Third-party packages ###
from pytest import fixture

### Local modules ###
from src.services import Lightning, WalletKit


@fixture(scope="session")
def lightning() -> Lightning:
    return Lightning()


@fixture(scope="session")
def wallet_kit() -> WalletKit:
    return WalletKit()


__all__ = ["lightning", "wallet_kit"]

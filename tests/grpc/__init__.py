#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023-2024 All rights reserved.
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
from src.services import ChainKit, Lightning, WalletKit
from tests import LND_EXTERNAL_MACAROON, LND_EXTERNAL_TLSCERT, LND_EXTERNAL_URL


@fixture(scope="session")
def chain_kit() -> ChainKit:
  return ChainKit()


@fixture(scope="session")
def external_lightning() -> Lightning:
  return Lightning(
    macaroon_path=LND_EXTERNAL_MACAROON, tlscert_path=LND_EXTERNAL_TLSCERT, url=LND_EXTERNAL_URL
  )


@fixture(scope="session")
def lightning() -> Lightning:
  return Lightning()


@fixture(scope="session")
def wallet_kit() -> WalletKit:
  return WalletKit()


__all__ = ["chain_kit", "external_lightning", "lightning", "wallet_kit"]

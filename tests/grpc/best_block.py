#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:    ~~/tests/grpc/request_address.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-11-25 16:28
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Local modules ###
from src.services import ChainKit, GetBestBlockResponse
from tests.grpc import chain_kit


def test_best_block(chain_kit: ChainKit) -> None:
  best_block: GetBestBlockResponse = chain_kit.best_block()
  assert best_block.block_hash is not None
  assert isinstance(best_block.block_hash, bytes)
  assert best_block.block_height is not None
  assert isinstance(best_block.block_height, int)

#!/usr/bin/env python3.9
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:  ~~/tests/routes/swap.py
# VERSION: 	 0.1.0
# CREATED: 	 2023-11-25 11:06
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from random import choices
from string import ascii_letters
from typing import Dict, Generator, Union

### Third-party packages ###
from bitcoin import SelectParams
from fastapi.testclient import TestClient
from httpx import Response
from pytest import fixture, mark
from orjson import dumps

### Local modules ###
from tests import LND_TARGET_PUBKEY, test_tesla_ball


@fixture(autouse=True, scope="module")
def setup_teardown() -> Generator:
  SelectParams("regtest")
  yield
  SelectParams("mainnet")

@mark.asyncio
async def test_01_submarine_swap(test_tesla_ball: TestClient) -> None:
  params_list: list = ["amount", "claimPubkey", "preImage"]
  amount: int = 560
  claim_pubkey: str = LND_TARGET_PUBKEY
  pre_image: str = "".join(choices(ascii_letters, k=64))
  body: Dict[str, Union[int, str]] = dict(zip(params_list, [amount, claim_pubkey, pre_image]))
  response: Response = test_tesla_ball.post("/swap", content=dumps(body))
  assert response.text is not None
  assert isinstance(response.text, str)

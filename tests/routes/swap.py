#!/usr/bin/env python3.9
# Copyright (C) 2023 All rights reserved.
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
from typing import Dict, Union

### Third-party packages ###
from fastapi.testclient import TestClient
from httpx import Response
from pytest import mark
from orjson import dumps

### Local modules ###
from tests import test_tesla_ball


@mark.asyncio
async def test_01_submarine_swap(test_tesla_ball: TestClient) -> None:
  params_list: list = ["amount", "claimPubkey", "preImage"]
  amount: int = 560
  # TODO: use external lnd to create claim pubkey
  claim_pubkey: str = "03f8109578aae1e5cfc497e466cf6ae6625497cd31886e87b2f4f54f3f0f46b539"
  pre_image: str = "".join(choices(ascii_letters, k=64))
  body: Dict[str, Union[int, str]] = dict(zip(params_list, [amount, claim_pubkey, pre_image]))
  response: Response = test_tesla_ball.post("/swap", content=dumps(body))
  assert response.text is not None
  assert isinstance(response.text, str)

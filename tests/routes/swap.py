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
from typing import Any, Dict, Optional, Generator

### Third-party packages ###
from bitcoin import SelectParams
from fastapi.testclient import TestClient
from httpx import Response
from orjson import dumps
from pytest import fixture, mark

### Local modules ###
from src.schemas import SwapOrder
from src.services import AddrResponse, WalletKit
from tests import tesla_ball
from tests.grpc import wallet_kit
from tests.routes import setup_teardown_database


@fixture(autouse=True, scope="module")
def setup_teardown() -> Generator:
  SelectParams("regtest")
  yield
  SelectParams("mainnet")


@mark.asyncio
async def test_01_submarine_swap(wallet_kit: WalletKit, tesla_ball: TestClient) -> None:
  addr_response: AddrResponse = wallet_kit.request_address()
  claim_address: str = addr_response.addr
  addr_response = wallet_kit.request_address()
  refund_address: str = addr_response.addr
  response: Response = tesla_ball.post(
    "/swap",
    content=dumps(
      {
        "amount": 560,
        "claimAddress": claim_address,
        "preImage": "".join(choices("0123456789abcdef", k=64)),
        "refundAddress": refund_address,
      }
    ),
  )
  data: Dict[str, Any] = response.json()
  assert data is not None
  assert data.get("expectedAmount", None) is not None
  assert isinstance(data["expectedAmount"], int)
  assert data.get("lockup", None) is not None
  assert isinstance(data["lockup"], str)
  swap_order: Optional[SwapOrder] = await SwapOrder.all().order_by("-id").first()
  assert swap_order is not None
  assert swap_order.expected_amount == data["expectedAmount"]
  assert swap_order.lockup == data["lockup"]

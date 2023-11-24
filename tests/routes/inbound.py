#!/usr/bin/env python3.9
# Copyright (C) 2023 All rights reserved.
# FILENAME:  ~~/tests/routes/inbound.py
# VERSION: 	 0.1.0
# CREATED: 	 2023-10-04 23:52
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, Generator, Optional, Union

### Third-party packages ###
from fastapi.testclient import TestClient
from httpx import Response
from orjson import dumps
from pytest import fixture, mark
from tortoise import Tortoise, run_async

### Local modules ###
from src.models import InboundOrder, OrderState
from tests import LND_TARGET_HOST, LND_TARGET_PUBKEY, test_tesla_ball


### Module-specific setup-teardown ###
@fixture(scope="module", autouse=True)
def setup_teardown() -> Generator:
    run_async(Tortoise.init(db_url="sqlite://./tests/test.db", modules={"models": ["src.models"]}))
    run_async(Tortoise.generate_schemas(True))

    yield

    # run_async(InboundOrder.all().delete())
    run_async(Tortoise._drop_databases())
    run_async(Tortoise.close_connections())


@mark.asyncio
async def test_00_precheck_empty_orders(test_tesla_ball: TestClient) -> None:
    """Pre-checks the table for InboundOrder and asserts count to be null or zero"""
    assert await InboundOrder.all().count() is 0


@mark.asyncio
async def test_01_create_inbound_order(test_tesla_ball: TestClient) -> None:
    body: Dict[str, Union[int, str]] = {
        "feeRate": 3,
        "nodeUri": f"{ LND_TARGET_PUBKEY }@{ LND_TARGET_HOST }:9735",
        "remoteBalance": 200_000,
    }
    response: Response = test_tesla_ball.post("/inbound", content=dumps(body))
    assert response.status_code == 200
    order: Optional[InboundOrder] = await InboundOrder.all().order_by("-id").first()
    assert order is not None
    assert response.json().get("bolt11", None) is not None
    assert len(response.json().get("bolt11", None)) in {378, 379}  # regtest invoice lengths
    assert response.json().get("bolt11", None)[:6] == "lnbcrt"  # lightning bitcoin regtest
    assert response.json().get("orderId", None) is not None
    assert response.json().get("orderId", None) == str(order.order_id)


@mark.asyncio
async def test_02_check_inbound_request(test_tesla_ball: TestClient) -> None:
    order: Optional[InboundOrder] = await InboundOrder.all().order_by("-id").first()
    assert order is not None
    response: Response = test_tesla_ball.get(f"/inbound?orderId={ order.order_id }")
    assert response.status_code == 200
    assert response.json().get("bolt11", None) is not None
    assert isinstance(response.json().get("bolt11", None), str)
    assert len(response.json().get("bolt11", None)) in {378, 379}  # regtest invoice lengths
    assert response.json().get("bolt11", None)[:6] == "lnbcrt"  # lightning bitcoin regtest
    assert response.json().get("bolt11", None) == order.bolt11
    assert response.json().get("feeRate", None) is not None
    assert isinstance(response.json().get("feeRate", None), int)
    assert response.json().get("feeRate", None) == order.fee_rate
    assert response.json().get("orderId", None) is not None
    assert isinstance(response.json().get("orderId", None), str)
    assert response.json().get("orderId", None) == str(order.order_id)
    assert len(response.json().get("orderId", None).split("-")) == 5  # dumb test for UUID
    assert response.json().get("remoteBalance", None) is not None
    assert isinstance(response.json().get("remoteBalance", None), int)
    assert response.json().get("remoteBalance", None) == order.remote_balance
    assert response.json().get("state", None) is not None
    assert response.json().get("state", None) == OrderState.PENDING  # not yet paid
    assert response.json().get("state", None) == order.state

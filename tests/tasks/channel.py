#!/usr/bin/env python3.9
# Copyright (C) 2023 All rights reserved.
# FILENAME:  ~~/tests/tasks/channel.py
# VERSION: 	 0.1.0
# CREATED: 	 2023-10-14 15:20
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
### Standard packages ###
from typing import Dict, Generator, Union

### Third-party packages ###
from fastapi.testclient import TestClient
from orjson import dumps
from pytest import fixture, mark
from tortoise import Tortoise, run_async

### Local modules ###
# from src.services.lightning import Lightning
from src.middlewares.channel_scheduler import task as channel_task
from src.models import InboundOrder
from tests import LND_TARGET_HOST, LND_TARGET_PUBKEY, test_tesla_ball


### Module-specific setup-teardown ###
@fixture(scope="module", autouse=True)
def setup_teardown() -> Generator:
    run_async(Tortoise.init(db_url="sqlite://./tests/test.db", modules={"models": ["src.models"]}))
    run_async(Tortoise.generate_schemas(True))

    yield

    run_async(InboundOrder.all().delete())
    run_async(Tortoise._drop_databases())
    run_async(Tortoise.close_connections())


@mark.asyncio
async def test_01_open_channel(test_tesla_ball: TestClient) -> None:
    body: Dict[str, Union[int, str]] = {
        "feeRate": 3,
        "nodeUri": f"{ LND_TARGET_PUBKEY }@{ LND_TARGET_HOST }:9735",
        "remoteBalance": 200_000,
    }
    test_tesla_ball.post("/inbound", content=dumps(body))

    order: InboundOrder = await InboundOrder.all().order_by("-id").first()
    assert order.state == "pending"
    order.state = "paid"
    await order.save()  # pending -> paid
    await channel_task()
    order = await InboundOrder.get(order_id=order.order_id)
    assert order.state == "completed"

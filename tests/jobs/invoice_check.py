#!/usr/bin/env python3.9
# Copyright (C) 2023 All rights reserved.
# FILENAME:  ~~/tests/jobs/invoice_check.py
# VERSION: 	 0.1.0
# CREATED: 	 2023-10-14 19:17
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, Generator, Optional, Union

### Third-party packages ###
from fastapi.testclient import TestClient
from orjson import dumps
from pytest import fixture, mark
from tortoise import Tortoise, run_async

### Local modules ###

from src.jobs.invoice_check import job as invoice_check_job
from src.models import InboundOrder, OrderState
from src.services.lightning import Lightning
from tests import (
    LND_EXTERNAL_MACAROON,
    LND_EXTERNAL_TLSCERT,
    LND_EXTERNAL_URL,
    LND_TARGET_HOST,
    LND_TARGET_PUBKEY,
    test_tesla_ball,
)


### Module-specific setup-teardown ###
@fixture(scope="module", autouse=True)
def setup_teardown() -> Generator:
    run_async(Tortoise.init(db_url="sqlite://./test.db", modules={"models": ["src.models"]}))
    run_async(Tortoise.generate_schemas(True))

    yield

    # run_async(InboundOrder.all().delete())
    run_async(Tortoise._drop_databases())
    run_async(Tortoise.close_connections())


@mark.asyncio
async def test_01_check_invoice(test_tesla_ball: TestClient) -> None:
    body: Dict[str, Union[int, str]] = {
        "feeRate": 3,
        "nodeUri": f"{ LND_TARGET_PUBKEY }@{ LND_TARGET_HOST }:9735",
        "remoteBalance": 200_000,
    }
    test_tesla_ball.post("/inbound", content=dumps(body))
    order: Optional[InboundOrder] = await InboundOrder.all().order_by("-id").first()
    assert order is not None
    assert order.state == OrderState.PENDING

    ### Run job ###
    await invoice_check_job()

    ### Assertion completion ###
    order = await InboundOrder.get(order_id=order.order_id)
    assert order.state == OrderState.PENDING


@mark.asyncio
async def test_02_check_invoice_after_paid(test_tesla_ball: TestClient) -> None:
    body: Dict[str, Union[int, str]] = {
        "feeRate": 3,
        "nodeUri": f"{ LND_TARGET_PUBKEY }@{ LND_TARGET_HOST }:9735",
        "remoteBalance": 200_000,
    }
    test_tesla_ball.post("/inbound", content=dumps(body))
    order: Optional[InboundOrder] = await InboundOrder.all().order_by("-id").first()
    assert order is not None
    assert order.state == OrderState.PENDING

    ### Pay invoice ###
    lightning: Lightning = Lightning(
        macaroon_path=LND_EXTERNAL_MACAROON, tlscert_path=LND_EXTERNAL_TLSCERT, url=LND_EXTERNAL_URL
    )
    lightning.send_payment(order.bolt11)

    ### Run job ###
    await invoice_check_job()

    ### Assertion completion ###
    order = await InboundOrder.get(order_id=order.order_id)
    assert order.state == OrderState.PAID

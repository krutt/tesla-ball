#!/usr/bin/env python3.9
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:  ~~/tests/jobs/txn_confirm.py
# VERSION: 	 0.1.0
# CREATED: 	 2023-10-14 19:17
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from time import sleep
from typing import Dict, Generator, Optional, Union

### Third-party packages ###
from fastapi.testclient import TestClient
from orjson import dumps
from pytest import fixture, mark
from tortoise import Tortoise, run_async

### Local modules ###
from src.jobs import channel_open_job, invoice_check_job, txn_confirm_job
from src.schema import InboundOrder, OrderState
from src.services.lightning import Lightning
from tests import (
  LND_EXTERNAL_MACAROON,
  LND_EXTERNAL_TLSCERT,
  LND_EXTERNAL_URL,
  LND_TARGET_HOST,
  LND_TARGET_PUBKEY,
  TEST_BLOCK_TIME,
  test_tesla_ball,
)


### Module-specific setup-teardown ###
@fixture(scope="module", autouse=True)
def setup_teardown() -> Generator:
  run_async(Tortoise.init(db_url="sqlite://./test.db", modules={"models": ["src.schema"]}))
  run_async(Tortoise.generate_schemas(True))

  yield

  # run_async(InboundOrder.all().delete())
  run_async(Tortoise._drop_databases())
  run_async(Tortoise.close_connections())


@mark.asyncio
async def test_01_check_pending_channels(test_tesla_ball: TestClient) -> None:
  body: Dict[str, Union[int, str]] = {
    "feeRate": 3,
    "nodeUri": f"{ LND_TARGET_PUBKEY }@{ LND_TARGET_HOST }:9735",
    "remoteBalance": 200_000,
  }
  test_tesla_ball.post("/inbound", content=dumps(body))
  order: Optional[InboundOrder] = await InboundOrder.all().order_by("-id").first()
  assert order is not None
  lightning: Lightning = Lightning(
    macaroon_path=LND_EXTERNAL_MACAROON, tlscert_path=LND_EXTERNAL_TLSCERT, url=LND_EXTERNAL_URL
  )
  lightning.send_payment(order.bolt11)
  await invoice_check_job()
  order = await InboundOrder.get(order_id=order.order_id)
  assert order.state == OrderState.PAID
  await channel_open_job()
  order = await InboundOrder.get(order_id=order.order_id)
  assert order.state == OrderState.OPENING

  sleep(TEST_BLOCK_TIME * 6)  # wait for 6 confirmations
  await txn_confirm_job()
  order = await InboundOrder.get(order_id=order.order_id)
  assert order.state == OrderState.COMPLETED

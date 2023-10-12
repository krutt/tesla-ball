#!/usr/bin/env python3.9
# Copyright (C) 2023 All rights reserved.
# FILENAME:  ~~/tests/inbound.py
# VERSION: 	 0.1.0
# CREATED: 	 2023-10-04 23:52
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, Generator, Union

### Third-party packages ###
from fastapi.testclient import TestClient
from httpx import Response
from orjson import dumps
from pytest import fixture
from tortoise import Tortoise, run_async

### Local modules ###
# from src.services.lightning import Lightning
from tests import LND_TARGET_HOST, LND_TARGET_PUBKEY, test_tesla_ball


### Module-specific setup-teardown ###
@fixture(scope="module", autouse=True)
def setup_teardown() -> Generator:
    run_async(Tortoise.init(db_url="sqlite://./test.db", modules={"models": ["src.models"]}))
    run_async(Tortoise.generate_schemas(True))

    yield

    run_async(Tortoise.close_connections())


def test_create_inbound_liquidity_request(test_tesla_ball: TestClient) -> None:
    body: Dict[str, Union[int, str]] = {
        "feeRate": 3,
        "nodeUri": f"{ LND_TARGET_PUBKEY }@{ LND_TARGET_HOST }:9735",
        "remoteBalance": 200_000,
    }
    response: Response = test_tesla_ball.post("/inbound", content=dumps(body))
    assert response.status_code == 200
    print(response.json())
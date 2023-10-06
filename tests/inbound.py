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
from typing import Dict, Union

### Third-party packages ###
from fastapi.testclient import TestClient
from httpx import Response
from orjson import dumps
from pytest import fixture

### Local modules ###
from tests import LND_TARGET_HOST, LND_TARGET_PUBKEY, test_tesla_ball


### Module-specific teardown ###
@fixture(scope="module", autouse=True)
def teardown() -> None:
    yield
    from src.services.lightning import Lightning

    lightning: Lightning = Lightning()
    print(lightning.disconnect_peer(LND_TARGET_PUBKEY))


def test_check_inbound_liquidity_info(test_tesla_ball: TestClient) -> None:
    response: Response = test_tesla_ball.get("/inbound")
    assert response.status_code == 200
    assert response.json() == {"detail": "OK"}


def test_create_inbound_liquidity_request(test_tesla_ball: TestClient) -> None:
    body: Dict[str, Union[int, str]] = {
        "amount": 20_000,
        "host": LND_TARGET_HOST or "",
        "pubkey": LND_TARGET_PUBKEY or "",
        # TODO: Sat Per Byte
    }
    response: Response = test_tesla_ball.post("/inbound", content=dumps(body))
    assert response.status_code == 200
    assert "txid" in response.json().keys()
    txid: str = response.json().get("txid", None)
    assert txid not in ("", None)
    assert len(txid) == 64

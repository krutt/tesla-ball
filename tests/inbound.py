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

### Third-party packages ###
from fastapi.testclient import TestClient
from httpx import Response

### Local modules ###
from . import test_tesla_ball


def test_create_inbound_liquidity_request(test_tesla_ball: TestClient) -> None:
    response: Response = test_tesla_ball.get("/inbound")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
    print(response.json())

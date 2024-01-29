#!/usr/bin/env python3.9
# Copyright (C) 2023 All rights reserved.
# FILENAME:  ~~/tests/routes/info.py
# VERSION: 	 0.1.0
# CREATED: 	 2023-10-19 14:49
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Optional

### Third-party packages ###
from fastapi.testclient import TestClient
from httpx import Response
from pytest import mark

### Local modules ###
from tests import test_tesla_ball


@mark.asyncio
async def test_01_get_node_info(test_tesla_ball: TestClient) -> None:
  response: Response = test_tesla_ball.get("/info")
  assert response.status_code == 200
  node_uri: Optional[str] = response.json().get("nodeUri", None)
  assert node_uri is not None
  pubkey, endpoint = node_uri.split("@")
  assert len(pubkey) == 66  # dumb test for aezeed hash
  host, port = endpoint.split(":")
  assert len(host.split(".")) == 4  # dumb test for ip-address
  assert port == "9735"

#!/usr/bin/env python3.9
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:  ~~/tests/__init__.py
# VERSION: 	 0.1.0
# CREATED: 	 2023-10-04 23:52
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard Packages ###
from os import environ
from typing import Optional

### Third-Party Packages ###
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture

### Local modules ###
from src.routes import earn_router, inbound_router, info_router, swap_router

try:
  from dotenv import load_dotenv

  load_dotenv("test.env")
except ImportError:
  pass


LND_EXTERNAL_MACAROON: Optional[str] = environ.get("LND_EXTERNAL_MACAROON", None)
LND_EXTERNAL_TLSCERT: Optional[str] = environ.get("LND_EXTERNAL_TLSCERT", None)
LND_EXTERNAL_URL: str = environ.get("LND_EXTERNAL_URL", "localhost:10010")
LND_HOST_URL: str = environ.get("LND_HOST_URL", "localhost:10009")
LND_MACAROON_PATH: Optional[str] = environ.get("LND_MACAROON_PATH", None)
LND_TARGET_HOST: Optional[str] = environ.get("LND_TARGET_HOST", None)
LND_TARGET_PUBKEY: Optional[str] = environ.get("LND_TARGET_PUBKEY", None)
LND_TLSCERT_PATH: Optional[str] = environ.get("LND_TLSCERT_PATH", None)
TEST_BLOCK_TIME: int = int(environ.get("TEST_BLOCK_TIME", "5"))
TEST_DB_PATH: str = environ.get("TEST_DB_PATH", "sqlite://./tests/test.db")


@fixture
def tesla_ball() -> TestClient:
  """
  Sets up a FastAPI TestClient wrapped around Tesla Ball application

  ---
  :returns: TestClient
  """
  app = FastAPI()
  app.include_router(earn_router)
  app.include_router(inbound_router)
  app.include_router(info_router)
  app.include_router(swap_router)
  return TestClient(app)


__all__ = [
  "LND_EXTERNAL_MACAROON",
  "LND_EXTERNAL_TLSCERT",
  "LND_EXTERNAL_URL",
  "LND_HOST_URL",
  "LND_MACAROON_PATH",
  "LND_TARGET_HOST",
  "LND_TARGET_PUBKEY",
  "LND_TLSCERT_PATH",
  "TEST_BLOCK_TIME",
  "TEST_DB_PATH",
  "tesla_ball",
]

#!/usr/bin/env python3.9
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:  ~~/tests/routes/__init__.py
# VERSION: 	 0.1.0
# CREATED: 	 2023-10-14 14:39
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
"""

### Standard packages ###
from typing import Generator

### Third-party packages ###
from pytest import fixture
from tortoise import Tortoise, run_async

### Local modules ###
from tests import TEST_DB_PATH


@fixture(scope="module", autouse=True)
def setup_teardown_database() -> Generator:
  run_async(Tortoise.init(db_url=TEST_DB_PATH, modules={"models": ["src.models"]}))
  run_async(Tortoise.generate_schemas(True))

  yield

  # run_async(InboundOrder.all().delete())
  run_async(Tortoise._drop_databases())
  run_async(Tortoise.close_connections())


__all__ = ["setup_teardown_database"]

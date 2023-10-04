#!/usr/bin/env python3.9
# Copyright (C) 2023 All rights reserved.
# FILENAME:  ~~/tests/__init__.py
# VERSION: 	 0.1.0
# CREATED: 	 2023-10-04 23:52
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard Packages ###
from pytest import fixture

### Third-Party Packages ###
from fastapi.testclient import TestClient

### Local modules ###
from serve import app


@fixture
def test_tesla_ball() -> TestClient:
    """
    Sets up a FastAPI TestClient wrapped around Tesla Ball application

    ---
    :returns: TestClient
    """
    return TestClient(app)

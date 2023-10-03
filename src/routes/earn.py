#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/routes/earn.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-04 00:15
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
Module defining earning opportunity endpoints using Lightning's force-closures as a method to clear
up lazy capital for a reward
"""

### Standard packages ###
from typing import Dict

### Third-party packages ###
from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRouter

### Local modules ###
from src.configs import LND_HOST_URL
from src.services.lightning import Lightning

### Routing ###
router: APIRouter = APIRouter(
    prefix="/earn",
    tags=["Earn endpoint"],
    responses={404: {"description": "Not Found"}},
)

# TODO: define routes


@router.get("", response_class=ORJSONResponse)
def get_earn() -> Dict[str, str]:
    lightning: Lightning = Lightning()
    print(lightning.get_info())
    return {"status": "OK"}


__all__ = ["router"]

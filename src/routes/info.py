#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/routes/info.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-19 14:16
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
Module defining node information when one wants to open an outbound channel with us and / or inquire
about capacity / price for outbound channel
"""

### Standard packages ###
from typing import Dict

### Third-party packages ###
from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRouter

### Local modules ###
from src.services import GetInfoResponse, Lightning

### Routing ###
router: APIRouter = APIRouter(
  prefix="/info",
  tags=["Node information endpoint"],
  responses={404: {"detail": "Not Found"}},
)


@router.get("", response_class=ORJSONResponse)
async def get_info() -> Dict[str, str]:
  lightning: Lightning = Lightning()
  info_response: GetInfoResponse = lightning.get_info()
  node_uri: str = info_response.uris[0]
  return {"nodeUri": node_uri}


__all__ = ["router"]

#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/routes/inbound.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-04 00:15
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
Module detailing inbound liquidity purchase endpoints used for creating channels between this node
and requester's node
"""

### Standard packages ###
from typing import Dict

### Third-party packages ###
from fastapi.routing import APIRouter
from fastapi.responses import ORJSONResponse
from grpc import RpcError
from pydantic import BaseModel, StrictInt, StrictStr

### Local modules ###
from src.services.lightning import Lightning

### Routing ###
router: APIRouter = APIRouter(
    prefix="/inbound",
    tags=["Inbound liquidity purchase endpoints"],
    responses={404: {"description": "Not Found"}},
)


class InboundPurchase(BaseModel):
    amount: StrictInt
    host: StrictStr
    pubkey: StrictStr


@router.get("", response_class=ORJSONResponse)
def check_purchase_info() -> Dict[str, str]:
    lightning: Lightning = Lightning()
    print(lightning.get_info())
    return {"detail": "OK"}


@router.post("", response_class=ORJSONResponse)
def request_inbound_channel(purchase: InboundPurchase, response: ORJSONResponse) -> Dict[str, str]:
    lightning: Lightning = Lightning()
    try:
        print(lightning.connect_peer(host=purchase.host, pubkey=purchase.pubkey))
    except RpcError:
        response.status_code = 502
        return {"detail": "Failed to connect to peer"}
    try:
        print(lightning.open_channel(amount=purchase.amount, pubkey=purchase.pubkey, sat_per_byte=20))
    except RpcError:
        response.status_code = 502
        return {"detail": "Unable to open new channel"}
    return {"detail": "OK"}


__all__ = ["router"]

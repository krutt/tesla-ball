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
from typing import Dict, Optional, Union
from uuid import UUID

### Third-party packages ###
from fastapi.routing import APIRouter
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel, Field, StrictInt, StrictStr
from tortoise.exceptions import DoesNotExist, IntegrityError, ValidationError

### Local modules ###
from src.models import InboundOrder

### Routing ###
router: APIRouter = APIRouter(
    prefix="/inbound",
    tags=["Inbound liquidity purchase endpoints"],
    responses={404: {"detail": "Not Found"}},
)


class InboundPurchase(BaseModel):
    fee_rate: Optional[StrictInt] = Field(
        alias="feeRate",
        description="the on-chain fee rate for the channel opening transaction in satoshis/vbyte. "
        "If not set, will default to next-block fee rate.",
    )
    node_uri: StrictStr = Field(
        alias="nodeUri",
        description="connection information to your node with the following format "
        "`pubkey@host:port`",
    )
    remote_balance: StrictInt = Field(
        alias="remoteBalance",
        description="the amount of liquidity desired on this side of the channel, in satoshis "
        "inbound toward `nodeUri` field",
    )


@router.get("", response_class=ORJSONResponse)
async def check_purchase_info(
    orderId: UUID, response: ORJSONResponse
) -> Dict[str, Union[UUID, int, str]]:
    try:
        inbound_order: InboundOrder = await InboundOrder.get(order_id=orderId)
        return {
            "feeRate": inbound_order.fee_rate,
            "orderId": inbound_order.order_id,
            "remoteBalance": inbound_order.remote_balance,
            "state": inbound_order.state,
        }
    except DoesNotExist:
        response.status_code = 404
        return {"detail": "Not found"}


@router.post("", response_class=ORJSONResponse)
async def request_inbound_channel(
    purchase: InboundPurchase, response: ORJSONResponse
) -> Dict[str, Union[UUID, str]]:
    pubkey, url = purchase.node_uri.split("@")
    host, port_str = url.split(":")
    port: int = int(port_str)
    try:
        inbound_order: InboundOrder = await InboundOrder.create(host=host, port=port, pubkey=pubkey)
        return {"orderId": inbound_order.order_id}
    except ValidationError as err:
        response.status_code = 400
        return {"detail": str(err)}
    except IntegrityError:
        response.status_code = 502
        return {"detail": "Unable to receive order"}


__all__ = ["router"]

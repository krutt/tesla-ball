#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023-2024 All rights reserved.
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
from math import ceil
from typing import Dict, Optional, Union
from uuid import UUID

### Third-party packages ###
from fastapi import BackgroundTasks
from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field, StrictInt, StrictStr
from tortoise.exceptions import DoesNotExist, IntegrityError, ValidationError

### Local modules ###
from src.configs import LIQUIDITY_FEE_PPM as FEE_PPM, ONCHAIN_BYTES_EST
from src.schemas import InboundOrder
from src.services.lightning import AddInvoiceResponse, Lightning
from src.services.wallet_kit import EstimateFeeResponse, WalletKit

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
    order: InboundOrder = await InboundOrder.get(order_id=orderId)
    return {
      "bolt11": order.bolt11 or "",
      "feeRate": order.fee_rate,
      "orderId": order.order_id,
      "remoteBalance": order.remote_balance,
      "state": order.state,
    }
  except DoesNotExist:
    response.status_code = 404
    return {"detail": "Not found"}


@router.post("", response_class=ORJSONResponse)
async def request_inbound_channel(
  background_tasks: BackgroundTasks, purchase: InboundPurchase, response: ORJSONResponse
) -> Dict[str, Union[UUID, str]]:
  pubkey, url = purchase.node_uri.split("@")
  host, port_str = url.split(":")
  port: int = int(port_str)

  fee_rate: Optional[int] = purchase.fee_rate or None
  if not fee_rate:
    wallet_kit: WalletKit = WalletKit()
    fee_estimate: EstimateFeeResponse = wallet_kit.estimate_fee()
    fee_rate = fee_estimate.sat_per_kw / 4_000  # sats per kiloweightunit -> sats per vByte
  remote_balance: int = purchase.remote_balance

  ### Calculate fees for inbound liquidity purchase ###
  total_fee_sats: int = fee_rate * ONCHAIN_BYTES_EST + ceil(remote_balance * FEE_PPM / 1e6)

  try:
    order: InboundOrder = await InboundOrder.create(host=host, port=port, pubkey=pubkey)
    lightning: Lightning = Lightning()
    add_invoice_response: AddInvoiceResponse = lightning.add_invoice(
      memo=f"Invoice for <InboundOrder (order-id={order.order_id})>", value=total_fee_sats
    )
    order.bolt11 = add_invoice_response.payment_request
    background_tasks.add_task(order.save)
    return {"bolt11": order.bolt11, "orderId": order.order_id}
  except ValidationError as err:
    response.status_code = 400
    return {"detail": str(err)}
  except IntegrityError:
    response.status_code = 502
    return {"detail": "Unable to receive order"}


__all__ = ["router"]

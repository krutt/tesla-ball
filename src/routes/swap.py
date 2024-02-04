#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:    ~~/src/routes/swap.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-04 00:15
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
Module detailing swap endpoints used for swapping bitcoin asset on the base-chain with bitcoin asset
on the Lightning liquidity network
"""

### Standard packages ###
import hashlib
from enum import Enum
from hashlib import sha256
from typing import List

### Third-party packages ###
from bitcoin.core.script import (
  CScript,
  OP_0,
  OP_CHECKLOCKTIMEVERIFY,
  OP_CHECKSIG,
  OP_DROP,
  OP_ELSE,
  OP_ENDIF,
  OP_EQUAL,
  OP_HASH160,
  OP_IF,
)
from bitcoin.wallet import P2WSHBitcoinAddress
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field, PositiveInt, StrictInt, StrictStr
from starlette.background import BackgroundTasks

### Local modules ###
from src.configs import SWAP_FEERATE
from src.helpers import encode_cltv
from src.schema import SwapOrder
from src.services import ChainKit, GetBestBlockResponse, Lightning, LnFeeEstimate

### Routing ###
router: APIRouter = APIRouter(
  prefix="/swap",
  tags=["Swap endpoints for swapping bitcoin from base-chain to Lightninng liquidity network"],
  responses={404: {"detail": "Not Found"}},
)


### Endpoint: schemas ###
class SwapType(str, Enum):
  reverse: str = "reverse"  # Lightning -> Chain
  submarine: str = "submarine"  # Chain -> Lightning


class SwapRequest(BaseModel):
  amount: PositiveInt = Field(description="Designated swap amount")
  claim_pubkey: StrictStr = Field(
    alias="claimPubkey", description="Public key of keypair needed for claiming"
  )
  pre_image: StrictStr = Field(alias="preImage", description="Pre-image for swap")
  refund_pubkey: StrictStr = Field(
    alias="refundPubkey", description="Public of keypair needed for refunding"
  )
  swap_type: SwapType = Field(SwapType.submarine, alias="swapType", description="Type of swap")


class SwapTicket(BaseModel):
  expected_amount: StrictInt = Field(alias="expectedAmount", description="")
  lockup: StrictStr = Field(description="Address in which the bitcoin will be locked up.")


### Endpoint: routes ###
@router.post("/", response_model=SwapTicket)
async def create_swap(background_tasks: BackgroundTasks, swap: SwapRequest) -> str:
  if swap.swap_type is SwapType.submarine:
    claim_buffer: List[int] = [
      int(swap.claim_pubkey[i : i + 2], 16) for i in range(0, len(swap.claim_pubkey), 2)
    ]
    claim: bytes = bytes(bytearray(claim_buffer))
    image_buffer: List[int] = [
      int(swap.pre_image[i : i + 2], 16) for i in range(0, len(swap.pre_image), 2)
    ]
    image: bytes = hashlib.new("ripemd160", bytearray(image_buffer)).digest()
    refund_buffer: List[int] = [
      int(swap.refund_pubkey[i : i + 2], 16) for i in range(0, len(swap.refund_pubkey), 2)
    ]
    refund: bytes = bytes(bytearray(refund_buffer))
    chain_kit: ChainKit = ChainKit()
    lightning: Lightning = Lightning()
    best_block: GetBestBlockResponse = chain_kit.best_block()
    timeout_blockheight: int = best_block.block_height + 6
    witness: bytes
    if swap.swap_type == "submarine":
      # fmt: off
      witness = CScript([
        OP_HASH160, image,
        OP_EQUAL,
        OP_IF,
          claim,
        OP_ELSE,
          encode_cltv(timeout_blockheight),
          OP_CHECKLOCKTIMEVERIFY,
          OP_DROP,
          refund,
        OP_ENDIF,
        OP_CHECKSIG,
      ])
      # fmt: on
    else:
      raise HTTPException(412, "Precondition failed")

    lockup: str = str(
      P2WSHBitcoinAddress.from_scriptPubKey(CScript([OP_0, sha256(witness).digest()]))
    )
    fee_estimate: LnFeeEstimate = lightning.estimate_fee(lockup, swap.amount, confirmations=1)
    fee_network: int = int(fee_estimate.fee_sat / fee_estimate.feerate_sat_per_byte)
    fee_service: int = int(swap.amount * SWAP_FEERATE / 100)
    expected_amount: int = fee_network + fee_service + swap.amount
    swap_order: SwapOrder = SwapOrder(
      claim_pubkey=swap.claim_pubkey,
      expected_amount=expected_amount,
      lockup=lockup,
      pre_image=swap.pre_image,
      refund_pubkey=swap.refund_pubkey,
      swap_type="submarine",
    )
    background_tasks.add_task(swap_order.save)
    return {"expectedAmount": expected_amount, "lockup": lockup}


__all__ = ["router"]

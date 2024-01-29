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
from hashlib import sha256
from enum import Enum

### Third-party packages ###
from bitcoin.core import Hash160
from bitcoin.core.script import (
  CScript,
  OP_0,
  OP_CHECKLOCKTIMEVERIFY,
  OP_CHECKSIG,
  OP_DROP,
  OP_DUP,
  OP_ELSE,
  OP_ENDIF,
  OP_EQUALVERIFY,
  OP_HASH160,
  OP_IF,
)
from bitcoin.wallet import P2WSHBitcoinAddress
from fastapi.responses import PlainTextResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field, PositiveInt, StrictStr

### Local modules ###
from src.services import (
  AddrResponse,
  ChainKit,
  GetBestBlockResponse,
  Lightning,
  LnFeeEstimate,
  WalletKit,
)
from src.configs import SWAP_FEERATE

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
  swap_type: SwapType = Field(SwapType.submarine, alias="swapType", description="Type of swap")


### Endpoint: routes ###
@router.post("/", response_class=PlainTextResponse)
async def create_swap(swap_request: SwapRequest) -> str:
  if swap_request.swap_type is SwapType.submarine:
    image: bytes = hashlib.new("ripemd160", swap_request.pre_image.encode("utf-8")).digest()
    claim_pubkey: bytes = swap_request.claim_pubkey.encode("utf-8")

    chain_kit: ChainKit = ChainKit()
    lightning: Lightning = Lightning()
    wallet_kit: WalletKit = WalletKit()

    addr_response: AddrResponse = wallet_kit.request_address()
    best_block: GetBestBlockResponse = chain_kit.best_block()
    locktime: int = best_block.block_height + 6
    refund_pubkey: bytes = addr_response.addr.encode("utf-8")

    # fmt: off
    witness: bytes = CScript([
      OP_IF,
        OP_HASH160, image, OP_EQUALVERIFY, OP_DUP, OP_HASH160, Hash160(claim_pubkey),
      OP_ELSE,
        locktime, OP_CHECKLOCKTIMEVERIFY, OP_DROP, OP_DUP, OP_HASH160, Hash160(refund_pubkey),
      OP_ENDIF,
      OP_EQUALVERIFY,
      OP_CHECKSIG,
    ])
    # fmt: on

    address: str = str(
      P2WSHBitcoinAddress.from_scriptPubKey(CScript([OP_0, sha256(witness).digest()]))
    )
    fee_estimate: LnFeeEstimate = lightning.estimate_fee(
      address, swap_request.amount, confirmations=1
    )
    fee_network: int = int(fee_estimate.fee_sat) / int(fee_estimate.feerate_sat_per_byte)
    fee_service: int = int(swap_request.amount * SWAP_FEERATE / 100)

    value_release: int = fee_network + fee_service + swap_request.amount

    # TODO: add hold invoice

    return address


__all__ = ["router"]

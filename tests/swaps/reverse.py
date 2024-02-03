#!/usr/bin/env python3.9
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:  ~~/tests/swaps/reverse.py
# VERSION: 	 0.1.0
# CREATED: 	 2024-02-02 18:06
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION: Using reference implementation by Boltz
#              https://github.com/BoltzExchange/boltz-core/blob/master/lib/swap/ReverseSwapScript.ts
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import List

### Third-party packages ###
import hashlib
from bitcoin.core.script import (
  CScript,
  OP_CHECKLOCKTIMEVERIFY,
  OP_CHECKSIG,
  OP_DROP,
  OP_ELSE,
  OP_ENDIF,
  OP_EQUAL,
  OP_EQUALVERIFY,
  OP_HASH160,
  OP_IF,
  OP_SIZE,
)
from pytest import mark

### Local modules ###
from src.helpers import encode_cltv


@mark.parametrize(
  "claim_pubkey, pre_image, refund_pubkey, snapshot, timeout_blockheight",
  [
    (
      "03f8109578aae1e5cfc497e466cf6ae6625497cd31886e87b2f4f54f3f0f46b539",
      "e5a211aa15cc91def065a1bf09f878991faeb9504d8606f645ec620cb9c09f1f",
      "03ec0c1e45b709d708cd376a6f2daf19ac27be229647780d592e27d7fb7efb207a",
      "8201208763a9144eee61c39e3b6d46f6fc7da6ae80519aa681f6d2882103f8109578aae1e5cfc497e466cf6ae6625497cd31886e87b2f4f54f3f0f46b53967750354df07b1752103ec0c1e45b709d708cd376a6f2daf19ac27be229647780d592e27d7fb7efb207a68ac",
      515924,
    )
  ],
)
def test_reverse_submarine_swap(
  claim_pubkey: str,
  pre_image: str,
  refund_pubkey: str,
  snapshot: str,
  timeout_blockheight: int,
) -> None:
  claim_buffer: List[int] = [
    int(claim_pubkey[i : i + 2], 16) for i in range(0, len(claim_pubkey), 2)
  ]
  claim: bytes = bytes(bytearray(claim_buffer))
  image_buffer: List[int] = [int(pre_image[i : i + 2], 16) for i in range(0, len(pre_image), 2)]
  image: bytes = hashlib.new("ripemd160", bytearray(image_buffer)).digest()
  refund_buffer: List[int] = [
    int(refund_pubkey[i : i + 2], 16) for i in range(0, len(refund_pubkey), 2)
  ]
  refund: bytes = bytes(bytearray(refund_buffer))

  # fmt: off
  witness: bytes = CScript([
    OP_SIZE,
      encode_cltv(32),
    OP_EQUAL,
      OP_IF,
        OP_HASH160,
          image,
        OP_EQUALVERIFY,
          claim,
      OP_ELSE,
        OP_DROP,
          encode_cltv(timeout_blockheight),
          OP_CHECKLOCKTIMEVERIFY,
        OP_DROP,
          refund,
      OP_ENDIF,
    OP_CHECKSIG
  ])
  # fmt: on
  assert witness.hex() == snapshot

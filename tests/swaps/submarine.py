#!/usr/bin/env python3.9
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:  ~~/tests/swaps/submarine.py
# VERSION: 	 0.1.0
# CREATED: 	 2024-02-02 18:06
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION: Using reference implementation by Boltz
#              https://github.com/BoltzExchange/boltz-core/blob/master/lib/swap/SwapScript.ts
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
  OP_HASH160,
  OP_IF,
)
from pytest import mark

### Local modules ###
from src.helpers import encode_cltv


@mark.parametrize(
  "claim_pubkey, pre_image, refund_pubkey, snapshot, timeout_blockheight",
  [
    (
      "03f8109578aae1e5cfc497e466cf6ae6625497cd31886e87b2f4f54f3f0f46b539",
      "53ada8e6de01c26ff43040887ba7b22bddce19f8658fd1ba00716ed79d15cd5e",
      "03ec0c1e45b709d708cd376a6f2daf19ac27be229647780d592e27d7fb7efb207a",
      """
      a914e2ac8cb97af3d59b1c057db4b0c4f9aa12a9127387632103f8109578aae1e5cfc497e466cf6ae6625497cd3188
      6e87b2f4f54f3f0f46b539670354df07b1752103ec0c1e45b709d708cd376a6f2daf19ac27be229647780d592e27d7
      fb7efb207a68ac
      """.replace("\n", "").replace(" ", ""),
      515924,
    )
  ],
)
def test_submarine_swap(
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

  assert witness.hex() == snapshot

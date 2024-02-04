#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:  ~~/tests/grpc/send_payment.py
# VERSION: 	 0.1.0
# CREATED: 	 2024-01-29 18:43
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from pytest import mark

### Local modules ###
from src.services.lightning import AddInvoiceResponse, Lightning, SendResponse
from tests.grpc import external_lightning, lightning


@mark.parametrize(
  "amount",
  [100, 1_000, 10_000, 100_000, 1_000_000],
)
def test_02_check_invoice_after_paid(
  amount: int, external_lightning: Lightning, lightning: Lightning
) -> None:
  add_invoice: AddInvoiceResponse = external_lightning.add_invoice(memo="testInvoice", value=amount)
  assert add_invoice is not None
  assert add_invoice.payment_request is not None
  assert isinstance(add_invoice.payment_request, str)
  assert add_invoice.r_hash is not None
  assert isinstance(add_invoice.r_hash, bytes)
  response: SendResponse = lightning.send_payment(add_invoice.payment_request)
  assert response is not None
  assert response.payment_hash is not None
  assert isinstance(response.payment_hash, bytes)
  assert response.payment_hash == add_invoice.r_hash
  assert response.payment_route is not None
  assert response.payment_route.total_amt is not None
  assert isinstance(response.payment_route.total_amt, int)
  assert response.payment_route.total_amt == amount

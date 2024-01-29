#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/tests/grpc/list_invoices.py
# VERSION: 	   0.1.0
# CREATED: 	   2024-01-16 16:53
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Generator

### Third-party packages ###
from pytest import fixture, mark

### Local modules ###
from src.services.lightning import AddInvoiceResponse, Lightning, ListInvoiceResponse
from tests.grpc import external_lightning, lightning


### Module-specific setup-teardown ###
@fixture(scope="module", autouse=True)
def setup_teardown(external_lightning: Lightning, lightning: Lightning) -> Generator:
  response: ListInvoiceResponse = lightning.list_invoices()
  [external_lightning.send_payment(invoice.payment_request) for invoice in response.invoices]
  yield
  [external_lightning.send_payment(invoice.payment_request) for invoice in response.invoices]


def test_01_list_invoices(lightning: Lightning) -> None:
  response: ListInvoiceResponse = lightning.list_invoices()
  assert response is not None
  if response.invoices is None:
    for invoice in response.invoices:
      assert invoice.state == 1  # SETTLED


def test_02_list_empty_unsettled_invoices(lightning: Lightning) -> None:
  response: ListInvoiceResponse = lightning.list_invoices()
  assert response is not None
  if response.invoices is not None:
    unsettled = [*filter(lambda invoice: invoice.state != 1, response.invoices)]
    assert len(unsettled) == 0


@mark.parametrize("amount", [1, 2, 3, 4, 5])
def test_03_list_one_invoice(amount: int, lightning: Lightning) -> None:
  add_invoice: AddInvoiceResponse = lightning.add_invoice(memo="test-invoice", value=amount)
  assert add_invoice is not None
  response: ListInvoiceResponse = lightning.list_invoices()
  assert response is not None
  assert response.invoices is not None
  assert len(response.invoices) != 0
  invoice = response.invoices[-1]  # last added invoice
  assert invoice.memo == "test-invoice"
  assert invoice.value == amount

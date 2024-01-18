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

### Third-party packages ###
from pytest import mark

### Local modules ###
from src.services.lightning import AddInvoiceResponse, Lightning, ListInvoiceResponse
from tests.grpc import lightning


def test_01_list_empty_invoices(lightning: Lightning) -> None:
    list_invoice_response: ListInvoiceResponse = lightning.list_invoices()
    assert list_invoice_response is not None
    print(list_invoice_response)
    # assert len(list_invoice_response) == 0

@mark.parametrize("amount", [0, 1, 2, 3, 4, 5])
def test_02_list_one_invoice(amount: int, lightning: Lightning) -> None:
    add_invoice: AddInvoiceResponse = lightning.add_invoice(memo="test-invoice", value=amount)
    assert add_invoice is not None
    list_invoice_response: ListInvoiceResponse = lightning.list_invoices()
    assert list_invoice_response is not None
    assert list_invoice_response.invoices is not None
    assert len(list_invoice_response.invoices) != 0
    invoice = list_invoice_response.invoices[-1]  # last added invoice
    assert invoice.memo == "test-invoice"
    assert invoice.value == amount

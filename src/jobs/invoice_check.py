#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:    ~~/src/jobs/invoice_check.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-14 19:17
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import List

### Local modules ###
from src.schema import InboundOrder, OrderState
from src.services.lightning import Invoice, Lightning, PayReq


async def job() -> None:
  lightning: Lightning = Lightning()
  orders: List[InboundOrder] = await InboundOrder.pending()  # type: ignore[assignment]
  for order in orders:
    payment_request: PayReq = lightning.decode_pay_req(order.bolt11)
    invoice: Invoice = lightning.lookup_invoice(payment_request.payment_hash)
    if invoice.state in (0, 3):  # OPEN, ACCEPTED
      continue
    elif invoice.state in (1, 2):  # SETTLED, CANCELED
      order.state = (OrderState.PAID, OrderState.REJECTED)[invoice.state - 1]
      await order.save()


__all__ = ["job"]

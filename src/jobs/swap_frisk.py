#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:    ~~/src/jobs/swap_frisk.py
# VERSION: 	   0.1.0
# CREATED: 	   2024-02-04 13:37
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import List

### Local modules ###
from src.schema import SwapOrder


async def job() -> None:
  orders: List[SwapOrder] = await SwapOrder.pending()  # type: ignore[assignment]
  for order in orders:
    print(order)

__all__ = ["job"]

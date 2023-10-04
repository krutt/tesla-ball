#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
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

### Third-party packages ###
from fastapi.routing import APIRouter

### Routing ###
router: APIRouter = APIRouter(
    prefix="/swap",
    tags=["Swap endpoints for swapping bitcoin from base-chain to Lightninng liquidity network"],
    responses={404: {"description": "Not Found"}},
)

# TODO: define routes

__all__ = ["router"]

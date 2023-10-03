#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/routes/inbound.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-04 00:15
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
Module detailing inbound liquidity purchase endpoints used for creating channels between this node
and requester's node
"""

### Third-party packages ###
from fastapi import APIRouter

### Routing ###
router: APIRouter = APIRouter(
    prefix="/inbound",
    tags=["Inbound liquidity purchase endpoints"],
    responses={404: {"description": "Not Found"}},
)

# TODO: define routes

__all__ = ["router"]

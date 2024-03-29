#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:    ~~/src/routes/earn.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-04 00:15
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
Module defining earning opportunity endpoints using Lightning's force-closures as a method to clear
up lazy capital for a reward
"""

### Third-party packages ###
from fastapi.routing import APIRouter

### Routing ###
router: APIRouter = APIRouter(
  prefix="/earn",
  tags=["Earn endpoint"],
  responses={404: {"detail": "Not Found"}},
)

# TODO: define routes
__all__ = ["router"]

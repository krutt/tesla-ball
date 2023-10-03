#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/routes/__init__.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-04 00:15
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Local modules ###
from src.routes.earn import router as earn_router
from src.routes.inbound import router as inbound_router
from src.routes.swap import router as swap_router

__all__ = ["earn_router", "inbound_router", "swap_router"]

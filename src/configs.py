#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/configs.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-04 00:15
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
Module detailing environment variables used by server and services
"""

### Local modules ###
from os import environ

DEFAULT_TIMEZONE: str = environ.get("DEFAULT_TIMEZONE", "Asia/Bangkok")
PORT: int = int(environ.get("PORT", 8080))
REDIS_URL: str = environ.get("REDIS_URL", "redis://localhost:5432")
SECRET_KEY: str = environ.get("SECRET_KEY", "asecrettoeverybody")
TIME_FORMAT: str = environ.get("TIME_FORMAT", "MMM DD, HH:mm")

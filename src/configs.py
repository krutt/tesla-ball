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

### Standard packages ###
from typing import Optional

### Load dotenv envionment if `python-dotenv` is installed ###
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

### Local modules ###
from os import environ
from typing import Optional

DATABASE_NAME: str = environ.get("DATABASE_NAME", "tesladb")
DATABASE_URL: Optional[str] = environ.get(
    "DATABASE_URL", None
)  # defaults to "postgres://localhost:5432"
if DATABASE_URL is None:
    ### Derive `DATABASE_URL` from env vars ###
    DATABASE_HOST: str = environ.get("DATABASE_HOST", "localhost")
    DATABASE_NGIN: str = environ.get("DATABASE_NGIN", "postgres")
    DATABASE_PASS: Optional[str] = environ.get("DATABASE_PASS", None)
    DATABASE_PORT: int = int(environ.get("DATABASE_PORT", "5432"))
    DATABASE_USER: Optional[str] = environ.get("DATABASE_USER", None)
    if DATABASE_USER is not None and DATABASE_PASS is not None:
        DATABASE_URL = (
            f"{ DATABASE_NGIN }://{ DATABASE_USER }:{ DATABASE_PASS }"
            f"@{ DATABASE_HOST }:{ DATABASE_PORT }"
        )
    elif DATABASE_USER is not None:
        DATABASE_URL = f"{ DATABASE_NGIN }://{ DATABASE_USER }@{ DATABASE_HOST }:{ DATABASE_PORT }"
    elif DATABASE_PASS is not None:
        DATABASE_URL = f"{ DATABASE_NGIN }://:{ DATABASE_PASS }@{ DATABASE_HOST }:{ DATABASE_PORT }"
    else:
        DATABASE_URL = f"{ DATABASE_NGIN }://{ DATABASE_HOST }:{ DATABASE_PORT }"

LIQUIDITY_FEE_PPM: int = int(environ.get("LIQUIDITY_FEE_PPM", "1500"))
LND_HOST_URL: str = environ.get("LND_HOST_URL", "localhost:10009")
LND_MACAROON_PATH: Optional[str] = environ.get("LND_MACAROON_PATH", None)
LND_TLSCERT_PATH: Optional[str] = environ.get("LND_TLSCERT_PATH", None)
ONCHAIN_BYTES_EST: int = int(environ.get("ONCHAIN_BYTES_EST", "300"))
PORT: int = int(environ.get("PORT", 8080))
SECRET_KEY: str = environ.get("SECRET_KEY", "itsasecrettoeverybody")
SWAP_FEERATE: float = float(environ.get("SWAP_FEERATE", "0.5"))

__all__ = [
    "DATABASE_NAME",
    "DATABASE_URL",
    "DEFAULT_TIMEZONE",
    "LND_HOST_URL",
    "LND_MACAROON_PATH",
    "LND_TLSCERT_PATH",
    "PORT",
    "SECRET_KEY",
]

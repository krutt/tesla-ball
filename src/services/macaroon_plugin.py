#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/services/macaroon_plugin.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-28 18:44
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Any, Callable

### Third-party packages ###
from grpc import AuthMetadataPlugin
from pydantic import BaseModel


class MacaroonPlugin(AuthMetadataPlugin, BaseModel):
    """Metadata plugin to include macaroon in metadata of each RPC request"""

    macaroon: str

    def __call__(self, _: Any, callback: Callable) -> Any:
        callback([("macaroon", self.macaroon)], None)


__all__ = ["MacaroonMetadataPlugin"]
